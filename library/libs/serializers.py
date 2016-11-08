from rest_framework import serializers


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    '''
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    '''

    def __init__(self, *args, **kwargs):
        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        # initialize fields as empty tuple
        fields = ()
        if self.context and self.context.get('request'):
            fields = self.context['request'].query_params.get('fields')
        if fields:
            fields = fields.split(',')
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            not_to_display = existing - allowed

            if not_to_display != existing:
                for field_name in not_to_display:
                    self.fields.pop(field_name)