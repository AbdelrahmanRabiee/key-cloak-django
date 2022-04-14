from rest_framework import routers

from users import views

app_name = "users"

user_router = routers.SimpleRouter()

user_router.register(r'admin', views.AdminUserViewSet, basename='admin')
user_router.register(r'user', views.NormalUserViewSet, basename='users')
user_router.register(r'login', views.LoginViewSet, basename='login')

urlpatterns = user_router.urls