from rest_framework.serializers import CharField, ModelSerializer, SerializerMethodField, CurrentUserDefault, HiddenField, ValidationError

from core.models import Compra, ItensCompra

class ItensCompraCreateUpdateSerializer(ModelSerializer):
    
    class Meta:
        model = ItensCompra
        fields = ('livro', 'quantidade', 'preco')
    
    def validate_quantidade(self, quantidade):
        if quantidade <= 0:
            raise ValidationError('A quantidade deve ser maior do que zero.')
        return quantidade
    def validate(self, item):
        if item['quantidade'] > item['livro'].quantidade:
            raise ValidationError('Quantidade de itens maior do que a quantidade em estoque.')
        return item
    
class CompraCreateUpdateSerializer(ModelSerializer):
    itens = ItensCompraCreateUpdateSerializer(many=True)
    HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Compra
        fields = ('usuario', 'itens')
        
    def update(self, compra, validated_data):
        itens = validated_data.pop('itens')
        if itens:
            compra.itens.all().delete()
            for item in itens:
                item['preco'] = item['livro'].preco  
                ItensCompra.objects.create(compra=compra, **item)
        compra.save()
        return super().update(compra, validated_data)
    
class ItensCompraSerializer(ModelSerializer):
    total = SerializerMethodField()
    def get_total(self, instance):
        return instance.quantidade * instance.preco
    class Meta:
        model = ItensCompra
        fields = ('livro', 'quantidade', 'total', 'preco')
        
class CompraSerializer(ModelSerializer):
    total = SerializerMethodField()
    status = CharField(source='get_status_display', read_only=True)
    usuario = CharField(source='usuario.e-mail', read_only=True) 
    itens = ItensCompraSerializer(many=True, read_only=True)
    depth = 1

    class Meta:
        model = Compra
        fields = ('id', 'usuario', 'status', 'total', 'itens')
        read_only_fields = ['id', 'usuario', 'status']
        
    def get_total(self, obj):
        return obj.total
class ItensCompraListSerializer(ModelSerializer):
    livro = CharField(source='livro.titulo', read_only=True)

    class Meta:
        model = ItensCompra
        fields = ('quantidade', 'livro' 'preco')
        depth = 1        
        
class CompraListSerializer(ModelSerializer):
    usuario = CharField(source='usuario.email', read_only=True)
    itens = ItensCompraListSerializer(many=True, read_only=True)

    class Meta:
        model = Compra
        fields = ('id', 'usuario', 'itens')



