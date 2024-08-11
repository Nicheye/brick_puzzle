from prompts.models import Prompt

from rest_framework.serializers import SerializerMethodField, ModelSerializer

from backendmusic.settings import MEDIA_URL

class PromptSerializer(ModelSerializer):
    created_by = SerializerMethodField()
    image = SerializerMethodField()
    style = SerializerMethodField()
    color = SerializerMethodField()

    class Meta:
        model = Prompt
        fields = ['prompt', 'style', 'color', 'position', 'is_approved', 'created_by', 'created_at', 'image']

    def get_created_by(self, obj):
        return obj.created_by.username

    def get_image(self, obj):
        if obj.image:
            return f'{MEDIA_URL}images/{obj.created_by.id}.jpg'
        return None

    def get_style(self, obj):
        if obj.style:
            return obj.style.style

    def get_color(self, obj):
        if obj.color:
            return obj.color.color
