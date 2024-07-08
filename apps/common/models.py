from django.db import models
from .regx import validate_uzbekistan_phone_number


class BaseModel(models.Model):
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class University(BaseModel):
    name = models.CharField(max_length=123)

    def __str__(self):
        return self.name


class Student(BaseModel):
    StudentType = (
        ('bakalavr', 'Bakalavr'),
        ('master', 'Magistr'),
    )
    full_name = models.CharField(max_length=123)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='students')
    phone_number = models.CharField(max_length=20, validators=[validate_uzbekistan_phone_number])
    student_type = models.CharField(choices=StudentType, max_length=20)
    contract_amount = models.IntegerField()

    def __str__(self):
        return self.full_name


class Sponsor(BaseModel):
    PAYMENT_TYPE_CHOICES = (
        ('money_transfers', "pul o'tkazmalari"),
        ('cash', 'naqt pul orqali')
    )
    PERSON_TYPE_CHOICES = (
        ('legal_entity', 'yuridik shaxs'),
        ('simple_person', 'Jismoniy shaxs'),
    )
    STATUS_CHOICES = (
        ('new', 'Yangi'),
        ('moderation', 'Moderatsiyada'),
        ('approved', 'Tasdiqlangan'),
        ('cancelled', 'Bekor qilingan'),
    )
    full_name = models.CharField(max_length=123)
    person_type = models.CharField(choices=PERSON_TYPE_CHOICES, max_length=20)
    phone_number = models.CharField(max_length=20, validators=[validate_uzbekistan_phone_number])
    amount = models.IntegerField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default='new')
    organization = models.CharField(max_length=123, null=True, blank=True)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES, default='money_transfers')

    def __str__(self):
        return self.full_name


class StudentSponsor(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name='student_sponsors')
    sponsor = models.ForeignKey(Sponsor, on_delete=models.PROTECT, related_name='student_sponsors')
    amount = models.IntegerField()

    def __str__(self):
        return f"{self.sponsor}ning {self.student}ga homiyligi"




