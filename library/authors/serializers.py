from libs.serializers import DynamicFieldsModelSerializer
from authors.models import Author


class AuthorSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Author
        fields = ('id', 'first_name', 'last_name', 'email')
