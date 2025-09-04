from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('password-change/', views.PasswordChangeView.as_view(), name='password_change'),
    
    # User management
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/update/', views.ProfileUpdateView.as_view(), name='profile_update'),
    
    # Departments
    path('departments/', views.DepartmentListCreateView.as_view(), name='department_list_create'),
    path('departments/<int:pk>/', views.DepartmentDetailView.as_view(), name='department_detail'),
    
    # Faculty profiles
    path('faculty/', views.FacultyProfileListCreateView.as_view(), name='faculty_list_create'),
    path('faculty/<int:pk>/', views.FacultyProfileDetailView.as_view(), name='faculty_detail'),
    
    # Student profiles
    path('students/', views.StudentProfileListCreateView.as_view(), name='student_list_create'),
    path('students/<int:pk>/', views.StudentProfileDetailView.as_view(), name='student_detail'),
    
    # Parent profiles
    path('parents/', views.ParentProfileListCreateView.as_view(), name='parent_list_create'),
    path('parents/<int:pk>/', views.ParentProfileDetailView.as_view(), name='parent_detail'),
    
    # Parent-student relationships
    path('relationships/', views.ParentStudentRelationshipListCreateView.as_view(), name='relationship_list_create'),
    path('relationships/<int:pk>/', views.ParentStudentRelationshipDetailView.as_view(), name='relationship_detail'),
    
    # Invitations
    path('invitations/', views.InvitationListCreateView.as_view(), name='invitation_list_create'),
    path('invitations/<int:pk>/', views.InvitationDetailView.as_view(), name='invitation_detail'),
    path('invitations/accept/<str:token>/', views.accept_invitation, name='accept_invitation'),
]
