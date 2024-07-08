from django.db.models import Sum
from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework import serializers
from .models import Sponsor, Student, StudentSponsor, University


class SponsorSerializer(ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ['person_type', 'full_name', 'phone_number', 'amount', 'organization', 'payment_type']

    def validate(self, data):
        if data['person_type'] == 'legal_entity' and not data.get('organization'):
            raise ValidationError(detail={'error': "Organization is required for legal entities."})
        elif data['person_type'] == 'simple_person' and data.get('organization'):
            raise ValidationError(detail={'error': "Organization is not required for simple person"})
        return super().validate(data)


class SponsorListSerializer(serializers.ModelSerializer):
    spent_money = serializers.SerializerMethodField()

    class Meta:
        model = Sponsor
        fields = ['id', 'full_name', 'phone_number', 'amount', 'spent_money', 'created_at', 'status']

    def get_spent_money(self, obj):
        return obj.student_sponsors.aggregate(spent_money=Sum('amount'))['spent_money'] or 0


class SponsorStudentSerializer(serializers.ModelSerializer):
    sponsor_name = serializers.CharField(source='sponsor.full_name')

    class Meta:
        model = StudentSponsor
        fields = ['id', 'sponsor_name', 'amount']


class StudentDetailSerializer(serializers.ModelSerializer):
    university = serializers.CharField(source="university.name")
    sponsors = SponsorStudentSerializer(source='student_sponsors', many=True)
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'full_name', 'phone_number', 'university', 'student_type', 'total_amount', 'contract_amount', 'sponsors']

    def get_total_amount(self, obj):
        return obj.student_sponsors.aggregate(total_amount=Sum('amount'))['total_amount'] or 0


class StudentSerializer(ModelSerializer):
    university = serializers.CharField(source="university.name")
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'full_name', 'student_type', 'university', 'total_amount', 'contract_amount',]

    def get_total_amount(self, obj):
        return obj.student_sponsors.aggregate(total_amount=Sum('amount'))['total_amount'] or 0


class StudentUpdateSerializer(serializers.ModelSerializer):
    university = serializers.CharField(write_only=True)

    class Meta:
        model = Student
        fields = ['id', 'full_name', 'phone_number', 'university', 'student_type', 'contract_amount']

    def update(self, instance, validated_data):
        university_name = validated_data.pop('university', None)
        if university_name:
            try:
                university = University.objects.get(name=university_name)
                instance.university = university
            except University.DoesNotExist:
                raise serializers.ValidationError({'university': 'University does not exist'})
        return super().update(instance, validated_data)


class StudentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = "__all__"


class SponsorUpdateSerializer(ModelSerializer):

    class Meta:
        model = Sponsor
        fields = ['id', 'person_type', 'full_name', 'phone_number', 'status',
                  'amount', 'organization', 'payment_type']

    def validate(self, data):
        if data['person_type'] == 'legal_entity' and not data.get('organization'):
            raise ValidationError(detail={'error': "Organization is required for legal entities."})
        elif data['person_type'] == 'simple_person' and data.get('organization'):
            raise ValidationError(detail={'error': "Organization is not required for simple person"})
        return super().validate(data)


class SponsorDetailSerializer(ModelSerializer):

    class Meta:
        model = Sponsor
        fields = ['id', 'full_name', 'phone_number', 'status', 'amount', 'organization']


class StudentSponsorAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentSponsor
        fields = ['id', 'student', 'sponsor', 'amount']

    def validate(self, data):
        sponsor = data['sponsor']
        student = data['student']
        amount = data['amount']

        spent_money = sponsor.student_sponsors.aggregate(spent_money=Sum('amount'))['spent_money'] or 0
        total_amount = student.student_sponsors.aggregate(total_amount=Sum('amount'))['total_amount'] or 0

        if sponsor.amount - spent_money < amount:
            raise serializers.ValidationError(
                {'error': "The sponsor's remaining amount is less than the provided amount."}
            )

        if student.contract_amount - total_amount < amount:
            raise serializers.ValidationError(
                {'error': "The student's contract remaining amount is less than the provided amount."}
            )

        return super().validate(data)


class StudentSponsorUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentSponsor
        fields = ['sponsor', 'amount',]

    def validate(self, data):
        instance = self.instance
        sponsor = data.get('sponsor', instance.sponsor)
        amount = data.get('amount', instance.amount)
        student = data.get('student', instance.student)

        if sponsor != instance.sponsor:
            spent_money = sponsor.student_sponsors.aggregate(spent_money=Sum('amount'))['spent_money'] or 0
            if sponsor.amount - spent_money < amount:
                raise serializers.ValidationError(
                    {'error': "The new sponsor's remaining amount is less than the provided amount."}
                )
        else:
            spent_money = sponsor.student_sponsors.exclude(id=instance.id).aggregate(spent_money=Sum('amount'))['spent_money'] or 0
            if sponsor.amount - spent_money < amount:
                raise serializers.ValidationError(
                    {'error': "The sponsor's remaining amount is less than the provided amount."}
                )

        if amount != instance.amount:
            total_amount = student.student_sponsors.exclude(id=instance.id).aggregate(total_amount=Sum('amount'))['total_amount'] or 0
            if student.contract_amount - total_amount < amount:
                raise serializers.ValidationError(
                    {'error': "The student's contract remaining amount is less than the provided amount."})

        return super().validate(data)


class StudentSponsorDetailSerializer(ModelSerializer):
    student = serializers.CharField(source='student.full_name')
    sponsor = serializers.CharField(source='sponsor.full_name')

    class Meta:
        model = StudentSponsor
        fields = ['student', 'sponsor', 'amount']










