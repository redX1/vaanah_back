from rest_framework import fields, serializers
from .models import PaymentModel

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentModel
        fields = [
            "id",
            "order_number",
            "method",
            "amount",
            "currency",
            "created_at"
        ]