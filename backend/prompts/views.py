from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from prompts.models import Prompt
from prompts.serializers import PromptSerializer

from prompts.tasks import generate_image


class MainView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get(self, request):
        user = request.user
        queryset = Prompt.objects.all()
        ser = PromptSerializer(queryset, many=True)
        message = 'authenticate please'
        if user.is_authenticated:
            prompt = Prompt.objects.filter(created_by=user)
            if prompt.count() > 0:
                prompt = prompt.first()
                if prompt.is_approved:
                    message = f'your brick is #{prompt.position}'
                message = 'wait for improvement of your image :)'
            message = 'generate your image'
        return Response({'message': message, 'images': ser.data})

    def post(self, request):
        data = request.data
        user = request.user
        if user.is_authenticated:
            prompt = Prompt.objects.filter(created_by=user)
            if prompt.count() > 0:
                return Response({'message': 'you have already done your contribution'})
            ser = PromptSerializer(data=data)
            if ser.is_valid(raise_exception=True):
                ser.save()
                task = generate_image.delay(ser['prompt'], ser['style'], ser['color'], user)

            return Response({'message': 'generate your image'})
        return Response({'message': 'Authorize please'})