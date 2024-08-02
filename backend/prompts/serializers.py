from prompts.models import Prompt

from rest_framework.serializers import SerializerMethodField, ModelSerializer, ValidationError

from profanity_check import predict


class PromptSerializer(ModelSerializer):
    created_by = SerializerMethodField()
    class Meta:
        model = Prompt
        fields = ['prompt', 'style', 'color', 'position', 'is_approved', 'created_by', 'created_at']

    def get_created_by(self, obj):
        return obj.created_by.username

    def validate_prompt(self, value):
        if predict([value])[0]:
            raise ValidationError('This field contains inappropriate language.')
        return value