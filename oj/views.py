import markdown
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views import generic

from oj.models import Course, Assignment


def index(request):
    return render(request, 'oj/index.html')


class CourseListview(LoginRequiredMixin, generic.ListView):
    model = Course
    paginate_by = 10
    template_name = "oj/course_list.html"

    def get_queryset(self):
        return Course.objects.filter(student=self.request.user)


class CourseDetailView(LoginRequiredMixin, generic.DetailView):
    model = Course
    template_name = 'oj/course/index.html'
    slug_url_kwarg = 'course_identifier'

    def get_slug_field(self):
        return 'identifier'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        assignments = Assignment.objects.filter(course=self.object)
        context['assignments'] = assignments
        return context


class CourseAssignmentView(LoginRequiredMixin, generic.DetailView):
    template_name = 'oj/course/assignment.html'

    def get_queryset(self):
        self.course = get_object_or_404(Course, identifier=self.kwargs['course_identifier'])
        return Assignment.objects.filter(course=self.course).filter(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # TODO: get extra user related data, such as submission history

        # Needed for left sidebar
        assignments = Assignment.objects.filter(course=self.course).order_by('id')
        context['assignments'] = assignments
        context['course'] = self.course

        # Previous, Next
        previous_assignment = assignments.filter(id__lte=self.object.id).exclude(id=self.object.id).order_by('id')
        next_assignment = assignments.filter(id__gte=self.object.id).exclude(id=self.object.id).order_by('id')
        context['previous_assignment'] = previous_assignment.last()
        context['next_assignment'] = next_assignment.first()

        # Rendered assignment description
        self.object.description = markdown.markdown(self.object.description,
                                                    extensions=[
                                                        'markdown.extensions.extra',
                                                        'markdown.extensions.codehilite',  # 代码高亮
                                                        'markdown.extensions.toc'
                                                    ])

        # Check if deadline is passed.
        context['pass_deadline'] = timezone.now() > self.object.deadline

        # Submission records
        submissions = Submission.objects.filter(user=self.request.user).filter(assignment=self.object)
        context['submissions'] = submissions

        # Get best score
        graded_submissions = submissions.filter(gradereport__isnull=False)
        if len(graded_submissions) == 0:
            best_submission = None
        else:
            best_submission = graded_submissions.order_by('gradereport__grade')[0]
        context['best_submission'] = best_submission

        return context


from .forms import SubmissionForm
from .models import Submission
from bootstrap_modal_forms.generic import BSModalCreateView


class SubmissionCreateView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'oj/course/component/assignment/submit.html'
    form_class = SubmissionForm
    success_message = 'Success: Submission was created.'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.assignment = get_object_or_404(Assignment,
                                                     id=self.kwargs.get('assignment_pk'))  # new line
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')
