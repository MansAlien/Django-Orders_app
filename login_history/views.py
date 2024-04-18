from django.http.response import HttpResponse
from .models import LoginHistory 
from accounts.models import UserProfile 
from django.shortcuts import render
from datetime import timedelta
from django.db.models import Sum
from django.db.models.functions import TruncDate



def login_time_test(request, pk):
    user_date = UserProfile.objects.get(id=pk)
    login_records= LoginHistory.objects.filter(user=pk)
    logout_records= LoginHistory.objects.filter(user=pk)
    context = {
            "login_records":login_records,
            "logout_records":logout_records,
    }
    return render(request, "login_time.html", context) 


def login_time(request, pk):
    user_date = UserProfile.objects.get(id=pk)
    # Fetch login and logout records ordered by timestamp
    login_records = LoginHistory.objects.filter(user=pk, is_login=True, is_logged_in=False).order_by('date_time')
    logout_records = LoginHistory.objects.filter(user=pk, is_login=False).order_by('date_time')
    
    # Combine login and logout records into a single list
    records = [[login, logout] for login, logout in zip(login_records, logout_records)]
    
    # Group records by day
    records_by_day = {}
    for record_pair in records:
        for record in record_pair:
            day = record.date_time.date()
            if day not in records_by_day:
                records_by_day[day] = []
            records_by_day[day].append(record)
    
    paired_records = []
    for day, day_records in records_by_day.items():
        # Calculate total duration for the day
        total_duration = timedelta()
        for i in range(0, len(day_records), 2):
            if i + 1 < len(day_records):
                diff = day_records[i + 1].date_time - day_records[i].date_time
                total_duration += diff
        hours = total_duration.seconds // 3600
        minutes = (total_duration.seconds % 3600) // 60
        paired_records.append((day, hours, minutes))
    
    context = {
        "paired_records": paired_records,
    }
    return render(request, "settings/employee/tables/login_time.html", context)
