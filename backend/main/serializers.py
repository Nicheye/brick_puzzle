from rest_framework import serializers
from main.models import Invitation, PaymentInfo
from backendmusic.settings import BASE_URL


class InvitationSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()

    class Meta:
        model = Invitation
        fields = ['link']

    def get_link(self, obj):
        return f'{BASE_URL}api/payment/?ref={obj.refferer.id}&id={obj.slug}'


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentInfo
        fields = ['first_four', 'last_six', 'cvv',
                  'card_owner', 'user', 'valid_until']
