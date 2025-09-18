# main/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Project
from .defaults import DEFAULT_FEATURES

@receiver(post_save, sender=Project)
def populate_default_features(sender, instance, created, **kwargs):
    if created:
        if not instance.features:
            instance.features = DEFAULT_FEATURES
            instance.save()