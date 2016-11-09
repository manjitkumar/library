
from rest_framework import viewsets

from libs.pagination import ResultSetPagination

from captcha.models import Captcha
from captcha.serializers import CaptchaSerializer


class CaptchaViewSet(viewsets.ModelViewSet):
    queryset = Captcha.objects.all()
    serializer_class = CaptchaSerializer
    pagination_class = ResultSetPagination
