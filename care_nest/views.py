from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from django.shortcuts import get_object_or_404
from django.contrib.auth.password_validation import validate_password
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

from .models import Child, ChildAchievements, Attendance, Section
from .serializers import (
    ChildSerializer, 
    ChildAchievementsSerializer, 
    AttendanceSerializer, 
    SectionSerializer
    )

# Create your views here.

# ------ Child Model ----------#

class ChildListCreateView(APIView):
    
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        if request.user.is_superuser:
            child = Child.objects.all()
        else:
            child = Child.objects.filter(owner=request.user)
        serializer = ChildSerializer(child, many=True, context={'request': request})
        return Response(serializer.data, status=200)
    
    def post(self, request):
        if not (request.user.is_superuser):
            raise PermissionDenied('Sorry, you dont have the permission to add a child')
        serializer = ChildSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
# ------ Child Model ----------#

class ChildDetailView(APIView):
    
    permission_classes = [IsAuthenticated]  

    def get_object(self, pk):
        return get_object_or_404(Child, pk=pk)
    
    def get(self, request, pk):
        child = self.get_object(pk)
        if not (request.user.is_superuser or child.owner == request.user):
            raise PermissionDenied('Sorry, you dont have the permission to get this child')
        serializer = ChildSerializer(child)
        return Response(serializer.data, status=200)
    
    def patch(self, request, pk):
        child = self.get_object(pk)
        if not (request.user.is_superuser):
            raise PermissionDenied('Sorry, you dont have the permission to update this child')
        serializer = ChildSerializer(child, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk):
        child = self.get_object(pk)
        if not (request.user.is_superuser):
            raise PermissionDenied('Sorry, you dont have the permission to delete this child')
        child.delete()
        return Response(status=204)

# ------ Child Model ----------#

class ChildrenBySectionView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request, section_id):
        children = Child.objects.filter(section_id=section_id)
        serializer = ChildSerializer(children, many=True)
        return Response(serializer.data, status=200)

# ------ Child Achivements Model ----------#

class ChildAchievementsListCreateView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        achievements = ChildAchievements.objects.all()
        serializer = ChildAchievementsSerializer(achievements, many=True)
        return Response(serializer.data, status=200)
    
    def post(self, request):
        if not (request.user.is_superuser):
            raise PermissionDenied('Sorry, you dont have the permission to add an achievement')
        serializer = ChildAchievementsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
# ------ Child Achivements Model ----------#

class ChildAchievementsByChildView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        return get_object_or_404(Child, pk=pk)
    
    def get(self, request, pk):
        child = self.get_object(pk)
        if not (request.user.is_superuser or child.owner == request.user):
            raise PermissionDenied("Sorry, you dont have the permission to view this child achievements")
        achievements = ChildAchievements.objects.filter(child=child)
        serializer = ChildAchievementsSerializer(achievements, many=True)
        return Response(serializer.data, status=200)
    
class AchievementsBySectionView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request, section_id):
        achievements = ChildAchievements.objects.filter(child__section_id=section_id)
        serializer = ChildAchievementsSerializer(achievements, many=True)
        return Response(serializer.data, status=200)
    
# ------ Child Achivements Model ----------#
    
class ChildAchievementsDetailView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(ChildAchievements, pk=pk)
    
    def get(self, request, pk):
        achievements = self.get_object(pk)
        serializer = ChildAchievementsSerializer(achievements)
        return Response(serializer.data, status=200)
    
    def patch(self, request, pk):
        achievements = self.get_object(pk)
        if not (request.user.is_superuser):
            raise PermissionDenied('Sorry, you dont have the permission to edit an achievement')
        serializer = ChildAchievementsSerializer(achievements, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk):
        achievements = self.get_object(pk)
        if not (request.user.is_superuser):
            raise PermissionDenied('Sorry, you dont have the permission to delete an achievement')
        achievements.delete()
        return Response(status=204)

# ------ Attendance Model ----------#

class AttendanceListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_superuser:
            records = Attendance.objects.all()
        else:
            records = Attendance.objects.filter(child__owner=request.user)
        serializer = AttendanceSerializer(records, many=True)
        return Response(serializer.data, status=200)
    
class AttendanceCreateView(APIView): 
    
    permission_classes = [IsAuthenticated]

    def get(self, request, section_id):
        records = Attendance.objects.filter(child__section_id=section_id)
        serializer = AttendanceSerializer(records, many=True)
        return Response(serializer.data, status=200)
    
    def post(self, request, section_id):
        if not (request.user.is_superuser):
            raise PermissionDenied('Sorry, you dont have the permission to add an attendance')
        serializer = AttendanceSerializer(data=request.data,  many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# ------ Attendance Model ----------#

class AttendanceDetailView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Attendance, pk=pk)
    
    def get(self, request, pk):
        record = self.get_object(pk)
        serializer = AttendanceSerializer(record)
        return Response(serializer.data, status=200)
    
    def patch(self, request, pk):
        record = self.get_object(pk)
        if not (request.user.is_superuser):
            raise PermissionDenied('Sorry, you dont have the permission to edit an attendance')
        serializer = AttendanceSerializer(record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
# ------ Attendance Model ----------#

class AttendanceBySectionView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, section_id):
            if request.user.is_superuser:
                records = Attendance.objects.filter(child__section__id=section_id)
            else:
                records = Attendance.objects.filter(child__owner=request.user)
            serializer = AttendanceSerializer(records, many=True)
            return Response(serializer.data, status=200)

# ------ sections Model ----------#

class SectionListView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        section = Section.objects.all()
        serializer = SectionSerializer(section, many=True)
        return Response(serializer.data, status=200)
    
#------------- Signup --------------#

class SignUpView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            validate_password(password)
        except ValidationError as err:
            return Response({'error': err.messages}, status=400)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        tokens = RefreshToken.for_user(user)
        return Response(
            {
                'refresh': str(tokens),
                'access': str(tokens.access_token)
            },
            status=201
        )

@api_view(['GET']) #https://www.django-rest-framework.org/api-guide/views/#api_view: to convert the ffunction into API view
@permission_classes([IsAuthenticated])
def this_user_details(request):

    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_superuser': user.is_superuser,
        'is_staff': user.is_staff
    })
    
@api_view(['GET']) 
@permission_classes([IsAuthenticated])
def all_parents(request):
    parents = User.objects.filter(is_superuser=False)
    parent_data = []
    for parent in parents:
        parent_data.append({
            'id': parent.id,
            'username': parent.username
        })
    return Response(parent_data)



