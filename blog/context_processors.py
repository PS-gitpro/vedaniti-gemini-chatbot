from django.conf import settings

def site_info(request):
    """
    Add site information to all templates
    """
    return {
        'SITE_NAME': getattr(settings, 'SITE_NAME', 'Django Blog'),
        'SITE_DESCRIPTION': getattr(settings, 'SITE_DESCRIPTION', 'A Django-powered blog'),
        'SITE_AUTHOR': getattr(settings, 'SITE_AUTHOR', 'Admin'),
    }