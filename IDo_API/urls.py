from django.urls import path
from .views import *
from .topicviews import *
from .tasksviews import *

urlpatterns = [
    path('users/create', create_user, name='create_user'),
    path('users/delete', delete_user, name='delete_user'),
    path('users/edit/', edit_user, name='edit_user'),
    path('users/', get_user, name='get_user'),
    path('tasks/', get_task, name='get_task'),
    path('users/logout/', log_out, name='log_out'),
    path('topics/create/', create_topic, name='create_topic'),
    path('topics/edit/<int:pk>/', edit_topic, name='edit_topic'),
    path('topics/delete/<int:pk>/', delete_topic, name='delete_topic'),
    path('topics/', get_topics, name='get_topics'),
    path('topics/<int:pk>', get_topic, name='get_topic'),
    path('topics/<int:pk>/create_subtopic', create_subtopic, name="create_subtopic"),
    path('subtopics/', get_subtopics, name="get_subtopics"),
    path('subtopics/<int:pk>/', get_subtopic, name='get_subtopic'),
    path('subtopics/edit/<int:pk>', edit_subtopic, name='edit_subtopic'),
    path('subtopics/delete/<int:pk>', delete_subtopic, name='delete_subtopic'),
    path('subtopics/create_task/', create_task, name='create_task'),
    path('tasks/edit/<int:pk>/', edit_task, name='edit_task'),
    path('tasks/delete/<int:pk>/', delete_task, name='delete_task'),
    path('tasks/<int:pk>/', get_task, name='get_task'),
    path('tasks/', get_tasks, name='get_tasks')
]