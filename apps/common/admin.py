from django.contrib import admin
from .models import Sponsor, StudentSponsor, Student, University


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'student_type', 'university', 'contract_amount']
    list_filter = ['student_type', ]
    search_fields = ['full_name', 'university']


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone_number', 'amount', 'created_at', 'status']
    list_filter = ['status',]
    search_fields = ['full_name', 'organization']


@admin.register(StudentSponsor)
class StudentSponsorAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'sponsor', 'amount', 'created_at']
    search_fields = ['student', 'sponsor']


admin.site.register(University)
