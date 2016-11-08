from rest_framework import routers

from publishers import views

router = routers.SimpleRouter()

router.register(r'publishers', views.PublisherViewSet)

urlpatterns = router.urls
