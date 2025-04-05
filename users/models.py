from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

class User(AbstractUser):
    ROLE_CHOICES = [
        ('janta', 'Janta'),
        ('sabhasad', 'Sabhasad'),
        ('chairman', 'Chairman'),
        ('vidhayak', 'Vidhayak'),
        ('sarpanch', 'Sarpanch'),
        ('cm', 'CM'),
        ('pm', 'PM'),
        ('admin', 'Admin'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='janta')

    assigned_country = models.ForeignKey('news.Country', on_delete=models.SET_NULL, null=True, blank=True, related_name="users_in_country")
    assigned_state = models.ForeignKey('news.State', on_delete=models.SET_NULL, null=True, blank=True, related_name="users_in_state")
    assigned_district = models.ForeignKey('news.District', on_delete=models.SET_NULL, null=True, blank=True, related_name="users_in_district")
    assigned_city = models.ForeignKey('news.CityVillage', on_delete=models.SET_NULL, null=True, blank=True, related_name="users_in_city")
    assigned_village = models.ForeignKey('news.CityVillage', on_delete=models.SET_NULL, null=True, blank=True, related_name="users_in_village")
    assigned_ward = models.ForeignKey('news.Ward', on_delete=models.SET_NULL, null=True, blank=True, related_name="users_in_ward")

    user_country = models.ForeignKey('news.Country', on_delete=models.SET_NULL, null=True, blank=True, related_name='residents_in_country')
    user_state = models.ForeignKey('news.State', on_delete=models.SET_NULL, null=True, blank=True, related_name='residents_in_state')
    user_district = models.ForeignKey('news.District', on_delete=models.SET_NULL, null=True, blank=True, related_name='residents_in_district')
    user_city = models.ForeignKey('news.CityVillage', on_delete=models.SET_NULL, null=True, blank=True, related_name='residents_in_city')
    user_ward = models.ForeignKey('news.Ward', on_delete=models.SET_NULL,null=True, blank=True, related_name='residents_in_ward')
    is_active = models.BooleanField(default=True)

    def clean(self):
        """Only clear assignments that don't match the user's role"""
        if self.role == 'janta':
            # Janta can ONLY have ward assignments (no country/state/district/city/village)
            self.assigned_country = None
            self.assigned_state = None
            self.assigned_district = None
            self.assigned_city = None
            self.assigned_village = None
            # NOTE: assigned_ward is ALLOWED for janta
        
        elif self.role == 'sabhasad':
            # Sabhasad can ONLY have ward assignments
            self.assigned_country = None
            self.assigned_state = None
            self.assigned_district = None
            self.assigned_city = None
            self.assigned_village = None
        
        elif self.role in ['chairman', 'sarpanch']:
            # Chairman/Sarpanch can ONLY have city/village assignments
            self.assigned_country = None
            self.assigned_state = None
            self.assigned_district = None
            self.assigned_ward = None
        
        elif self.role == 'vidhayak':
            # Vidhayak can ONLY have district assignments
            self.assigned_country = None
            self.assigned_state = None
            self.assigned_city = None
            self.assigned_village = None
            self.assigned_ward = None
    
    # ... similar logic for cm/pm/admin ...

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        
        if self.pk:
            original = User.objects.get(pk=self.pk)
            if original.role != self.role:
                self.handle_role_change(original.role)

    def handle_role_change(self, old_role):
        if old_role == 'sabhasad' and self.role != 'sabhasad':
            if self.assigned_ward:
                ward = self.assigned_ward
                ward.sabhasad = None
                ward.save()
            self.assigned_ward = None
        
        if old_role == 'vidhayak' and self.role != 'vidhayak':
            if self.assigned_district:
                district = self.assigned_district
                district.vidhayak = None
                district.save()
            self.assigned_district = None
            
        if old_role == 'chairman' and self.role != 'chairman':
            if self.assigned_city:
                city = self.assigned_city
                city.chairman = None
                city.save()
            self.assigned_city = None
            
        self.save()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"