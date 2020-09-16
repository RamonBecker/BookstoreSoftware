
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views

urlpatterns = [
  
    path('admin/', admin.site.urls),
    path('conta/',include('django.contrib.auth.urls'), name='login'),
   # path('accounts/login/', views.LoginView.as_view(), name='login'),
   # path('accounts/logout/', views.LogoutView.as_view(next_page='/'), name='logout'),
    path('blog', include('blog.urls'), name='blog'),  
    path('', include('livraria.urls')),
]
