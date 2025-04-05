from django.db import models
from django.forms import ValidationError
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models import Q

User = get_user_model()  # Dynamically gets the User model

class UserLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    log_message = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)  # To track if the notification is read or not

    def __str__(self):
        return f"{self.user.username} - {self.log_message}"
    
class Country(models.Model):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    STATUS_CHOICES = [(ACTIVE, 'Active'), (INACTIVE, 'Inactive')]

    name = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=INACTIVE)
    pm = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        limit_choices_to={'role': 'pm'},
        related_name="governing_country"
    )

    def clean(self):
        if self.pm and self.pm.role != 'pm':
            raise ValidationError('Only PM can be assigned to country')

    def save(self, *args, **kwargs):
        self.status = self.ACTIVE if self.pm else self.INACTIVE
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

class State(models.Model):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    STATUS_CHOICES = [(ACTIVE, 'Active'), (INACTIVE, 'Inactive')]

    name = models.CharField(max_length=100, unique=True)
    state_code = models.CharField(max_length=10, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="states")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=INACTIVE)
    cm = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        limit_choices_to={'role': 'cm'},
        related_name="governing_state"
    )
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)  # Central point
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)  # Central point
    polygon = models.JSONField(blank=True, null=True)  # Full boundary as JSON
    def clean(self):
        if self.cm and self.cm.role != 'cm':
            raise ValidationError('Only CM can be assigned to state')

    def save(self, *args, **kwargs):
        self.status = self.ACTIVE if self.cm else self.INACTIVE
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}, {self.country}"

class District(models.Model):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    STATUS_CHOICES = [(ACTIVE, 'Active'), (INACTIVE, 'Inactive')]

    name = models.CharField(max_length=100, unique=True)
    district_code = models.CharField(max_length=10, unique=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="districts")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=INACTIVE)
    vidhayak = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        limit_choices_to={'role': 'vidhayak'},
        related_name="governing_district"
    )
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)  # Central point
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)  # Central point
    polygon = models.JSONField(blank=True, null=True)  # Full boundary as JSON
    def clean(self):
        if self.vidhayak and self.vidhayak.role != 'vidhayak':
            raise ValidationError('Only Vidhayak can be assigned to district')

    def save(self, *args, **kwargs):
        # Update status based on two conditions:
        # 1. Has a vidhayak assigned
        # 2. Has at least one ward in its localities
        has_wards = any(locality.wards.exists() for locality in self.localities.all())
        self.status = self.ACTIVE if (self.vidhayak and has_wards) else self.INACTIVE
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}, {self.state}"
    
class CityVillage(models.Model):
    CITY = 'City'
    VILLAGE = 'Village'
    TYPE_CHOICES = [(CITY, 'City'), (VILLAGE, 'Village')]
    
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    STATUS_CHOICES = [(ACTIVE, 'Active'), (INACTIVE, 'Inactive')]

    name = models.CharField(max_length=100)
    location_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    tehsil = models.CharField(max_length=100)
    post_office = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=6)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="localities")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=INACTIVE)
    
    chairman = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        limit_choices_to={'role': 'chairman'},
        related_name="governing_city"
    )
    sarpanch = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        limit_choices_to={'role': 'sarpanch'},
        related_name="governing_village"
    )
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)  # Central point
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)  # Central point
    polygon = models.JSONField(blank=True, null=True)  # Full boundary as JSON
    def clean(self):
        """Validate proper role assignments based on location type"""
        if self.location_type == self.CITY and self.sarpanch:
            raise ValidationError('Cities cannot have Sarpanch')
        if self.location_type == self.VILLAGE and self.chairman:
            raise ValidationError('Villages cannot have Chairman')
        
        # Validate pin code format
        if not self.pin_code.isdigit() or len(self.pin_code) != 6:
            raise ValidationError('PIN code must be 6 digits')

    def save(self, *args, **kwargs):
        """
        Modified save method to prevent recursion with User model
        """
        # First determine if we're creating or updating
        is_new = self._state.adding
        
        # Update status based on leadership assignment
        self.status = self.ACTIVE if (
            (self.location_type == self.CITY and self.chairman) or
            (self.location_type == self.VILLAGE and self.sarpanch)
        ) else self.INACTIVE
        
        # Get current DB values if updating
        if not is_new:
            old_instance = CityVillage.objects.get(pk=self.pk)
            old_chairman = old_instance.chairman
            old_sarpanch = old_instance.sarpanch
        else:
            old_chairman = None
            old_sarpanch = None
        
        # Save the CityVillage first
        super().save(*args, **kwargs)
        
        # Handle chairman assignment without recursion
        if self.chairman != old_chairman:
            # Clear old chairman's assignment
            if old_chairman:
                old_chairman.assigned_city = None
                old_chairman.save(update_fields=['assigned_city'])
            
            # Set new chairman's assignment
            if self.chairman:
                self.chairman.assigned_city = self
                self.chairman.save(update_fields=['assigned_city'])
        
        # Handle sarpanch assignment without recursion
        if self.sarpanch != old_sarpanch:
            # Clear old sarpanch's assignment
            if old_sarpanch:
                old_sarpanch.assigned_village = None
                old_sarpanch.save(update_fields=['assigned_village'])
            
            # Set new sarpanch's assignment
            if self.sarpanch:
                self.sarpanch.assigned_village = self
                self.sarpanch.save(update_fields=['assigned_village'])
        
        # Update wards status if needed
        if hasattr(self, 'wards'):
            self.update_wards_status()

    def update_wards_status(self):
        """Update status of all wards in this city/village"""
        for ward in self.wards.all():
            ward.save(update_fields=['status'])  # Only update status field

    def __str__(self):
        return f"{self.name} ({self.get_location_type_display()})"

class Ward(models.Model):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    STATUS_CHOICES = [(ACTIVE, 'Active'), (INACTIVE, 'Inactive')]

    name = models.CharField(max_length=100)
    number = models.CharField(max_length=2)
    city_village = models.ForeignKey(CityVillage, on_delete=models.CASCADE, related_name="wards")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=INACTIVE)
    sabhasad = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        limit_choices_to={'role': 'sabhasad'},
        related_name="governing_ward"
    )
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)  # Central point
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)  # Central point
    polygon = models.JSONField(blank=True, null=True)  # Full boundary as JSON

    def clean(self):
        if self.sabhasad and self.sabhasad.role != 'sabhasad':
            raise ValidationError('Only Sabhaad can be assigned to ward')

    def save(self, *args, **kwargs):
        self.status = self.ACTIVE if self.sabhasad else self.INACTIVE
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Ward {self.number}, {self.city_village}"

class News(models.Model):
    content = models.TextField()
    photo = models.ImageField(upload_to='news_photos/', blank=True, null=True)
    video = models.FileField(upload_to='news_videos/', blank=True, null=True)
    is_public = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)  

    # Blockchain fields
    content_hash = models.CharField(max_length=256, blank=True, null=True)
    blockchain_txn_id = models.CharField(max_length=256, blank=True, null=True)

    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='news_posts')
    role = models.CharField(max_length=50, choices=User.ROLE_CHOICES)  # Sync with User's roles
    
    # Geographic fields - for news location
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True, blank=True)
    state = models.ForeignKey('State', on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey('District', on_delete=models.SET_NULL, null=True, blank=True)
    city_village = models.ForeignKey('CityVillage', on_delete=models.SET_NULL, null=True, blank=True)
    ward = models.ForeignKey('Ward', on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_by', 'role']),
            models.Index(fields=['country', 'state', 'district', 'city_village', 'ward']),
        ]

    def __str__(self):
        return f"News by {self.created_by.username} - {self.created_at}"

    @classmethod
    def get_news_for_user(cls, user):
        """
        Get news relevant for the user based on their role and location
        Returns 3 querysets in a tuple:
        1. News posted by the user
        2. News from user's resident area
        3. News from user's assigned area (based on role)
        """
        # 1. News posted by the user
        user_posts = cls.objects.filter(created_by=user, is_deleted=False)
        
        # 2. News from user's resident area
        resident_news_filters = Q()
        if user.user_country:
            resident_news_filters |= Q(country=user.user_country)
        if user.user_state:
            resident_news_filters |= Q(state=user.user_state)
        if user.user_district:
            resident_news_filters |= Q(district=user.user_district)
        if user.user_city:
            resident_news_filters |= Q(city_village=user.user_city)
        if user.user_ward:
            resident_news_filters |= Q(ward=user.user_ward)

        resident_news = cls.objects.filter(
            is_public=True,
            is_deleted=False
        ).filter(
            resident_news_filters
        ).exclude(created_by=user)
        
        # 3. News from user's assigned area (based on role)
        assigned_filters = {}
        if user.role in ['cm', 'pm', 'admin']:
            # These roles can see ALL public news
            assigned_news = cls.objects.filter(is_public=True, is_deleted=False)
        else:
            assigned_filters = {}
            if user.assigned_country:
                assigned_filters['country'] = user.assigned_country
            if user.assigned_state:
                assigned_filters['state'] = user.assigned_state
            if user.assigned_district:
                assigned_filters['district'] = user.assigned_district
            if user.assigned_city or user.assigned_village:
                assigned_filters['city_village'] = user.assigned_city or user.assigned_village
            if user.assigned_ward:
                assigned_filters['ward'] = user.assigned_ward

            assigned_news = cls.objects.filter(
                is_public=True,
                is_deleted=False,
                **assigned_filters
            ).exclude(created_by=user)
        
        return (user_posts, resident_news, assigned_news)
    
class BlockchainRecord(models.Model):
    """
    Temporary model to store hashes before using real blockchain.
    """
    news = models.OneToOneField('News', on_delete=models.CASCADE)
    content_hash = models.CharField(max_length=256, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Blockchain Hash for News {self.news.id}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming you are using the default User model
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}"