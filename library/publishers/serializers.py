from libs.serializers import DynamicFieldsModelSerializer
from publishers.models import Publisher


class PublisherSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Publisher
        fields = ('id', 'name', 'email', 'website')
