from django import template
from datetime import datetime, timedelta

register = template.Library()

@register.filter
def add_days(value, days):
    try:
        days = int(days)
    except (ValueError, TypeError):
        return value
    
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return value
    
    if isinstance(value, datetime):
        return value + timedelta(days=days)
    return value
