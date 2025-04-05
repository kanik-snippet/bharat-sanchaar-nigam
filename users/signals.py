from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import User
from news.models import Ward, District, CityVillage

@receiver(pre_save, sender=User)
def handle_role_change(sender, instance, **kwargs):
    try:
        old_instance = User.objects.get(id=instance.id)
    except User.DoesNotExist:
        return  # New user, no role change to handle
    
    # Check if role changed
    if old_instance.role != instance.role:
        # Clear previous assignments based on old role
        if old_instance.role == 'sabhasad':
            if old_instance.assigned_ward:
                ward = old_instance.assigned_ward
                ward.sabhasad = None
                ward.status = Ward.INACTIVE
                ward.save()
            instance.assigned_ward = None
            
        elif old_instance.role == 'vidhayak':
            if old_instance.assigned_district:
                district = old_instance.assigned_district
                district.vidhayak = None
                district.status = District.INACTIVE
                district.save()
            instance.assigned_district = None
            
        elif old_instance.role == 'chairman':
            if old_instance.assigned_city:
                city = old_instance.assigned_city
                city.chairman = None
                city.status = CityVillage.INACTIVE
                city.save()
            instance.assigned_city = None
            
        elif old_instance.role == 'sarpanch':
            if old_instance.assigned_village:
                village = old_instance.assigned_village
                village.sarpanch = None
                village.status = CityVillage.INACTIVE
                village.save()
            instance.assigned_village = None

    # Update new assignments based on current role
    if instance.role == 'sabhasad' and instance.assigned_ward:
        instance.assigned_ward.sabhasad = instance
        instance.assigned_ward.status = Ward.ACTIVE
        instance.assigned_ward.save()
        
    elif instance.role == 'vidhayak' and instance.assigned_district:
        instance.assigned_district.vidhayak = instance
        instance.assigned_district.status = District.ACTIVE
        instance.assigned_district.save()
        
    elif instance.role == 'chairman' and instance.assigned_city:
        instance.assigned_city.chairman = instance
        instance.assigned_city.status = CityVillage.ACTIVE
        instance.assigned_city.save()
        
    elif instance.role == 'sarpanch' and instance.assigned_village:
        instance.assigned_village.sarpanch = instance
        instance.assigned_village.status = CityVillage.ACTIVE
        instance.assigned_village.save()