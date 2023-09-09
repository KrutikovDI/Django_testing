import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Student, Course

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def student():
    return Student.objects.create(name='Ivan')

@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory

@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.maker(Student, *args, **kwargs)
    return factory



@pytest.mark.django_db
def test_example(client, student, course_factory):
            # Arrange
    # client = APIClient()                             # заменяется фикстурой
    # stud1 = Student.objects.create(name='Ivan')      # заменяется фикстурой
    courses = course_factory(_quantity=10)
    # course1 = Course.objects.create(name='Java')
    # courses.students.set([student, ])
            # Act
    response = client.get('/api/v1/courses/')
            # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)
    for i, m in enumerate(data):
        assert m['name'] == courses[i].name

@pytest.mark.django_db
def test_course_create(client, student):
    # client = APIClient()                            # заменяется фикстурой
    count = Course.objects.count()
    response = client.post('/api/v1/courses/', data={'id': 1, 'name': 'Java', 'students': [student.id, ]})
    assert response.status_code == 201
    assert Course.objects.count() == count + 1

@pytest.mark.django_db
def test_student_create(client):
    students = student_factory(_quantity=20)
    response = client.post('/api/v1/courses', data={'id': 1, 'name': 'Java', 'students': [students]})
    assert response.status_code == 201