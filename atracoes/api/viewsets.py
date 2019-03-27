from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.viewsets import ModelViewSet
from atracoes.models import Atracao
from .serializers import AtracaoSerializer


class AtracaoViewSet(ModelViewSet):
    queryset = Atracao.objects.all()
    serializer_class = AtracaoSerializer

    # o "DjangoFilterBackend" tb pode ser implementado
    # separadamente em cada um dos VIEWSETS, apenas removendo-se
    # o parâmetro "REST_FRAMEWORK" do settings
    filter_backends = (DjangoFilterBackend,)

    # o Django Filters, já foi implementado no "settings.py",
    # acrescentando-se o parâmetro "REST_FRAMEWORK"
    filter_fields = ('nome','descricao')
