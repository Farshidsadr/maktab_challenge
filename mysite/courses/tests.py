from django.test import TestCase
from courses.models import Course, Review, Teacher
from django.contrib.auth import get_user_model
from accounts.models import User as UserModel
from rest_framework.test import APIClient
import datetime
import pytz

User = get_user_model()


class CourseModelTest(TestCase):
    def setUp(self) -> None:
        user: UserModel = User.objects.create(username='teacher1', email='teacher1@django.com', password='A123456789a')
        teacher: Teacher = Teacher.objects.create(user=user)
        Course.objects.create(title='Course 1', teacher=teacher, price=125000,
                              published_at=datetime.datetime(2022, 2, 1, tzinfo=pytz.UTC))
        db_course2: Course = Course.objects.create(title='Course 2', teacher=teacher, price=225000,
                                                   published_at=datetime.datetime(2022, 2, 1, tzinfo=pytz.UTC))
        Review.objects.create(course=db_course2, user=teacher.user, score=3)
        Review.objects.create(course=db_course2, user=teacher.user, score=5)

    def test_course_avg_has_no_review_should_return_zero(self):
        """
        Courses that have no reviews should return 0 average
        :return: None
        """
        db_course = Course.objects.filter(title='Course 1').first()
        self.assertEqual(db_course.review_avg, 0)

    def test_course_2_avg_should_return_4(self):
        """
        The two reviews that created for course 2 have scores 3 and 5, and should return average 4
        :return: None
        """
        db_course = Course.objects.filter(title='Course 2').first()
        self.assertEqual(db_course.review_avg, 4)


class CourseViewTest(TestCase):
    def setUp(self) -> None:
        user: UserModel = User.objects.create(username='teacher1', email='teacher1@django.com', password='A123456789a')
        teacher: Teacher = Teacher.objects.create(user=user)
        Course.objects.create(title='Course 1', teacher=teacher, price=125000,
                              published_at=datetime.datetime(2022, 1, 1, tzinfo=pytz.UTC))
        Course.objects.create(title='Course 2', teacher=teacher, price=225000,
                              published_at=datetime.datetime(2022, 2, 1, tzinfo=pytz.UTC))

        user2: UserModel = User.objects.create(username='teacher2', email='teacher2@django.com', password='A123456789a')
        teacher2: Teacher = Teacher.objects.create(user=user2)

    def test_anyone_should_can_retrieve_course(self):
        """
        Any authenticated and unauthenticated users should have possibility to retrieve specific course
        :return: None
        """
        client = APIClient()
        response = client.get('/api/courses/1/')

        self.assertEqual(response.status_code, 200)

    def test_anyone_should_can_get_course_list(self):
        """
        Any authenticated and unauthenticated users should have possibility to get course list
        :return:
        """
        client = APIClient()
        response = client.get('/api/courses/')

        self.assertEqual(response.status_code, 200)

    def test_update_course_by_anonymous_should_not_work(self):
        """
        Unauthenticated users shouldn't have ability to update course
        :return: None
        """
        client = APIClient()
        response = client.put('/api/courses/1/', {
            "title": "Python Course Advance3",
            "description": "salam",
            "teacher": 1,
            "published_at": "2022-03-1T20:00",
            "price": 100000
        })
        self.assertEqual(response.status_code, 401)

    def test_update_related_course_to_authenticated_teacher_should_work(self):
        """
        Authenticated teacher should have ability to update his/her courses
        :return: None
        """
        user = User.objects.get(username='teacher1')
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.put('/api/courses/1/', {
            "title": "Python Course Advance3",
            "description": "salam",
            "teacher": 1,
            "published_at": "2022-03-1T20:00",
            "price": 100000
        })
        self.assertEqual(response.status_code, 200)

    def test_update_unrelated_course_to_authenticated_teacher_should_not_work(self):
        """
        Authenticated teacher should not have ability to update other teachers courses
        :return: None
        """
        user = User.objects.get(username='teacher2')
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.put('/api/courses/1/', {
            "title": "Python Course Advance3",
            "description": "salam",
            "teacher": 1,
            "published_at": "2022-03-1T20:00",
            "price": 100000
        })
        self.assertEqual(response.status_code, 403)
