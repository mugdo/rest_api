from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from dataservice.serializers import  TeacherSerializer

from dataservice.models import Teacher

# Create your views here.
class TeacherView(APIView):
    def get(self, request):
        serializer = TeacherSerializer(Teacher.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)