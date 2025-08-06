from django.db import models
from .market_parser import PARSER_FUNCTIONS, DICTIONARIES

# Create your models here.
class Market(models.Model):
    name = models.CharField(max_length = 200)  
    b9_id = models.CharField(max_length = 100, null = True, blank = True)
    sporty_id = models.CharField(max_length = 50, null=True, blank=True) 
    
    b9_prefix = models.CharField(max_length=100, null=True, blank=True)  
    specifier = models.CharField(max_length = 200, null = True, blank = True)
    parser_function = models.CharField(max_length=100, null=True, blank=True)  

    def __str__(self):
        return self.name
    

class MarketParser(models.Model):
    PLATFORM_CHOICES = [
        ('bet9ja', 'Bet9ja'),
        ('betking', 'BetKing'),
        ('sportybet', 'SportyBet'),
        ('nairabet', 'NairaBet'),
    ]

    market = models.ForeignKey(Market, on_delete = models.CASCADE, related_name= "parser_data")
    from_platform = models.CharField(max_length = 20, choices = PLATFORM_CHOICES, null = True, blank = True)
    to_platform = models.CharField(max_length = 20, choices = PLATFORM_CHOICES)
    dictionary = models.CharField(null = True, blank = True)
    parser_func = models.CharField(max_length = 150)

    def __str__(self):
        return f'{self.to_platform} parser for {self.market.name}'

    def get_parser(self):
        parser_func = PARSER_FUNCTIONS.get(self.parser_func)
        return parser_func 
    
    def get_dict(self):
        if self.dictionary:
            dictionary = DICTIONARIES.get(self.dictionary)
            return dictionary
        
        return None


class Outcome(models.Model):
    market = models.ForeignKey(Market, on_delete= models.CASCADE, related_name= "outcomes")
    outcome_id = models.CharField(max_length = 100)
    desc = models.CharField(max_length = 300)

    def __str__(self):
        return f'{self.market.name} - {self.desc}'


# class Error(models.Model):
#     text = models.CharField()
#     type = models.CharField(max_length = 30)