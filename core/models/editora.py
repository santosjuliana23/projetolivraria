from django.db import models

from IPython.terminal.interactiveshell import black_reformat_handler

class Editora(models.Model):
    name = models.CharField(max_length=100)
    site = models.URLField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return f"({self.id}) {self.name}"