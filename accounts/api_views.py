from .models import UserProfile, JobTitle, Department, Country, Governorate, City, DepartmentHistory, JobTitleHistory, SalaryHistory, Deduction
from .serializers import UserProfileSerializer, JobTitleSerializer, DepartmentSerializer, CountrySerializer, GovernorateSerializer, CitySerializer, DepartmentHistorySerializer, JobTitleHistorySerializer, SalaryHistorySerializer, DeductionSerializer
from rest_framework import viewsets


##########################################################
#######                APIS                ###############
##########################################################
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class JobTitleViewSet(viewsets.ModelViewSet):
    queryset = JobTitle.objects.all()
    serializer_class = JobTitleSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class GovernorateViewSet(viewsets.ModelViewSet):
    queryset = Governorate.objects.all()
    serializer_class = GovernorateSerializer

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

class DepartmentHistoryViewSet(viewsets.ModelViewSet):
    queryset = DepartmentHistory.objects.all()
    serializer_class = DepartmentHistorySerializer

class JobTitleHistoryViewSet(viewsets.ModelViewSet):
    queryset = JobTitleHistory.objects.all()
    serializer_class = JobTitleHistorySerializer

class SalaryHistoryViewSet(viewsets.ModelViewSet):
    queryset = SalaryHistory.objects.all()
    serializer_class = SalaryHistorySerializer

class DeductionViewSet(viewsets.ModelViewSet):
    queryset = Deduction.objects.all()
    serializer_class = DeductionSerializer
