from rest_framework import mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import Tag, Recipe
from .serializers import TegSerializer, RecipeCreate
from .permissions import AuthorIsRequestUserPermission


class TegViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TegSerializer


class RecipeWiewSet(viewsets.ModelViewSet):
    permission_classes = [AuthorIsRequestUserPermission]
    queryset = Recipe.objects.all()
    serializer_class = RecipeCreate
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author']
