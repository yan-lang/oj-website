import markdown
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
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


class CourseDetailView(generic.DetailView):
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


class CourseAssignmentView(generic.DetailView):
    template_name = 'oj/course/course_assignment.html'

    def get_queryset(self):
        self.course = get_object_or_404(Course, identifier=self.kwargs['course_identifier'])
        return Assignment.objects.filter(course=self.course).filter(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # TODO: get extra user related data, such as submission history
        assignments = Assignment.objects.filter(course=self.course)
        context['assignments'] = assignments
        context['course'] = self.course
        self.object.description = markdown.markdown(self.object.description,
                                                    extensions=[
                                                        'markdown.extensions.extra',
                                                        'markdown.extensions.codehilite',  # 代码高亮
                                                        'markdown.extensions.toc'
                                                    ])
        return context
