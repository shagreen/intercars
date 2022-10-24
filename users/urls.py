from django.urls import path, include

from users.views.user import UserLogin, UserLogout

users_patterns = [
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
]

urlpatterns = [
    path('', include((users_patterns, 'users'))),
]
