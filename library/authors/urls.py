from rest_framework import routers

from authors import views

router = routers.SimpleRouter()

router.register(r'authors', views.AuthorViewSet)

urlpatterns = router.urls
