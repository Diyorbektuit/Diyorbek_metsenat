from django.urls import path
from . import views


urlpatterns = [
    path('sponsors/add/', views.SponsorPostView.as_view(), name='add_sponsor'),
    path('students/', views.StudentList.as_view(), name='students'),
    path('students/<int:pk>/', views.StudentDetailUpdate.as_view(), name='student'),
    path('sponsors/', views.SponsorList.as_view(), name='sponsors'),
    path('sponsors/<int:pk>/', views.SponsorDetailUpdate.as_view(), name='sponsor'),
    path('add/sponsor/', views.StudentSponsorAddView.as_view(), name='sponsor_add_sponsor'),
    path('update/sponsor/<int:pk>/', views.StudentSponsorUpdateView.as_view(), name='update_student_sponsor'),
    path('students/add/', views.StudentCreateView.as_view(), name='add_student'),
    path('students/<int:pk>/delete/', views.StudentDeleteView.as_view(), name='delete_student'),
    path('sponsors/<int:pk>/delete/', views.SponsorDeleteView.as_view(), name='delete_sponsor'),

]