from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

# Auto create Profile -> when User is Created
@receiver (post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    # region agent log
    import json, time, os
    try:
        log_path = "/Users/mahadharoon/Desktop/django_projects/django4/myproject/debug.log"
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, "a") as f:
            now_ms = int(time.time() * 1000)
            f.write(
                json.dumps(
                    {
                        "id": f"log_{now_ms}_create_profile",
                        "timestamp": now_ms,
                        "runId": "pre-fix-1",
                        "hypothesisId": "H1",
                        "location": "users/signals.py:create_profile",
                        "message": "create_profile signal handler called",
                        "data": {
                            "user_id": getattr(instance, "id", None),
                            "created": created,
                        },
                    }
                )
                + "\n"
            )
    except Exception:
        # Debug logging must never break application logic
        pass
    # endregion agent log

    if created:
        Profile.objects.create(user=instance)

# Auto save User Instance like profile and image. when User is Saved.
@receiver (post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    # region agent log
    import json, time, os
    try:
        log_path = "/Users/mahadharoon/Desktop/django_projects/django4/myproject/debug.log"
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, "a") as f:
            now_ms = int(time.time() * 1000)
            f.write(
                json.dumps(
                    {
                        "id": f"log_{now_ms}_save_profile",
                        "timestamp": now_ms,
                        "runId": "pre-fix-1",
                        "hypothesisId": "H1",
                        "location": "users/signals.py:save_profile",
                        "message": "save_profile signal handler called",
                        "data": {
                            "user_id": getattr(instance, "id", None),
                        },
                    }
                )
                + "\n"
            )
    except Exception:
        # Debug logging must never break application logic
        pass
    # endregion agent log

    instance.profile.save()