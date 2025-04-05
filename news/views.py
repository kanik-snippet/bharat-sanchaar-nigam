from django.forms import ValidationError
from django.shortcuts import render
from users.models import User
from rest_framework.views import APIView
from rest_framework import status
from threading import Thread
from .notifications import notify_users, assign_news_location
from django.db.models import Q,Max
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
# Create your views here.
import requests

from django.contrib.auth.tokens import default_token_generator
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import News,Notification,District,CityVillage,Country
from .serializers import *
from django.shortcuts import get_object_or_404, render, redirect
from rest_framework.exceptions import PermissionDenied
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives, send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from .utils import *
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
import hashlib
from .blockchain_utils import store_on_blockchain
from .blockchain_utils import verify_blockchain_hash,generate_content_hash # Function to fetch stored hash from blockchain

# Define the view for the dashboard
def home(request):
    return render(request, 'auth/home.html', {'LANGUAGE_CODE': request.LANGUAGE_CODE})
def dashboard(request):
    return render(request, 'frontend/dash.html')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_counts(request):
    user = request.user
    
    # Original counts (unchanged)
    news_count = News.objects.count()
    last_news_update = News.objects.aggregate(last_update=Max('created_at'))['last_update']
    
    # Get 5 most recent news with the correct fields (unchanged)
    recent_news = News.objects.order_by('-created_at')[:5].select_related('created_by')
    
    recent_news_data = []
    for news in recent_news:
        created_by_display = 'System'
        if news.created_by:
            if news.created_by.first_name and news.created_by.last_name:
                created_by_display = f"{news.created_by.first_name} {news.created_by.last_name}"
            else:
                created_by_display = news.created_by.username
        
        news_data = {
            'id': news.id,
            'heading': news.heading if hasattr(news, 'heading') else 'No Title',
            'content': news.content[:100] + '...' if news.content else '',
            'created_at': news.created_at,
            'created_by': created_by_display,
            'image_url': news.image.url if hasattr(news, 'image') and news.image else None
        }
        recent_news_data.append(news_data)
    
    # Get ALL notifications for the user (both read and unread) (unchanged)
    user_notifications = Notification.objects.filter(user=user)
    notification_count = user_notifications.count()
    last_notification_update = user_notifications.aggregate(last_update=Max('created_at'))['last_update']
    
    # NEW: Get resident news count using the same logic as UserNewsFeedAPIView
    _, resident_news, _ = News.get_news_for_user(user)
    resident_news_count = resident_news.count()
    
    return Response({
        'news_count': news_count,  # Original total news count
        'resident_news_count': resident_news_count,  # NEW: Added resident news count
        'last_news_update': last_news_update,
        'recent_news': recent_news_data,
        'notification_count': notification_count,
        'last_notification_update': last_notification_update
    })

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def mark_all_notifications_read(request):
    updated = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).update(is_read=True)
    
    return Response({'status': 'success', 'marked_read': updated})

from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from .models import News

# def khabhar(request):
#     if not request.user.is_authenticated:
#         print("❌ User is not authenticated! Redirecting to login...")
#         return redirect('login')  # or your custom login URL name

#     user = request.user
#     print("👤 Logged-in User:", user.username)
#     print("📍 Assigned Location → State:", user.assigned_state, 
#           "| District:", user.assigned_district, 
#           "| City:", user.assigned_city, 
#           "| Ward:", user.assigned_ward)

#     assigned_filters = Q()
#     live_filters = Q()

#     role = user.role
#     print("🧩 Role Detected:", role)

#     if role == "Sabhasad":
#         assigned_filters = Q(
#             state=user.assigned_state,
#             district=user.assigned_district,
#             city_village=user.assigned_city,
#             ward=user.assigned_ward,
#             created_by__role="Sabhasad"
#         )
#         print("🔍 Sabhasad Filter Applied")
#     elif role == "Chairman":
#         assigned_filters = Q(
#             state=user.assigned_state,
#             district=user.assigned_district,
#             city_village=user.assigned_city,
#             created_by__role__in=["Chairman", "Sabhasad"]
#         )
#         print("🔍 Chairman Filter Applied")
#     elif role == "Vidhayak":
#         assigned_filters = Q(
#             state=user.assigned_state,
#             district=user.assigned_district,
#             created_by__role__in=["Vidhayak", "Chairman", "Sabhasad"]
#         )
#         print("🔍 Vidhayak Filter Applied")
#     elif role == "CM":
#         assigned_filters = Q(
#             state=user.assigned_state,
#             created_by__role__in=["CM", "Vidhayak", "Chairman", "Sabhasad"]
#         )
#         print("🔍 CM Filter Applied")
#     elif role == "PM":
#         assigned_filters = Q(
#             country=user.assigned_country,
#             created_by__role__in=["PM", "CM", "Vidhayak", "Chairman", "Sabhasad"]
#         )
#         print("🔍 PM Filter Applied")

#     # Live location data from query parameters
#     live_state = request.GET.get("live_state")
#     live_district = request.GET.get("live_district")
#     source = request.GET.get("source", "assigned")

#     if live_state and live_district:
#         live_filters = Q(
#             Q(state_id=live_state) | Q(district_id=live_district)
#         )
#         print("📡 Live Location → State ID:", live_state, "| District ID:", live_district)
#         print("🔍 Live Filters Applied")

#     if source == "live":
#         print("📑 Fetching Live Location News Only")
#         final_news_list = News.objects.filter(live_filters)
#     else:
#         print("📑 Fetching Assigned Location News Only")
#         final_news_list = News.objects.filter(assigned_filters)

#     print("🧮 Total News Found:", final_news_list.count())

#     paginator = Paginator(final_news_list.distinct(), 9)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     context = {
#         'news_list': page_obj,
#         'selected_source': source,
#     }

#     return render(request, 'frontend/khabhar.html', context)

def khabhar(request):
    return render(request, 'frontend/khabhar.html')
def pod(request):
    return render(request, 'frontend/pod.html')

def log(request):
    return render(request, 'frontend/logs.html')

def live(request):
    return render(request, 'live.html')

def evlogs(request, event_id):
    # Just render the template and pass the event_id to it
    return render(request, 'frontend/evlogs.html', {'event_id': event_id})


def wifi(request):
    return render(request, 'frontend/wifi.html')
def stream(request):
    return render(request, 'frontend/stream.html')

def profile(request):
    return render(request, 'frontend/profile.html')

def change_password(request):
    return render(request, 'frontend/changepass.html')

def subscription(request):
    return render(request, 'frontend/subscription.html')
def subscription_txn(request):
    return render(request, 'frontend/subscription_txn.html')

def pod_detail(request, device_id):
    return render(request, 'frontend/pod_detail.html', {'device_id': device_id})

def login(request):
    return render(request,'auth/login.html')

def register(request):
    return render(request,'auth/register.html')

def forgot(request):
    return render(request,'auth/forgot.html')
def resetpass(request, token):
    # You can pass the token to the template if needed
    return render(request, 'auth/resetpass.html', {'token': token})
# def static_content_view(request, slug):
#     # Fetch the static content by slug
#     content = get_object_or_404(StaticContent, slug=slug)
#     return render(request, 'static_content.html', {'content': content})

# def email_content_view(request, slug):
#     # Fetch the static content by slug
#     content = get_object_or_404(emailContent, slug=slug)
#     return render(request, 'email_content.html', {'content': content})

def add_contact(request):
    return render(request, 'frontend/add_contact.html')
def terms(request):
    return render(request, 'terms-and-conditions.html')
def privacy(request):
    return render(request, 'Privacy.html')
def termsOfuse(request):
    return render(request, 'termsOfuse.html')
def salesandrefund(request):
    return render(request, 'salesandrefund.html')
def legalinfo(request):
    return render(request, 'legalinfo.html')
def test(request):
    return render(request, 'test.html')

def ordernow(request):
    return render(request,'ordernow.html')
def tutorials(request):
    return render(request,'tutorials.html')
def plan_pricing(request):
    return render(request,'plan_pricing.html')
def case_study(request):
    return render(request,'case_study.html')
def hiworks(request):
    return render(request,'hiworks.html')
# def user_invoice_view(request, transaction_id):
#     transaction = get_object_or_404(PaymentHistory, pk=transaction_id)
#     context = {
#         'transaction': transaction
#     }
#     return render(request, 'invoice/user_invoice.html', context)

def notifications(request):
    return render(request, 'frontend/notifications.html')

bearer_token = openapi.Parameter(
        'Authorization', openapi.IN_HEADER, description="Bearer token",
        type=openapi.TYPE_STRING, required=True
    )

class GetProfileAPIView(APIView):
    """
    API endpoint to retrieve the logged-in user's profile.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get the profile of the logged-in user.",
        responses={
            200: openapi.Response(
                description="Profile retrieved successfully.",
                schema=UserProfileSerializer,
            ),
            401: openapi.Response(
                description="Unauthorized. Access token is missing or invalid.",
            ),
        },
        manual_parameters=[bearer_token],  # Includes the bearer token in the Swagger UI
        security=[{'Bearer': []}]  # This ensures the security is linked to the bearer token
    )
    def get(self, request):
        """
        Retrieve the logged-in user's profile.
        """
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# API view for updating the user's profile
class UpdateProfileAPIView(APIView):
    """
    API endpoint to update the logged-in user's profile.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Update the profile of the logged-in user.",
        responses={
            200: openapi.Response(
                description="Profile updated successfully.",
                schema=UserProfileSerializer,
            ),
            400: openapi.Response(
                description="Bad Request. Validation failed or invalid data provided.",
            ),
            401: openapi.Response(
                description="Unauthorized. Access token is missing or invalid.",
            ),
        },
        request_body=UserProfileSerializer,  # Serializer used for updating the profile
        manual_parameters=[bearer_token],  # Includes the bearer token in the Swagger UI
        security=[{'Bearer': []}]  # This ensures the security is linked to the bearer token
    )
    def put(self, request):
        """
        Update the logged-in user's profile.
        """
        serializer = UserProfileSerializer(request.user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"detail": _("Profile updated successfully!")}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateProfileImageAPIView(APIView):
    """
    API endpoint to update or delete the profile image of the logged-in user.
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # Ensure file upload is handled

    @swagger_auto_schema(
        operation_description="Update the profile image of the logged-in user.",
        responses={
            200: openapi.Response(
                description="Profile image updated successfully.",
                schema=ProfileImageUpdateSerializer,
            ),
            400: openapi.Response(
                description="Bad Request. Validation failed or invalid data provided.",
            ),
            401: openapi.Response(
                description="Unauthorized. Access token is missing or invalid.",
            ),
        },
        request_body=ProfileImageUpdateSerializer,  # Use the serializer for updating the image
        manual_parameters=[bearer_token],  # Includes the bearer token in the Swagger UI
        security=[{'Bearer': []}],  # Security is linked to the bearer token
        consumes=["multipart/form-data"]  # Allows file uploads for the profile image
    )
    
    def post(self, request):
        """
        Update the profile image of the logged-in user.
        """
        serializer = ProfileImageUpdateSerializer(request.user, data=request.data)

        if serializer.is_valid():
            # Save the image update
            serializer.save()
            return Response({"detail": "Profile image updated successfully!"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete the profile image of the logged-in user.",
        responses={
            200: openapi.Response(
                description="Profile image deleted successfully.",
            ),
            400: openapi.Response(
                description="Bad Request. Validation failed or invalid data provided.",
            ),
            401: openapi.Response(
                description="Unauthorized. Access token is missing or invalid.",
            ),
        },
        manual_parameters=[bearer_token],  # Includes the bearer token in the Swagger UI
        security=[{'Bearer': []}],  # Security is linked to the bearer token
    )

    def delete(self, request):
        """
        Delete the profile image of the logged-in user.
        """
        if request.user.profile_image:
            request.user.profile_image.delete()  # Delete the profile image
            return Response({"detail": _("Profile image deleted successfully!")}, status=status.HTTP_200_OK)
        
        return Response({"detail": _("No profile image found to delete.")}, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordAPIView(APIView):
    """
    API endpoint for changing the user's password.
    """
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    @swagger_auto_schema(
        operation_description="Change the password of the logged-in user.",
        responses={
            200: openapi.Response(
                description="Password changed successfully.",
            ),
            400: openapi.Response(
                description="Bad Request. Invalid form data.",
            ),
            401: openapi.Response(
                description="Unauthorized. Access token is missing or invalid.",
            ),
        },
        request_body=PasswordChangeSerializer,  # Directly use the serializer for the request body
        manual_parameters=[bearer_token],  # Includes the bearer token in the Swagger UI
        security=[{'Bearer': []}]  # This ensures the security is linked to the bearer token
    )
    def post(self, request):
        """
        Handle password change for the logged-in user.
        """
        # Initialize the serializer with the data and user context
        serializer = PasswordChangeSerializer(data=request.data, context={'user': request.user})

        if serializer.is_valid():
            new_password = serializer.validated_data['new_password1']
            request.user.set_password(new_password)
            request.user.save()
            password_changed(request.user)

            return Response({"detail": _("Your password was successfully updated!")}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestAPIView(APIView):
    """
    API to send password reset link to user email.
    """
    permission_classes = [AllowAny]  # Allows access without authentication

    @swagger_auto_schema(
        operation_description="Send password reset link to the user's email.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
            }
        ),
        responses={
            200: openapi.Response(description='Password reset link sent successfully'),
            404: openapi.Response(description='User not found'),
        }
    )
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": _("Email field is required.")}, status=400)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": _("We couldn’t find an account with the provided email. Please check and try again.")}, status=422)

        # Generate password reset token
        token = default_token_generator.make_token(user)

        # Generate password reset URL
        reset_url = reverse('resetpass', kwargs={'token': token})
        reset_link = f"{settings.SITE_URL}{reset_url}"

        # Render email template
        subject = 'ICE-Button System - Reset Your Password'
        message = render_to_string('email/password_reset_email.html', {
            'user': user,
            'reset_link': reset_link,
        })

        # Send the email
        email_message = EmailMultiAlternatives(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email]
        )
        email_message.attach_alternative(message, "text/html")
        email_message.send()

        return Response({"sucess": _("A password reset link has been sent to your registered email address. Please check your inbox and follow the instructions. Note: The reset link will expire in 5 minutes.")}, status=200)


class PasswordResetConfirmAPIView(APIView):
    """
    API to verify the password reset token.
    """
    permission_classes = [AllowAny]  # Allows access without authentication

    @swagger_auto_schema(
        operation_description="Verify the token sent to the user's email.",
        responses={
            200: openapi.Response(description='Token is valid, proceed to reset password.'),
            400: openapi.Response(description='Invalid token or expired link.'),
        }
    )
    def get(self, request, token):
        try:
            user = None
            for potential_user in User.objects.all():
                if default_token_generator.check_token(potential_user, token):
                    user = potential_user
                    break

            if user is None:
                return Response({"detail": "Invalid token or expired link."}, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                "detail": "Token is valid, proceed to reset password.",
                "token": token  # Return the token so the user can use it in the next step.
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetAPIView(APIView):
    permission_classes = [AllowAny]
    """
    API to reset the user's password after verifying the token.
    """

    @swagger_auto_schema(
        operation_description="Reset the user's password.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'new_password': openapi.Schema(type=openapi.TYPE_STRING, description='New password'),
                'confirm_password': openapi.Schema(type=openapi.TYPE_STRING, description='Confirm new password'),
            }
        ),
        responses={
            200: openapi.Response(description='Password has been reset successfully!'),
            400: openapi.Response(description='Invalid token or passwords do not match.'),
        }
    )
    def post(self, request, token):
        try:
            # Find user based on the token
            user = None
            for potential_user in User.objects.all():
                if default_token_generator.check_token(potential_user, token):
                    user = potential_user
                    break

            if user is None:
                raise ValidationError("Invalid token or expired link.")

            # Validate password match
            new_password = request.data.get('new_password')
            confirm_password = request.data.get('confirm_password')

            # Check if new password matches the old password
            if user.check_password(new_password):
                raise ValidationError(_("Your new password cannot be the same as your old password."))

            # Check if new password and confirm password match
            if new_password != confirm_password:
                raise ValidationError(_("The passwords you entered do not match. Please try again."))

            # Update the password
            user.password = make_password(new_password)
            user.save()
            password_reset(user)
            # Send the email
            subject = "ICE-Button System - Password Reset Confirmation"
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = user.email
            context = {"user_name": user.first_name or "User"}
            email_body = render_to_string("email/password_reset_confirmation.html", context)

            email = EmailMultiAlternatives(
                subject=subject,
                body=email_body,
                from_email=from_email,
                to=[to_email],
            )
            email.attach_alternative(email_body, "text/html")
            email.send()

            return Response({"detail": _("Your password has been reset successfully! You can now log in with your new password.")}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class NotificationListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        data = [
            {"id": n.id, "message": n.message, "created_at": n.created_at, "is_read": n.is_read}
            for n in notifications
        ]
        return Response(data)

class MarkNotificationAsReadView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Notification.objects.all()  # Add this line
    lookup_field = 'id'  # Make sure this matches your URL pattern

    def patch(self, request, *args, **kwargs):
        notification = self.get_object()
        
        # Check if the notification belongs to the requesting user
        if notification.user != request.user:
            return Response(
                {"detail": "You don't have permission to mark this notification as read."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if not notification.is_read:
            notification.is_read = True
            notification.save()
            return Response(
                {"status": "Notification marked as read"},
                status=status.HTTP_200_OK
            )
        return Response(
            {"status": "Notification was already read"},
            status=status.HTTP_200_OK
        )
import traceback
from django.core.exceptions import ObjectDoesNotExist

class NewsCreateView(generics.CreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            user = self.request.user

            # Ensure the user is authenticated
            if not user or user.is_anonymous:
                raise ValueError("User must be authenticated to create news.")

            print(f"User: {user}")

            # Assign location based on user role
            location_data = assign_news_location(user)
            print(f"Location Data: {location_data}")

            # Create news object
            news = serializer.save(created_by=user, role=user.role, **location_data)
            print(f"News Created: {news}")

            # Generate Hash
            content_hash = generate_content_hash(news)
            print(f"Content Hash: {content_hash}")

            # Store Hash in BlockchainRecord (Simulated Blockchain Storage)
            txn_id = store_on_blockchain(news, content_hash)
            print(f"Blockchain Transaction ID: {txn_id}")

            # Save Hash & Blockchain Transaction ID
            news.content_hash = content_hash
            news.blockchain_txn_id = txn_id
            news.save()
            print("✅ News saved successfully!")

            # Process notifications in background thread
            Thread(target=notify_users, args=(news,)).start()

        except ValueError as e:
            print(f"❌ Error: {e}")
        except ObjectDoesNotExist as e:
            print(f"❌ User not found: {e}")
        except Exception:
            print("❌ Error in NewsCreateView.perform_create:")
            print(traceback.format_exc())  # Print full error traceback

class NewsListView(generics.ListAPIView):
    serializer_class = NewsListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = News.objects.filter(is_deleted=False, is_public=True).order_by('-created_at')

        # Fetch user's assigned location
        user_ward = user.user_ward
        user_city = user.user_city
        user_district = user.user_district
        user_state = user.user_state
        user_country = user.user_country

        # Get live location from request params (passed from frontend)
        live_state_id = self.request.query_params.get("live_state")
        live_district_id = self.request.query_params.get("live_district")

        # Assigned location filter
        user_news = queryset.filter(
            Q(ward=user_ward) |
            Q(city_village=user_city) |
            Q(district=user_district) |
            Q(state=user_state) |
            Q(country=user_country)
        )

        # Live location filter (if live state and district are provided)
        live_news = queryset.none()
        if live_state_id and live_district_id:
            live_news = queryset.filter(
                Q(state_id=live_state_id) |
                Q(district_id=live_district_id)
            )

        # Combine both assigned location and live location news
        final_queryset = user_news | live_news
        return final_queryset.distinct()

class NewsDetailView(generics.RetrieveAPIView):
    queryset = News.objects.filter(is_deleted=False, is_public=True)
    serializer_class = NewsDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        news = self.get_object()

        # Check integrity using the BlockchainRecord
        if not verify_blockchain_hash(news):
            return Response({"error": "This post has been tampered with!"}, status=400)

        return super().get(request, *args, **kwargs)

    
def news_list_view(request):
    return render(request, "news_list.html")


def add_news_view(request):
    return render(request, "add_news.html")


def news_detail_view(request, news_id):
    return render(request, "news_detail.html", {"news_id": news_id})



class UserNewsFeedAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_posts, resident_news, assigned_news = News.get_news_for_user(user)

        return Response({
        "user_posts": NewsListSerializer(user_posts, many=True, context={'request': request}).data,
        "resident_news": NewsListSerializer(resident_news, many=True, context={'request': request}).data,
        "assigned_news": NewsListSerializer(assigned_news, many=True, context={'request': request}).data,
    })

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import News
import json

@csrf_exempt
@require_POST
def filter_news_by_location(request):
    try:
        print("Starting filter_news_by_location...")
        data = json.loads(request.body)
        print(f"Received data: {data}")
        
        district_name = data.get('district')
        city_village_name = data.get('city_village')
        
        print(f"District name from request: {district_name}")
        print(f"City/Village name from request: {city_village_name}")
        
        # First try to find exact district match
        if district_name:
            print(f"Attempting to find district: {district_name}")
            try:
                district = District.objects.get(name__iexact=district_name)
                print(f"Found district: {district.id} - {district.name}")
                
                nearby_news = News.objects.filter(
                    district=district,
                    is_public=True,
                    is_deleted=False
                ).order_by('-created_at')[:50]
                
                print(f"Found {nearby_news.count()} news items for district")
                
                if nearby_news.exists():
                    print("Returning news filtered by district")
                    return serialize_news_response(nearby_news)
                else:
                    print("No news found for this district")
            except District.DoesNotExist:
                print(f"District not found: {district_name}")
                pass
        
        # Fallback to city/village if no district matches
        if city_village_name:
            print(f"Attempting to find city/village: {city_village_name}")
            try:
                city_village = CityVillage.objects.get(name__iexact=city_village_name)
                print(f"Found city/village: {city_village.id} - {city_village.name}")
                
                nearby_news = News.objects.filter(
                    city_village=city_village,
                    is_public=True,
                    is_deleted=False
                ).order_by('-created_at')[:50]
                
                print(f"Found {nearby_news.count()} news items for city/village")
                
                if nearby_news.exists():
                    print("Returning news filtered by city/village")
                    return serialize_news_response(nearby_news)
                else:
                    print("No news found for this city/village")
            except CityVillage.DoesNotExist:
                print(f"City/Village not found: {city_village_name}")
                pass
        
        print("No matching location found, returning empty array")
        return JsonResponse({'news': []})
    
    except Exception as e:
        print(f"Error in filter_news_by_location: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)

def serialize_news_response(news_queryset):
    print("Serializing news response...")
    serialized_news = []
    
    for news in news_queryset:
        print(f"Processing news item ID: {news.id}")
        
        photo_url = news.photo.url if news.photo else None
        video_url = news.video.url if news.video else None
        creator_name = news.created_by.get_full_name()
        
        print(f"News details - ID: {news.id}, Creator: {creator_name}, "
              f"Photo: {'Exists' if photo_url else 'None'}, "
              f"Video: {'Exists' if video_url else 'None'}")
        
        serialized_news.append({
            'id': news.id,
            'content': news.content,
            'photo': photo_url,
            'video': video_url,
            'creator_name': creator_name,
            'creator_role': news.role,
            'created_at': news.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'blockchain_txn_id': news.blockchain_txn_id,
            'is_public': news.is_public
        })
    
    print(f"Serialized {len(serialized_news)} news items")
    return JsonResponse({'news': serialized_news})