from .models import UserLog

def log_event(user, message):
    """Log an event for the user."""
    UserLog.objects.create(user=user, log_message=message)

def password_changed(user):
    """Log Password changed event."""
    message = "Your account password has been successfully updated. If this change wasn’t made by you, please contact our support team immediately."
    log_event(user, message)
    
def password_reset(user):
    """Log Password reset event."""
    message = "Your Password Reset was successful."
    log_event(user, message)