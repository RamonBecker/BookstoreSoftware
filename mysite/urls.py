
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views
from django.contrib.auth import views as auth_views

urlpatterns = [
  
    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls')),
   # path('accounts/login/', views.LoginView.as_view(), name='login'),
   # path('accounts/logout/', views.LogoutView.as_view(next_page='/'), name='logout'),
    #path('accounts/password_change/', views.PasswordChangeForm.as_view(), name='change'),
 
    path('blog', include('blog.urls'), name='blog'),  
    path('', include('livraria.urls')),
 
]
