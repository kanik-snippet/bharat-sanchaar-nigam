from django.db.models import Q
from django.core.mail import send_mass_mail
from .models import User, Notification
import logging
def assign_news_location(user):
    """Strict role-based location assignment"""
    location_data = {
        'is_public': True,
        'country': user.assigned_country if user.role == 'pm' else None,
        'state': user.assigned_state if user.role == 'cm' else None,
        'district': user.assigned_district if user.role == 'vidhayak' else None,
        'city_village': (user.assigned_city or user.assigned_village) 
                       if user.role in ['chairman', 'sarpanch'] else None,
        'ward': user.assigned_ward if user.role == 'sabhasad' else None
    }
    return {k: v for k, v in location_data.items() if v}

from django.db.models import Q

def get_users_to_notify(news):
    """
    Returns users to notify including janta based on hierarchy:
    - PM: All users in country (through city/village/ward) + all officials
    - CM: All users in state (through city/village/ward) + state officials
    - Vidhayak: All users in district (through city/village/ward) + district officials
    - Chairman/Sarpanch: All users in city/village + officials
    - Sabhasad: All users in ward + officials
    """
    creator = news.created_by
    base_query = User.objects.filter(is_active=True).exclude(id=creator.id)
    
    if creator.role == 'pm':
        # All users in country (through their city/village/ward's district->state->country)
        # Plus all officials nationwide
        country = creator.governing_country
        return base_query.filter(
            Q(assigned_city__district__state__country=country) |
            Q(assigned_village__district__state__country=country) |
            Q(assigned_ward__city_village__district__state__country=country) |
            Q(role__in=['cm', 'vidhayak', 'chairman', 'sarpanch', 'sabhasad'])
        )
    
    elif creator.role == 'cm':
        # All users in state (through their city/village/ward's district->state)
        # Plus state officials
        state = creator.governing_state
        return base_query.filter(
            Q(assigned_city__district__state=state) |
            Q(assigned_village__district__state=state) |
            Q(assigned_ward__city_village__district__state=state) |
            Q(role='cm', governing_state__isnull=False) |  # All CMs
            Q(role__in=['vidhayak', 'chairman', 'sarpanch', 'sabhasad'],
              governing_district__state=state)
        )
    
    elif creator.role == 'vidhayak':
        # All users in district (through their city/village/ward)
        # Plus district officials
        district = creator.governing_district
        return base_query.filter(
            Q(assigned_city__district=district) |
            Q(assigned_village__district=district) |
            Q(assigned_ward__city_village__district=district) |
            Q(role='vidhayak', governing_district__isnull=False) |  # All vidhayaks in district
            Q(role__in=['chairman', 'sarpanch', 'sabhasad']) &
            (Q(governing_city__district=district) |
             Q(governing_village__district=district) |
             Q(governing_ward__city_village__district=district))
        )
    
    elif creator.role == 'chairman':
        # All users in city + officials
        city = creator.governing_city
        return base_query.filter(
            Q(assigned_city=city) |
            Q(assigned_ward__city_village=city) |
            Q(role='chairman', governing_city__isnull=False) |  # All chairmen
            Q(role='sabhasad', governing_ward__city_village=city)
        )
    
    elif creator.role == 'sarpanch':
        # All users in village + officials
        village = creator.governing_village
        return base_query.filter(
            Q(assigned_village=village) |
            Q(assigned_ward__city_village=village) |
            Q(role='sarpanch', governing_village__isnull=False) |  # All sarpanches
            Q(role='sabhasad', governing_ward__city_village=village)
        )
    
    elif creator.role == 'sabhasad':
        # All users in ward + officials
        ward = creator.governing_ward
        return base_query.filter(
            Q(assigned_ward=ward) |
            Q(role='sabhasad', governing_ward=ward)
        )
    
    return User.objects.none()

def notify_users(news):
    try:
        recipients = get_users_to_notify(news)
        
        # Create notifications
        Notification.objects.bulk_create([
            Notification(
                user=user,
                message=f"{news.created_by.get_role_display()} Update: {news.content[:200]}"
            ) for user in recipients
        ], batch_size=1000)
        
        # Send emails
        email_recipients = recipients.filter(email__isnull=False)
        if email_recipients.exists():
            send_mass_mail([
                (f"New {news.created_by.get_role_display()} Update",
                 news.content,
                 'notifications@gov.in',
                 [user.email]) 
                for user in email_recipients
            ], fail_silently=True)
            
    except Exception as e:
        print(f"Error sending notifications: {e}")