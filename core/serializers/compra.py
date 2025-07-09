from rest_framework.serializers import CharField, ModelSerializer, SerializerMethodField

from core.models import Compra, ItensCompra

class ItensCompraSerializer(ModelSerializer):
    total = SerializerMethodField()
    def get_total(self, instance):
        return instance.livro.preco * instance.quantidade
    class Meta:
        model = ItensCompra
        fields = ('livro', 'quantidade', 'total')
        
class CompraSerializer(ModelSerializer):
    status = CharField(source='get_status_display', read_only=True)
    usuario = CharField(source='usuario.e-mail', read_only=True) 
    itens = ItensCompraSerializer(many=True, read_only=True)
    depth = 1

    class Meta:
        model = Compra
        fields = ('id', 'usuario', 'status', 'total', 'itens')
        read_only_fields = ['id', 'usuario', 'status']