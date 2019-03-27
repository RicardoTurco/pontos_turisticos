from django.http import HttpResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from core.models import PontoTuristico
from .serializers import PontoTuristicoSerializer


class PontoTuristicoViewSet(ModelViewSet):
    #queryset = PontoTuristico.objects.all()
    serializer_class = PontoTuristicoSerializer

    # utilizando o "Search Fielter"
    filter_backends = (SearchFilter,)

    permission_classes = (AllowAny,)
    authentication_classes = (TokenAuthentication,)

    search_fields = ('nome','descricao', 'endereco__linha1')  # fará a busca no campo "linha1" de endereco
    #search_fields = ('nome','descricao')

    # ao utilizar "", alteramos o comportamento padrão da busca,
    # não fica mais por ID e sim o campo informado ...
    # ex: http://localhost:8000/pontosturisticos/XXX   (ao invés de filtrar por ID, será por NOME ...)
    # poderá ocorrer um erro, se existirem mais de 1 registro ...
    lookup_field = 'id'


    # o método abaixo, substitui a variável "queryset" ...
    def get_queryset(self):                                          # filtra registros ...

        # podemos passar os parâmetros esperados ...
        # esses parâmetros são "passados" diretamente na URL ... (queryStrings)
        # EX: http://localhost:8000/pontosturisticos/?id=3&nome=XXX&descricao=KDKDKDKDK
        id = self.request.query_params.get('id', None)
        nome = self.request.query_params.get('nome', None)
        descricao = self.request.query_params.get('descricao', None)
        queryset = PontoTuristico.objects.all()

        if id:
            queryset = queryset.filter(id=id)

        if nome:
            queryset = queryset.filter(nome__iexact=nome)   # usando "__iexact" o filtro fica CASE INSENSITIVE
            #queryset = queryset.filter(nome=nome)

        if descricao:
            queryset = queryset.filter(descricao__iexact=descricao)   # usando "__iexact" o filtro fica CASE INSENSITIVE
            #queryset = queryset.filter(descricao=descricao)

        return queryset
        #return PontoTuristico.objects.filter(aprovado=True)    # filtro definido FIXO no método ...


    def list(self, request, *args, **kwargs):                       # Lista TODOS os registros
        #return Response({'teste': 123})
        return super(PontoTuristicoViewSet, self).list(request, *args, **kwargs)             # Herda a "super-classe" do método padrão ...


    def create(self, request, *args, **kwargs):                      # Insere registro ...
        #return Response({'Hello': request.data['nome']})
        return super(PontoTuristicoViewSet, self).create(request, *args, **kwargs)           # Herda a "super-classe" do método padrão ...


    def destroy(self, request, *args, **kwargs):                     # Deleta registro ...
        return super(PontoTuristicoViewSet, self).destroy(request, *args, **kwargs)          # Herda a "super-classe" do método padrão ...


    def retrieve(self, request, *args, **kwargs):                    # Lista registro por ID ...
        return super(PontoTuristicoViewSet, self).retrieve(request, *args, **kwargs)         # Herda a "super-classe" do método padrão ...


    def update(self, request, *args, **kwargs):                      # Atualiza TODOS os campos do registro ...
        return super(PontoTuristicoViewSet, self).update(request, *args, **kwargs)           # Herda a "super-classe" do método padrão ...


    def partial_update(self, request, *args, **kwargs):              # Atualiza SOMENTE os campos que forem "passados" no body da request (data)
        return super(PontoTuristicoViewSet, self).partial_update(request, *args, **kwargs)   # Herda a "super-classe" do método padrão ...

    # implementa um método PERSONALIZADO para "T O D O " o recurso (detail=False) ...
    # ex: http://localhost:8000/pontosturisticos/teste
    @action(methods=['get'], detail=False)
    def teste(self, request):
        pass

    # implementa um método PERSONALIZADO para um registro específico (ID) - (detail=True) ...
    # ex: http://localhost:8000/pontosturisticos/1/denunciar
    @action(methods=['get'], detail=True)
    def denunciar(self, request, pk=None):
        pass

    @action(methods=['post'], detail=True)
    def associa_atracoes(self, request, id):
        atracoes = request.data['ids']

        ponto = PontoTuristico.objects.get(id=id)

        ponto.atracoes.set(atracoes)

        ponto.save()
        return HttpResponse('OK')
