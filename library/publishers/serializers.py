from rest_framework import serializers

from publishers.models import Publisher


class PublisherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Publisher
        fields = ('id', 'name', 'email', 'website')
