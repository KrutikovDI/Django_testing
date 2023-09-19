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

# получение деталей одного курса
@pytest.mark.django_db
def test_get_course(client, student, course_factory):
    course1 = Course.objects.create(name='Java')
    course1.students.set([student, ])
    response = client.get('/api/v1/courses/')
    data = response.json()
    assert len(data) == 1
    assert data[0]['name'] == course1.name

# получение списка курсов
@pytest.mark.django_db
def test_get_list_courses(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get('/api/v1/courses/')
    data = response.json()
    assert len(data) == len(courses)

# получение списка курсов, отфильтрованных по id
@pytest.mark.django_db
def test_get_courses_id(client, student, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get('/api/v1/courses/')
    data = response.json()
    assert data[3]['id'] == courses[3].id

# получение списка курсов, отфильтрованных по имени курса
@pytest.mark.django_db
def test_get_courses_name(client, student, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get('/api/v1/courses/')
    data = response.json()
    for i, m in enumerate(data):
        assert m['name'] == courses[i].name

# тест на создание курса
@pytest.mark.django_db
def test_course_create(client, student):
    count = Course.objects.count()
    response = client.post('/api/v1/courses/', data={'id': 1, 'name': 'Java', 'students': [student.id, ]})
    assert response.status_code == 201
    assert Course.objects.count() == count + 1

# тест на обновление курса
@pytest.mark.django_db
def test_course_update(client, student):
    # students = student_factory(_quantity=20).json()
    course_factory(_quantity=10)
    response = client.update('/api/v1/courses', data={'id': 1, 'name': 'Java'})
    data = response.json()
    assert data[1]['name'] == response.name

# тест на удаление курса
@pytest.mark.django_db
def test_course_delete(client, student):
    courses = course_factory(_quantity=10)
    response = client.delete('/api/v1/courses', data={'id': 1})
    assert response.status_code == 201

# Добавить валидацию на максимальное число студентов на курсе — 20
@pytest.mark.django_db
def test_course_max_students(client):
    students = student_factory(_quantity=21)
    response = client.post('/api/v1/courses/', data={'id': 1, 'name': 'Java', 'students': [students.id, ]})
    assert response.status_code == 201

