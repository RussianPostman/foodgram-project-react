from rest_framework import mixins, viewsets

from .models import Tag, Recipe
from .serializers import TegSerializer, RecipeCreate


class TegViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TegSerializer


class RecipeWiewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeCreate
