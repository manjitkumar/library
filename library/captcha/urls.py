from rest_framework import routers

from captcha import views

router = routers.SimpleRouter()

router.register(r'captcha', views.CaptchaViewSet)

urlpatterns = router.urls
