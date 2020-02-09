import markdown
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.utils import timezone

from oj.models import Course, Assignment, Submission, GradeUnit


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
    template_name = 'oj/course/course_assignment.html'

    def get_queryset(self):
        self.course = get_object_or_404(Course, identifier=self.kwargs['course_identifier'])
        return Assignment.objects.filter(course=self.course).filter(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # TODO: get extra user related data, such as submission history

        # Needed for left sidebar
        assignments = Assignment.objects.filter(course=self.course)
        context['assignments'] = assignments
        context['course'] = self.course

        # Rendered assignment description
        self.object.description = markdown.markdown(self.object.description,
                                                    extensions=[
                                                        'markdown.extensions.extra',
                                                        'markdown.extensions.codehilite',  # 代码高亮
                                                        'markdown.extensions.toc'
                                                    ])
        if self.object.alert:
            self.object.alert = markdown.markdown(self.object.alert,
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
        if len(submissions) == 0:
            best_submission = None
        else:
            best_submission = submissions.order_by('grade')[0]
        context['best_submission'] = best_submission

        return context
