from libs.serializers import DynamicFieldsModelSerializer
from captcha.models import Captcha


class CaptchaSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Captcha
        fields = ('id', 'question', 'image_path')
