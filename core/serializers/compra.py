from rest_framework.serializers import CharField, ModelSerializer

from core.models import Compra, ItensCompra

class ItensCompraSerializer(ModelSerializer):
    class Meta:
        model = ItensCompra
        fields = '__all__'
        
class CompraSerializer(ModelSerializer):
    status = CharField(source='get_status_display', read_only=True)
    usuario = CharField(source='usuario.e-mail', read_only=True) 
    itens = ItensCompraSerializer(many=True, read_only=True)

    
    class Meta:
        model = Compra
        fields = '__all__'
        read_only_fields = ['id', 'usuario', 'status']