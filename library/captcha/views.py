from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from rest_framework.decorators import detail_route, list_route

from libs.pagination import ResultSetPagination
from libs.utils import unblock_client

from captcha.models import Captcha
from captcha.serializers import CaptchaSerializer


class CaptchaViewSet(viewsets.ModelViewSet):
    queryset = Captcha.objects.all()
    serializer_class = CaptchaSerializer
    pagination_class = ResultSetPagination

    @list_route(methods=['GET'])
    def fetch_captcha(self, request):
        """
        returns a random captcha object from Captcha model.
        """
        captcha = Captcha.objects.filter().first()
        serializer = CaptchaSerializer(captcha)
        return Response(serializer.data)

    @detail_route(methods=['POST'])
    def validate_captcha(self, request, *args, **kwargs):
        """
        validates given answer to a captcha question againt a captcha ID.
        """
        captcha_id = self.kwargs['pk']
        payload = request.data

        try:
            captcha = Captcha.objects.get(id=captcha_id)
        except Captcha.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if payload:
            answer = payload.get('answer')
            is_valid_answer = captcha.answer == answer

            if is_valid_answer:
                # unblock client
                print unblock_client(request.client_indentity)

            return Response(
                {
                    "is_valid_answer": is_valid_answer,
                }
            )
        else:
            return Response(
                {
                    "error_msg": "Can't process this request with an empty payload."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
