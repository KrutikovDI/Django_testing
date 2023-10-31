import json

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
        return baker.make(Student, *args, **kwargs)
    return factory

# получение деталей одного курса
# @pytest.mark.django_db
# def test_get_course(client, course_factory):
#     courses = course_factory(_quantity=10)
#     course_id = courses[5].id
#     url = f'/api/v1/courses/'
#     response = client.get(url, data={'id': course_id})
#     data = response.json()
#     assert data[0]['id'] == course_id

@pytest.mark.django_db
def test_get_course(client, course_factory):
    courses = course_factory(_quantity=10)
    course_id = courses[5].id
    url = f'/api/v1/courses/{course_id}'
    response = client.get(url)
    data = response.json()
    assert data['id'] == course_id

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
    course_id = courses[5].id
    url = f'/api/v1/courses/'
    response = client.get(url, data={'id': course_id})
    data = response.json()
    assert data[0]['id'] == course_id

# получение списка курсов, отфильтрованных по имени курса
@pytest.mark.django_db
def test_get_courses_name(client, course_factory):
    courses = course_factory(_quantity=10)
    course_name = courses[5].name
    response = client.get('/api/v1/courses/', data={'name': course_name})
    data = response.json()
    assert data[0]['name'] == course_name

# тест на создание курса
@pytest.mark.django_db
def test_course_create(client, student):
    count = Course.objects.count()
    response = client.post('/api/v1/courses/', data={'id': 1, 'name': 'Java', 'students': [student.id, ]})
    assert response.status_code == 201
    assert Course.objects.count() == count + 1

# тест на обновление курса
@pytest.mark.django_db
def test_course_update(client, course_factory):
    courses = course_factory(_quantity=10)
    course_id = courses[5].id
    response = client.patch(f'/api/v1/courses/{course_id}', data={'name': 'Java'}, follow=True)
    assert response.status_code == 200

# тест на удаление курса
@pytest.mark.django_db
def test_course_delete(client, course_factory):
    courses = course_factory(_quantity=10)
    course_id = courses[0].id
    response = client.delete(f'/api/v1/courses/{course_id}')
    assert response.status_code == 201

# Добавить валидацию на максимальное число студентов на курсе — 20
@pytest.mark.django_db
def test_course_max_students(client, student_factory):
    students = student_factory(_quantity=21)
    students_list_id = []
    for i in range(0,21):
        students_list_id.append(students[i].id)
    response = client.post('/api/v1/courses/', data={'id': 1, 'name': 'Java', 'students': students_list_id})
    assert response.status_code == 201

