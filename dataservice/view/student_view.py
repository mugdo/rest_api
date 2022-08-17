from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from dataservice.serializers import StudentSerializer

from dataservice.models import Student

# Create your views here.
class StudentView(APIView):
    def get(self, request):
        serializer = StudentSerializer(Student.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)