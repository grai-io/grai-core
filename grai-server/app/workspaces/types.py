from strawberry_django_plus import gql
from strawberry_django_plus.gql import auto

from .models import Organisation as OrganisationModel


@gql.django.type(OrganisationModel)
class Organisation:
    id: auto
    name: auto
