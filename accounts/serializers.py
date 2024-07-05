from rest_framework import serializers
from .models import UserProfile, JobTitle, Department, Country, Governorate, City, DepartmentHistory, JobTitleHistory, SalaryHistory, Deduction

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class JobTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobTitle
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class GovernorateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Governorate
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class DepartmentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentHistory
        fields = '__all__'

class JobTitleHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobTitleHistory
        fields = '__all__'

class SalaryHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryHistory
        fields = '__all__'

class DeductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deduction
        fields = '__all__'