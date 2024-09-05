from django.template import Library
from django.http import HttpResponseForbidden
from django import template
from ..models import Company, CompanyAdministrator

register = Library()

@register.inclusion_tag('includes/dash-sidebar.html')
def sidebar_view(request):
    user = request.user
    try:
        company_admin = CompanyAdministrator.objects.get(user=user)
    except CompanyAdministrator.DoesNotExist:
        # User is not a company administrator, redirect or raise an error
        return HttpResponseForbidden("You are not authorized to access this dashboard.")

    company = company_admin.company
    context = {
        'company': company
    }

    return context
