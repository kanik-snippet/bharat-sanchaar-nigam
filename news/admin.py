from django.contrib import admin
from .models import News,Ward,CityVillage,Country,District,State,Notification
# Register your models here.
admin.site.register(News)
admin.site.register(Ward)
admin.site.register(CityVillage)
admin.site.register(Country)
admin.site.register(District)
admin.site.register(State)
admin.site.register(Notification)