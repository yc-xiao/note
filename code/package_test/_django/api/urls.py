from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers

from django.urls import path, include
from api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(r"login", obtain_jwt_token),

    path('sets/', views.set_session),
    path('cleans/', views.clean_session),
]
