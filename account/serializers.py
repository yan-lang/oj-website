from rest_framework import serializers

from account.models import User
from oj.models import Student


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class StudentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Student
        fields = ('user', 'student_id', 'name')

    def create(self, validated_data):
        student, created = Student.objects.update_or_create(
            user=validated_data.get('user', None),
            defaults={'student_id': validated_data.get('student_id', None),
                      'name': validated_data.get('name', None)})
        return student
