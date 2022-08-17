from django.urls import path

from dataservice.view.student_view import StudentView
from dataservice.view.teacher_view import TeacherView


app_name = "dataservice"

urlpatterns = [
	path('students/', StudentView.as_view(), name='student_list'),
    path('teacher/', TeacherView.as_view(), name='teacher_list'),
     path('teacher/', TeacherView.as_view(), name='teacher_list'),
    
	
]

	