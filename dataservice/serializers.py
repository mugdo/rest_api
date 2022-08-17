from rest_framework import serializers
from .models import Course, Student, Teacher

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['course'] = CourseSerializer(Course.objects.filter(enrollment__student__id=instance.id), many=True).data
        return ret

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'