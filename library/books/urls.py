from rest_framework import routers

from books import views

router = routers.SimpleRouter()

router.register(r'books', views.BookViewSet)

urlpatterns = router.urls
