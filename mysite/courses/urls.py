from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register("courses", views.CourseViewSet)
router.register("teachers", views.TeacherViewSet)
router.register("reviews", views.ReviewViewSet)

urlpatterns = [
    path('', include(router.urls))
]
