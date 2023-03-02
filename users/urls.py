from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import LoginView, UserView

router = DefaultRouter()
router.register(r'', UserView, 'users')

urlpatterns = [
    path('login/', LoginView.as_view(), name="user_login"),
    path('users/', include(router.urls))
]
