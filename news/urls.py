from django.urls import path
from .views import *

urlpatterns = [
        path('api/news-list/', NewsListView.as_view(), name='news_list_api'),
    path('api/news-create/', NewsCreateView.as_view(), name='news_create_api'),
        path('api/news/<int:pk>/', NewsDetailView.as_view(), name='news_detail_api'),

        path('', news_list_view, name="news_list"),  # Home page (news list)
    path('news/add/', add_news_view, name="add_news"),  # Add news
    # path('news/<int:news_id>/', news_detail_view, name="news_detail"),  # News details

       path('home',home,name='home'),
   path('login',login,name='login'),
   path('signup/',register,name='register'),
   path('forgot/',forgot,name='forgot'),
   path('reset-pass/<str:token>/',resetpass,name='resetpass'),
   path('dashboard/', dashboard, name='dashboard'),
   path('api/dashboard/counts/', dashboard_counts, name='dashboard-counts'),
   path('my-news-feed/', UserNewsFeedAPIView.as_view(), name='my-news-feed'),
   path('filter-by-location/', filter_news_by_location, name='filter-by-location'),

   path('khabhar/', khabhar, name='khabhar'),
   path('ice/', pod, name='pod'),
   path('log/', log, name='log'),
   path('wifi/', wifi, name='wifi'),
   path('stream/', stream, name='stream'),
   path('profile/', profile, name='profile'),
   path('subscription/', subscription, name='subscription'),
   path('change_password/', change_password, name='changepass'),
   path('ice_detail/<int:device_id>/', pod_detail, name='pod_detail'),
   path('add-contact/', add_contact, name='add_contact'),
   path('evlogs/<int:event_id>/',     evlogs, name='evlogs'),
   path('subscription_txn/',subscription_txn,name='subscription_txn'),
   path('terms-and-conditions/', terms, name='terms'),
   path('terms-of-use/', termsOfuse, name='termsOfuse'),
   path('privacy-policy/', privacy, name='privacy'),
   path('sales-and-refund-policy/', salesandrefund, name='salesandrefund'),
   path('legal-information/', legalinfo, name='legalinfo'),
   path('order-now/', ordernow, name='ordernow'),
   path('tutorials/', tutorials, name='tutorials'),
   path('pricing-plans/', plan_pricing, name='plan_pricing'),
   path('case-study/', case_study, name='case_study'),
   path('how-it-works/', hiworks, name='hiworks'),
#    path('user_invoice/<int:transaction_id>/', user_invoice_view, name='user_invoice'),
   path('notifications/', notifications, name='notifications'),
   path('api/notifications/', NotificationListView.as_view() , name='notification'),
    path('api/notifications/<int:id>/read/', MarkNotificationAsReadView.as_view(), name='mark_notification_as_read'),
   path('test/', test, name='test'),
   path('api/password-reset-request/', PasswordResetRequestAPIView.as_view(), name='password-reset-requestapi-api'),
#  path('api/reset-pass/<str:token>/', PasswordResetConfirmAPIView.as_view(), name='reset-pass-api'),
   path('api/password-reset-confirm/<str:token>/', PasswordResetConfirmAPIView.as_view(), name='password-reset-confirm-api'),
   path('password-reset/<str:token>/', PasswordResetAPIView.as_view(), name='password-reset-api'),
   path('api/profile/',GetProfileAPIView.as_view(), name='profile-api'),
   path('api/profile/update/',UpdateProfileAPIView.as_view(), name='update-profile-api'),
   path('api/update-profile-image/', UpdateProfileImageAPIView.as_view(), name='update-profile-image'),
   path('api/change-password/',ChangePasswordAPIView.as_view(), name='change-password-api'),
#    path('unsubscribe/<uidb64>/<token>/',unsubscribe, name='unsubscribe'),
]
