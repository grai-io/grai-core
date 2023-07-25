import strawberry

from .models import Organisation as OrganisationModel


@strawberry.django.type(OrganisationModel)
class Organisation:
    id: strawberry.auto
    name: strawberry.auto
