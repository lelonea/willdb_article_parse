from rest_framework import serializers


class RequestSerializer(serializers.Serializer):
    article = serializers.CharField(required=False)
    file = serializers.FileField(required=False)

    def validate(self, data):
        if data.get('article') and data.get('file'):
            raise serializers.ValidationError('You can send only one parameter')
        elif not data.get('article') and not data.get('file'):
            raise serializers.ValidationError('You must send one parameter')
        elif data.get('article'):
            if not data.get('article').isdigit():
                raise serializers.ValidationError('Article must be a number')
        elif data.get('file'):
            if not data.get('file').name.endswith('.xlsx'):
                raise serializers.ValidationError('File must be xlsx')
        return data


