from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet

from students.filters import CourseFilter
from students.models import Course
from students.serializers import CourseSerializer


class CoursesViewSet(ModelViewSet):

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = CourseFilter

    def create(self, request, *args, **kwargs):
        # if request.course.students.count() >= settings.MAX_STUDENTS_PER_COURSE:
        if len(request.data.get('students')) >= settings.MAX_STUDENTS_PER_COURSE:
            raise ValidationError('too many students on course', code='too-many-students')
        return super().create(request, *args, **kwargs)