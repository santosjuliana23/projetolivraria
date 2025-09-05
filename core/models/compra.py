from django.db import models

from django.db.models.fields.related import ForeignKey

from .user import User
from .livro import Livro

class Compra(models.Model):
    class StatusCompra(models.IntegerChoices):
        CARRINHO = 1, "Carrinho"
        FINALIZADO = 2, "Realizado"
        PAGO = 3, "Pago"
        ENTREGUE = 4, "Entregue"

    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name="compras")
    status = models.IntegerField(choices=StatusCompra.choices,  default=StatusCompra.CARRINHO)

    def __str__(self):
        return f'Compra {self.id} - {self.get_status_display()} - {self.usuario.email}'
    @property
    def total(self):
        return sum(item.total for item in self.itens.all())
    
class ItensCompra(models.Model):
    compra = models.ForeignKey (Compra, on_delete= models.CASCADE, related_name="itens")
    livro = models.ForeignKey (Livro, on_delete= models.PROTECT, related_name="+")
    quantidade = models.IntegerField(default=1)
    preco = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    
    ...
    @property
    def total(self):
        # total = 0
        # for item in self.itens.all():
        #     total += item.livro.preco * item.quantidade
        # return total
       return self.preco * self.quantidade
