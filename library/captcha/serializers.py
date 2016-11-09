from rest_framework import serializers

from libs.serializers import DynamicFieldsModelSerializer
from captcha.models import Captcha


class CaptchaSerializer(DynamicFieldsModelSerializer):
    message = serializers.SerializerMethodField()

    class Meta:
        model = Captcha
        fields = ('id', 'question', 'image_path', 'message')

    def get_message(self, instance):
        """
        returns a text string as instruction to solve CAPTCHA to get unblocked.
        """
        return (
            "To make CAPTCHA free API calls, Make a POST "
            "request to /captcha/<id>/validate_captcha/ "
            "with an answer in payload to given question "
            "in this CAPTCHA."
        )
