from django.utils.text import slugify

from .models import Organization


def unique_org_slug(base):
    slug = slugify(base) or 'org'
    candidate = slug
    suffix = 1
    while Organization.objects.filter(slug=candidate).exists():
        suffix += 1
        candidate = f'{slug}-{suffix}'
    return candidate
