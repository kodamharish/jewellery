from rest_framework import serializers
from .models import *


class SchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scheme
        fields = [
            'scheme_id',
            'scheme_name',
            'scheme_maturity_period',
            'scheme_benefit',
            'scheme_installment_amount',
        ]


class MemberSerializer(serializers.ModelSerializer):
    # Nested relationship to display the scheme details
    scheme = SchemeSerializer(read_only=True)
    scheme_id = serializers.PrimaryKeyRelatedField(
        queryset=Scheme.objects.all(),
        source='scheme',  # Maps to the ForeignKey field in the model
        write_only=True
    )

    class Meta:
        model = Member
        fields = [
            'id',
            'created_by',  # Ensure this is managed properly in the API views
            'name',
            'scheme',
            'scheme_id',  # Used for creating/updating the member
            'address',
            'city',
            'pin',
            'phone_number',
            'aadhaar',
            'pan',
            'email',
            'status',
            'join_date',
            'end_date',
            'nominee_name',
            'nominee_email',
            'nominee_phone_number',
            'nominee_aadhaar',
            'nominee_pan',
            'referred_person_name',
            'referred_person_id',
            'referred_person_referral_code',
            'member_referral_code',
            'referral_points',
            'total_paid_amount',
            'pending_amount',
            'paid_installments',
            'due_installments'
        ]
        read_only_fields = ['member_referral_code', 'referral_points']

    def validate_phone_number(self, value):
        """Validate the phone number to ensure it's valid."""
        if len(str(value)) != 10:
            raise serializers.ValidationError("Phone number must be 10 digits.")
        return value

    def validate_pin(self, value):
        """Validate the PIN code."""
        if len(value) < 6:
            raise serializers.ValidationError("PIN code must be at least 6 characters long.")
        return value

    def create(self, validated_data):
        """Custom create method to handle any additional logic."""
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Custom update method for additional logic if needed."""
        return super().update(instance, validated_data)




