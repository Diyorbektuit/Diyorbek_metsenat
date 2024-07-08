from django_filters.rest_framework import DjangoFilterBackend
from .models import Sponsor, Student, StudentSponsor
from rest_framework.filters import SearchFilter
from rest_framework import generics
from . import serializers


class SponsorPostView(generics.CreateAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = serializers.SponsorSerializer


class StudentList(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = serializers.StudentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['university', 'student_type']
    search_fields = ['full_name']


class SponsorList(generics.ListAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = serializers.SponsorListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['status',]
    search_fields = ['full_name']


class StudentDetailUpdate(generics.RetrieveUpdateAPIView):
    queryset = Student.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.StudentDetailSerializer
        elif self.request.method == 'PUT' or 'PATCH':
            return serializers.StudentUpdateSerializer


class SponsorDeleteView(generics.DestroyAPIView):
    queryset = Sponsor.objects.all()


class SponsorDetailUpdate(generics.RetrieveUpdateAPIView):
    queryset = Sponsor.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.SponsorDetailSerializer
        elif self.request.method == 'PUT' or 'PATCH':
            return serializers.SponsorUpdateSerializer


class StudentCreateView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = serializers.StudentCreateSerializer


class StudentDeleteView(generics.DestroyAPIView):
    queryset = Student.objects.all()


class StudentSponsorAddView(generics.CreateAPIView):
    queryset = StudentSponsor.objects.all()
    serializer_class = serializers.StudentSponsorAddSerializer


class StudentSponsorUpdateView(generics.RetrieveUpdateAPIView):
    queryset = StudentSponsor.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.StudentSponsorDetailSerializer
        elif self.request.method == 'PUT' or 'PATCH':
            return serializers.StudentSponsorUpdateSerializer

