from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Company, CompanyAdministrator

User = get_user_model()

@receiver(post_save, sender=Company)
def create_company_admin_for_new_company(sender, instance, created, **kwargs):
    if created:
        CompanyAdministrator.objects.create(user=instance.user, company=instance, is_company_admin=True)