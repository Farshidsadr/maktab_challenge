from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.mixins import ListModelMixin

from .serializers import CourseSerializer, TeacherSerializer, CourseListSerializer, ReviewSerializer
from .models import Course, Teacher, Review
from .permissions import IsCourseTeacherOrReadOnly, IsCourseTeacher


class PaginationClass(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.none()
    pagination_class = PaginationClass

    def get_permissions(self):
        # I don't know the system policies, so I define my approach for permissions
        if self.action == 'list' or self.action == 'retrieve':
            self.permission_classes = [IsCourseTeacherOrReadOnly]
        # only course teacher can update it
        elif self.action == "update":
            self.permission_classes = [IsCourseTeacher]
        # only admins can do delete and other actions for course
        else:
            self.permission_classes = [IsAdminUser]

        return super(CourseViewSet, self).get_permissions()

    def get_serializer_class(self):
        if self.action == "list":
            return CourseListSerializer
        return CourseSerializer

    def get_queryset(self):
        # ToDo: Override the get_queryset to display courses sorted by published_at
        course = Course.objects.order_by('-published_at')
        return course


class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    pagination_class = PaginationClass

    # ToDo: Add the required action here
    # when we use pagination, it's better to apply filter in an ordered query,
    # so by default we order teachers by created date to prevent inconsistent results
    def get_queryset(self):
        teachers = Teacher.objects.order_by('-created')
        return teachers

    # ToDo: Add an action that returns user's course list upon /teachers/1/courses
    @action(detail=True, methods=['GET'], name='Get Courses', url_path='courses')
    def get_courses(self, request, *args, **kwargs):
        teacher = self.get_object()
        queryset = Course.objects.filter(teacher=teacher)

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = CourseListSerializer(queryset, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CourseListSerializer(queryset, many=True)

        return Response(serializer.data)


class ReviewViewSet(GenericViewSet,
                    ListModelMixin):
    queryset = Review.objects.none()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # ToDo: Override the get_queryset so that only the user's own reviews are displayed.
        reviews = Review.objects.filter(user=self.request.user)
        return reviews
