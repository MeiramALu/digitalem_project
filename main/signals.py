from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Project, ProjectFeature
from .defaults import DEFAULT_FEATURES

@receiver(post_save, sender=Project)
def populate_default_features(sender, instance, created, **kwargs):
    if created:
        if not instance.features.exists():
            for i, data in enumerate(DEFAULT_FEATURES):
                ProjectFeature.objects.create(
                    project=instance,
                    icon_class=data["icon_class"],
                    text_ru=data["text_ru"],
                    text_kk=data["text_kk"],
                    text_en=data["text_en"],
                    order=i
                )