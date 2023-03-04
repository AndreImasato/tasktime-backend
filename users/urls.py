from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenVerifyView

from .views import LoginView, LoginWithTokenView, UserView

router = DefaultRouter()
router.register(r'', UserView, 'users')

urlpatterns = [
    path('login/', LoginView.as_view(), name="user_login"),
    path('users/', include(router.urls)),
    path('login-token/', LoginWithTokenView.as_view(), name="token_login"),
    path('verify-token/', TokenVerifyView.as_view(), name="token_verify"),
]
