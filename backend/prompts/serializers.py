from prompts.models import Prompt
from rest_framework.serializers import SerializerMethodField, ModelSerializer


class PromptSerializer(ModelSerializer):
    created_by = SerializerMethodField()
    class Meta:
        model = Prompt
        fields = ['prompt', 'style', 'color', 'position', 'is_approved', 'created_by', 'created_at']

    def get_created_by(self, obj):
        return obj.created_by.username