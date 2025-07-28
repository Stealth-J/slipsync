from django.db import models
from .market_parser import *

# Create your models here.
class Market(models.Model):
    name = models.CharField(max_length=100)  
    b9_identifier = models.CharField(max_length=100, null=True, blank=True)  
    sporty_id = models.CharField(max_length=50, null=True, blank=True) 
    parser_function = models.CharField(max_length=100, null=True, blank=True)  

    def __str__(self):
        return self.name
    
    # def parse(self, data):
    #     parser_fn = get_parser(self.parser_function)
    #     return parser_fn(data)





# class Error(models.Model):
#     text = models.CharField()
#     type = models.CharField(max_length = 30)