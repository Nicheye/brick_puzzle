from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q
from rest_framework.permissions import IsAuthenticated

from prompts.models import Prompt, Style, Color
from authentification.models import User
from authentification.serializers import LeaderboardSerializer
from prompts.serializers import PromptSerializer
from prompts.tasks import generate_image
from backendmusic import settings


class MainView(APIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'request': self.request
        })
        return context

    def get(self, request):
        user = request.user
        queryset = Prompt.objects.all()
        ser = PromptSerializer(queryset, many=True)
        message = 'authenticate please'
        can_add = False
        if user.is_authenticated:
            message = 'generate your image'
            can_add = user.can_add
            prompt = Prompt.objects.filter(created_by=user)
            if prompt.count() == 1:
                prompt = prompt.first()
                if prompt.is_approved:
                    message = f'your brick is #{prompt.position}'
                else:
                    message = 'wait for improvement of your image :)'
            elif prompt.count() > 0:
                ids = ' '.join([f'#{prom.position}' for prom in prompt])
                message = f'your bricks are on {ids} positions'

        return Response({'message': message, 'images': ser.data, 'can_add': can_add}, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        user = request.user

        if user.is_authenticated:
            if not user.can_add:
                return Response(
                    {'message': 'You have already done your contribution'},
                    status=status.HTTP_403_FORBIDDEN
                )
            else:
                ser = PromptSerializer(data=data, context={'request': request})
                ser.is_valid(raise_exception=True)

                style = Style.objects.filter(style=data['style']).first()
                color = Color.objects.filter(color=data['color']).first()
                ser.save(style=style, color=color, created_by=user)

                task = generate_image.delay(data['prompt'], data['style'], data['color'], user.id)
                print(task)

                user.can_add = False
                user.save()

                promps_count = Prompt.objects.filter(created_by=user).count()
                return Response(
                    {'message': f'Generate your image {promps_count}'},
                    status=status.HTTP_201_CREATED
                )

        return Response({'message': 'Authorize please'}, status=status.HTTP_401_UNAUTHORIZED)


class ShareView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user.can_add = True
        user.save()
        return Response({'message': 'thank you for sharing'}, status=status.HTTP_200_OK)


class CommonPicView(APIView):
    def get(self, request):
        common_picture = f"{settings.BASE_URL}media/media/images/common_pic.png"
        grid = f"{settings.BASE_URL}media/media/images/grid.jpg"
        user = request.user

        your_images = ''
        if user.is_authenticated:
            your_images = Prompt.objects.filter(created_by=request.user)
        print(your_images)
        leaderboard = User.objects.annotate(
            prompt_count=Count('prompt__id', filter=Q(prompt__is_approved=True))
        ).filter(
            prompt_count__gt=1  # Only include users with more than one approved prompt
        ).order_by('-prompt_count')
        leaderboard_ser = LeaderboardSerializer(leaderboard, many=True)
        return Response(
            {
                'common_pic': common_picture,
                'grid': grid,
                'your_images': PromptSerializer(your_images, many=True).data,
                'leaderboard': leaderboard_ser.data
            },
            status=status.HTTP_200_OK
        )
