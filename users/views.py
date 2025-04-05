from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Prefetch
# Create your views here.
from rest_framework.response import Response
from rest_framework import status, generics
from .models import User
from news.models import State, District, CityVillage, Ward, Country, News
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import User
from .forms import UserForm
from .serializers import RegisterSerializer, LoginSerializer,UserSerializer
from rest_framework.permissions import AllowAny
from django.http import JsonResponse

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

def login(request):
    return render(request,'auth/login.html')

def admin_dashboard(request):
    # User counts remain the same
    total_users = User.objects.filter(is_superuser=False).count()
    users_by_role = {
        'janta': User.objects.filter(role='janta').count(),
        'ward_member': User.objects.filter(role='ward_member').count(),
        'mla': User.objects.filter(role='mla').count(),
        'sarpanch': User.objects.filter(role='sarpanch').count(),
    }

    # News counts remain the same
    total_news = News.objects.count()
    news_by_role = News.objects.values('role').annotate(total=Count('id'))
    users = User.objects.filter(is_superuser=False).order_by('-date_joined')

    # Location counts
    total_countries = Country.objects.count()
    total_states = State.objects.count()
    total_districts = District.objects.count()
    total_city_villages = CityVillage.objects.count()
    total_wards = Ward.objects.count()

    # Corrected active counts using 'localities'
    active_wards = total_wards
    active_city_villages = CityVillage.objects.filter(wards__isnull=False).distinct().count()
    active_districts = District.objects.filter(localities__wards__isnull=False).distinct().count()
    active_states = State.objects.filter(
        districts__localities__wards__isnull=False
    ).distinct().count()

    inactive_wards = total_wards - active_wards
    inactive_city_villages = total_city_villages - active_city_villages
    inactive_districts = total_districts - active_districts
    inactive_states = total_states - active_states

    # Fetch lists with corrected field names
    states = State.objects.annotate(total_districts=Count('districts'))
    districts = District.objects.annotate(total_city_villages=Count('localities'))
    city_villages = CityVillage.objects.annotate(total_wards=Count('wards'))
    wards = Ward.objects.all()

    return render(request, 'customadmin/admin-dashboard.html', {
        'total_users': total_users,
        'users_by_role': users_by_role,
        'total_news': total_news,
        'news_by_role': news_by_role,
        'total_countries': total_countries,
        'total_states': total_states,
        'total_districts': total_districts,
        'total_city_villages': total_city_villages,
        'total_wards': total_wards,
        'users': users,
        'active_states': active_states,
        'inactive_states': inactive_states,
        'active_districts': active_districts,
        'inactive_districts': inactive_districts,
        'active_city_villages': active_city_villages,
        'inactive_city_villages': inactive_city_villages,
        'active_wards': active_wards,
        'inactive_wards': inactive_wards,
        'states': states,
        'districts': districts,
        'city_villages': city_villages,
        'wards': wards,
    })

# def UserManagement(request):
#     users = User.objects.filter(is_superuser=False).order_by('-date_joined')  # Exclude superusers
    
#     # Count users by role
#     users_by_role = {
#         'janta': User.objects.filter(role='janta', is_superuser=False).count(),
#         'sabhasad': User.objects.filter(role='sabhasad', is_superuser=False).count(),
#         'chairman': User.objects.filter(role='chairman', is_superuser=False).count(),
#         'vidhayak': User.objects.filter(role='vidhayak', is_superuser=False).count(),
#         'sarpanch': User.objects.filter(role='sarpanch', is_superuser=False).count(),
#     }

#     # Count of total users excluding superusers
#     total_users = User.objects.filter(is_superuser=False).count()

#     return render(request, 'customadmin/admin_user_management.html', {
#         'users': users,
#         'users_by_role': users_by_role,
#         'total_users': total_users,
#     })

# Check if the user is an admin or superuser
def is_admin(user):
    return user.is_superuser or user.role == 'admin'

@user_passes_test(is_admin)
def user_management(request):
    users = User.objects.filter(is_superuser=False).order_by('-date_joined')
    users_by_role = {role: User.objects.filter(role=role, is_superuser=False).count() for role, _ in User.ROLE_CHOICES}
    total_users = users.count()

    return render(request, 'customadmin/admin_user_management.html', {
        'users': users,
        'users_by_role': users_by_role,
        'total_users': total_users,
        'form': UserForm(),
    })

@user_passes_test(is_admin)
def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        role = request.POST.get('role', 'janta')  # Default role is 'janta'
        assigned_place_id = request.POST.get('assigned_place')  # Get assigned place ID

        if not username or not email or not role:
            messages.error(request, "All fields are required.")
            return redirect('add_user')

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('add_user')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('add_user')

        # Create user with a default password
        default_password = "Sanchaar@1"
        user = User.objects.create_user(username=username, email=email, role=role, password=default_password)

        # Assign the appropriate place based on the role
        if assigned_place_id:
            try:
                if role == "pm":
                    user.assigned_country = Country.objects.get(id=assigned_place_id)
                elif role == "cm":
                    user.assigned_state = State.objects.get(id=assigned_place_id)
                elif role == "vidhayak":
                    user.assigned_district = District.objects.get(id=assigned_place_id)
                elif role == "chairman":
                    user.assigned_city = CityVillage.objects.get(id=assigned_place_id)
                elif role == "sarpanch":
                    user.assigned_village = CityVillage.objects.get(id=assigned_place_id)
                elif role == "sabhasad":
                    user.assigned_ward = Ward.objects.get(id=assigned_place_id)
            except Exception as e:
                messages.error(request, f"Error assigning place: {e}")

        user.save()  # Save user after assigning location

        # Send credentials via email
        subject = "Your Account Credentials"
        message = render(request, 'customadmin/credentials_email.html', {
            'username': username,
            'password': default_password
        }).content.decode("utf-8")

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
            html_message=message,
        )

        messages.success(request, f"User '{username}' created successfully. Credentials have been sent via email.")
        return redirect('add_user')

    # Fetch locations for the dropdown
    countries = Country.objects.values("id", "name")
    states = State.objects.values("id", "name")
    districts = District.objects.values("id", "name")
    cities = CityVillage.objects.filter(location_type="City").values("id", "name")
    villages = CityVillage.objects.filter(location_type="Village").values("id", "name")
    wards = Ward.objects.values("id", "name")

    return render(request, 'customadmin/create_user.html', {
        "countries": countries,
        "states": states,
        "districts": districts,
        "cities": cities,
        "villages": villages,
        "wards": wards,
    })

@user_passes_test(is_admin)
def user_view(request, user_id):
    # Get the specific user, assuming UUID is being used for the user
    user = get_object_or_404(User, id=user_id)
    
    context = {
        'user': user,
    }
    return render(request, 'customadmin/user_view.html', context)

@user_passes_test(is_admin)
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    countries = Country.objects.values("id", "name")
    states = State.objects.values("id", "name")
    districts = District.objects.values("id", "name")
    cities = CityVillage.objects.filter(location_type="City").values("id", "name")
    villages = CityVillage.objects.filter(location_type="Village").values("id", "name")
    wards = Ward.objects.values("id", "name")

    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            updated_user = form.save(commit=False)
            assigned_id = request.POST.get("assigned_place")
            new_role = request.POST.get("role")

            # Handle role change
            if new_role and new_role != user.role:
                updated_user.role = new_role
                updated_user.assigned_country = None
                updated_user.assigned_state = None
                updated_user.assigned_district = None
                updated_user.assigned_city = None
                updated_user.assigned_village = None
                updated_user.assigned_ward = None

            # Assigned place logic (as before)
            if assigned_id:
                try:
                    if updated_user.role == "pm":
                        updated_user.assigned_country = Country.objects.get(id=assigned_id)
                    elif updated_user.role == "cm":
                        updated_user.assigned_state = State.objects.get(id=assigned_id)
                    elif updated_user.role == "vidhayak":
                        updated_user.assigned_district = District.objects.get(id=assigned_id)
                    elif updated_user.role == "chairman":
                        updated_user.assigned_city = CityVillage.objects.get(id=assigned_id, location_type="City")
                    elif updated_user.role == "sarpanch":
                        updated_user.assigned_village = CityVillage.objects.get(id=assigned_id, location_type="Village")
                    elif updated_user.role == "sabhasad":
                        updated_user.assigned_ward = Ward.objects.get(id=assigned_id)
                except Exception as e:
                    messages.error(request, f"Error assigning location: {str(e)}")
                    return redirect('edit_user', user_id=user_id)

            # Handle user resident location updates
            updated_user.user_country_id = request.POST.get("user_country") or None
            updated_user.user_state_id = request.POST.get("user_state") or None
            updated_user.user_district_id = request.POST.get("user_district") or None
            updated_user.user_city_id = request.POST.get("user_city") or None
            updated_user.user_ward_id = request.POST.get("user_ward") or None

            updated_user.save()
            messages.success(request, "User updated successfully!")
            return redirect("user_management")
    else:
        form = UserForm(instance=user)

    # Determine current assigned place
    assigned_place_id = (
        user.assigned_country_id or user.assigned_state_id or user.assigned_district_id or 
        user.assigned_city_id or user.assigned_village_id or user.assigned_ward_id
    )

    return render(request, "customadmin/edit_user.html", {
        "form": form,
        "user": user,
        "assigned_place_id": assigned_place_id,
        "countries": list(countries),
        "states": list(states),
        "districts": list(districts),
        "cities": list(cities),
        "villages": list(villages),
        "wards": list(wards),
    })


@user_passes_test(is_admin)
def block_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.is_active = False
        user.save()
        return redirect('user_management')
    return redirect('user_management')

def unblock_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.is_active = True
        user.save()
        return redirect('user_management')
    return redirect('user_management')

@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return JsonResponse({'message': 'User deleted successfully!'})


def StateManagement(request):
    states = State.objects.all()
    total_states = states.count()
    
    # Corrected query using 'localities' instead of 'city_villages'
    active_states = State.objects.filter(
        districts__localities__wards__isnull=False
    ).distinct().count()
    
    inactive_states = total_states - active_states

    state_data = []
    for state in states:
        district_count = state.districts.count()
        city_village_count = sum(d.localities.count() for d in state.districts.all())
        ward_count = sum(cv.wards.count() for d in state.districts.all() for cv in d.localities.all())

        state_data.append({
            'state': state,
            'district_count': district_count,
            'city_village_count': city_village_count,
            'ward_count': ward_count,
            'status': 'Active' if ward_count > 0 else 'Inactive',
        })

    return render(request, 'customadmin/state_management.html', {
        'total_states': total_states,
        'active_states': active_states,
        'inactive_states': inactive_states,
        'states': state_data,
    })

def DistrictManagement(request):
    # Prefetch all necessary related data
    districts = District.objects.select_related('state').prefetch_related(
        Prefetch('localities', queryset=CityVillage.objects.prefetch_related('wards'))
    ).all()

    # Get counts
    total_district = districts.count()
    active_district = districts.filter(status=District.ACTIVE).count()
    inactive_district = total_district - active_district

    # Prepare district data
    district_data = []
    for district in districts:
        city_village_count = district.localities.count()
        ward_count = sum(locality.wards.count() for locality in district.localities.all())

        district_data.append({
            'district': district,  # Pass the whole district object
            'district_name': f"{district.name} ({district.state.name})",
            'city_village_count': city_village_count,
            'ward_count': ward_count,
            # No need for manual status calculation here - using model's status
        })

    return render(request, 'customadmin/district_management.html', {
        'total_district': total_district,
        'active_district': active_district,
        'inactive_district': inactive_district,
        'districts': district_data,
    })

def CityVillageManagement(request):
    # Get all CityVillage objects
    all_places = CityVillage.objects.prefetch_related('wards').all()  # ✅ Optimized Query

    # Count total Cities and Villages
    total_cities = all_places.filter(location_type=CityVillage.CITY).count()
    total_villages = all_places.filter(location_type=CityVillage.VILLAGE).count()

    # Count Active Cities & Active Villages based on the presence of wards
    active_cities = all_places.filter(location_type=CityVillage.CITY, wards__isnull=False).distinct().count()
    active_villages = all_places.filter(location_type=CityVillage.VILLAGE, wards__isnull=False).distinct().count()
    
    inactive_cities = total_cities-active_cities
    inactive_villages = total_villages-active_villages
    # Prepare list for displaying in the table
    city_village_data = [
        {
            'name': place.name,
            'location_type': place.get_location_type_display(),
            'tehsil': place.tehsil,
            'post_office': place.post_office,
            'district': place.district.name,
            'pin_code': place.pin_code,
            'status': 'Active' if place.wards.exists() else 'Inactive',  # ✅ Check `wards.exists()` instead of `district`
        }
        for place in all_places
    ]

    return render(request, 'customadmin/city_village_mangement.html', {
        'total_cities': total_cities,
        'total_villages': total_villages,
        'active_cities': active_cities,
        'active_villages': active_villages,
        'inactive_cities':inactive_cities,
        'inactive_villages':inactive_villages,
        'city_villages': city_village_data,  # Pass processed data to template
    })


def WardManagement(request):
    # Get all Wards with related City/Village and Sabhasad for optimization
    all_wards = Ward.objects.select_related('city_village', 'sabhasad').all()

    # Update Ward Status based on whether it has an assigned Sabhasad
    for ward in all_wards:
        if ward.sabhasad:
            ward.status = "Active"  # If a Sabhasad is assigned, mark Ward as Active
        else:
            ward.status = "Inactive"  # If no Sabhasad, mark Ward as Inactive
        ward.save()

    # Count total Wards
    total_wards = all_wards.count()

    # Count total Sabhasads (Assigned Wards Only)
    total_sabhasads = all_wards.filter(sabhasad__isnull=False).count()
    
    # Count total Janta members assigned and unassigned
    total_janta = User.objects.filter(role="janta", assigned_ward__isnull=False).count()
    unassigned_janta = User.objects.filter(role="janta", assigned_ward__isnull=True).count()

    # Count Active and Inactive Wards
    active_wards = all_wards.filter(status='Active').count()
    inactive_wards = all_wards.filter(status='Inactive').count()

    # Prepare data for table display
    ward_data = [
        {
            "ward_name": ward.name,
            "ward_number": ward.number,
            "city_village_name": ward.city_village.name,
            "sabhasad_name": (
                f"{ward.sabhasad.first_name} {ward.sabhasad.last_name}".strip()
                if ward.sabhasad and (ward.sabhasad.first_name or ward.sabhasad.last_name)
                else (ward.sabhasad.username if ward.sabhasad else "Unassigned")  # ✅ Show "Unassigned" if no Sabhasad
            ),
            "ward_member_status": "Assigned" if ward.sabhasad else "Unassigned",  # ✅ Show Assigned/Unassigned
            "status": ward.status,  # ✅ Ensure status is updated
        }
        for ward in all_wards
    ]

    return render(request, 'customadmin/ward_management.html', {
        "total_wards": total_wards,
        "total_sabhasads": total_sabhasads,
        'total_janta': total_janta,
        'unassigned_janta': unassigned_janta,
        'active_wards': active_wards,
        'inactive_wards': inactive_wards,
        "ward_data": ward_data
    })

def NewsManagement(request):
    # Get all news with related creator info
    news_list = News.objects.filter(is_deleted=False).select_related('created_by').order_by('-created_at')
    
    processed_news = []
    for news in news_list:
        # Determine news type based on creator's role
        if news.created_by.role == 'pm':
            news_type = 'Country Wide'
        elif news.created_by.role == 'cm':
            news_type = 'State Wide'
        elif news.created_by.role == 'vidhayak':
            news_type = 'District Wide'
        elif news.created_by.role == 'chairman':
            news_type = 'City Wide'
        elif news.created_by.role == 'sabhasad':
            news_type = 'Ward Wide'
        else:
            news_type = 'General'
        
        processed_news.append({
            'id': news.id,
            'creator_name': news.created_by.get_full_name(),
            'creator_email': news.created_by.email,
            'news_type': news_type,
            'date_submitted': news.created_at.strftime("%d %b %Y %I:%M %p")
        })
    
    context = {'news_list': processed_news}
    return render(request, 'customadmin/news_management.html', context)


def news_detail(request, news_id):
    news = get_object_or_404(News, id=news_id)
    
    # Determine news type
    if news.created_by.role == 'pm':
        news_type = 'Country Wide'
    elif news.created_by.role == 'cm':
        news_type = 'State Wide'
    elif news.created_by.role == 'vidhayak':
        news_type = 'District Wide'
    elif news.created_by.role == 'chairman':
        news_type = 'City Wide'
    elif news.created_by.role == 'sabhasad':
        news_type = 'Ward Wide'
    else:
        news_type = 'General'
    
    context = {
        'news': news,
        'news_type': news_type
    }
    return render(request, 'customadmin/news_detail.html', context)

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# from .serializers import UserDetailSerializer

class UserDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)