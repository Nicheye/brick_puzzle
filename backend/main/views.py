from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from authentification.models import User
from authentification.serializers import UserSerializer
from main.models import Invitation
from main.helpers import parse_date_string, parse_ff_ls
from main.serializers import InvitationSerializer, PaymentSerializer


class InvitationView(APIView):

    def get(self, request):
        try:
            user = request.user
            reffer = request.query_params.get('ref', None)  # Assuming 'ref' refers to some external identifier
            invite_slug = request.query_params.get('id', None)
            print(reffer, invite_slug, user.is_authenticated)

            if user.is_authenticated and reffer is None and invite_slug is None:
                # Correct the attribute name to 'refferer'
                invitation_obj = Invitation.objects.create(refferer=user)
                invitation_ser = InvitationSerializer(invitation_obj)
                return Response(invitation_ser.data, status=status.HTTP_201_CREATED)

            elif user.is_authenticated and (reffer or invite_slug):
                return Response({'message': 'You already registered'}, status=status.HTTP_403_FORBIDDEN)

            elif reffer or invite_slug:
                return Response({'message': 'You need to do a POST request to register'}, status=status.HTTP_403_FORBIDDEN)

            return Response({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        user = request.user
        reffer = request.query_params.get('ref', None)
        invite_slug = request.query_params.get('id', None)

        if user.is_authenticated:
            return Response({'message': 'You already registered'}, status=status.HTTP_303_SEE_OTHER)

        if reffer and invite_slug:
            invite_obj = Invitation.objects.filter(slug=invite_slug).first()
            refferer_obj = User.objects.filter(id=reffer).first()

            if invite_obj and refferer_obj and not invite_obj.is_used:
                data = request.data
                user_serializer = UserSerializer(data=data)
                user_serializer.is_valid(raise_exception=True)
                new_user = user_serializer.save(grade_level='ST')
                invite_obj.is_used = True
                invite_obj.to = new_user
                invite_obj.save()
                return Response(user_serializer.data, status=status.HTTP_201_CREATED)

            return Response({'message': 'No such invitation or it has already been used'}, status=status.HTTP_403_FORBIDDEN)

        return Response({'message': 'You have not provided refferer or id or both'}, status=status.HTTP_303_SEE_OTHER)


"""
Принимает 
card: str
cvv: int
valid_until: str -> mm/dd
card_owner: str
"""


class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data
        try:
            data['first_four'], data['last_six'] = parse_ff_ls(data['card'])
            data.pop('card')
            data['valid_until'] = parse_date_string(data['valid_until'])
            payment_ser = PaymentSerializer(data=data)
            payment_ser.is_valid(raise_exception=True)
            payment_ser.save(user=user)
            invite_find = Invitation.objects.filter(to=user)
            msg = ''
            if invite_find.count() > 0:
                invite_find = invite_find.first()
                invite_find.to.lessons += 4
                invite_find.refferer.lessons += 4
                invite_find.to.save()
                invite_find.refferer.save()
                msg = 'As you were invited by link you and your refferer got 4 more free lessons'
            return Response({'data': payment_ser.data, 'message': msg}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        invitations = Invitation.objects.all()
        total_invitations = invitations.count()
        total_used = invitations.filter(is_used=True).count()
        total_with_payment_info = sum(1 for invitation in invitations if invitation.has_payment_info())

        stats = {
            'total_invitations': total_invitations,
            'total_used': total_used,
            'total_with_payment_info': total_with_payment_info,
            'total_without_payment_info': total_used - total_with_payment_info
        }
        return Response(stats, status=status.HTTP_200_OK)
