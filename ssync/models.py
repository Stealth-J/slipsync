from django.db import models
from datetime import timezone
from .market_parser import PARSER_FUNCTIONS, DICTIONARIES
from django.utils.timezone import now
from .countries import COUNTRY_CODES

# Create your models here.
class Platforms(models.TextChoices):
    BET9JA = 'bet9ja', 'Bet9ja'
    SPORTYBET = 'sportybet', 'SportyBet'



class Market(models.Model):
    name = models.CharField(max_length = 200)  
    b9_id = models.CharField(max_length = 100, null = True, blank = True)
    sporty_id = models.CharField(max_length = 50, null=True, blank=True) 
    
    b9_prefix = models.CharField(max_length=100, null=True, blank=True) 
    parser_function = models.CharField(max_length=100, null=True, blank=True)  

    def __str__(self):
        return self.name
    

class MarketParser(models.Model):
    market = models.ForeignKey(Market, on_delete = models.CASCADE, related_name= "parser_data")
    from_platform = models.CharField(max_length = 20, choices = Platforms.choices, null = True, blank = True)
    to_platform = models.CharField(max_length = 20, choices = Platforms.choices)
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
    specifier = models.CharField(max_length = 200, null = True, blank = True)

    def __str__(self):
        return f'{self.market.name} - {self.desc}'


class Tournament(models.Model):
    country = models.CharField(null = True, blank = True)
    b9_id = models.CharField(max_length = 50, null = True, blank = True)
    b9_name = models.CharField(max_length = 50, null = True, blank = True)
    sporty_id = models.CharField(max_length = 50, null = True, blank = True)
    sporty_name = models.CharField(max_length = 50, null = True, blank = True)

    def __str__(self):
        if self.sporty_name:
            return f'{self.sporty_name} - {self.country}'
        
        return self.b9_name


class NotSupportedMarket(models.Model):
    identifier = models.CharField()
    market_platform = models.CharField(max_length = 20, choices = Platforms.choices)
    name = models.CharField(null = True, blank = True)


class NotSupportedTournament(models.Model):
    country = models.CharField(null = True, blank = True)
    identifier = models.CharField()
    market_platform = models.CharField(max_length = 20, choices = Platforms.choices)
    tourney_name = models.CharField(null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return f'[{self.country[:3].upper()}]  {self.identifier} - {self.tourney_name} ({self.market_platform})'
    
    def country_avatar(self):
        country_name = self.country.lower().removesuffix('amateur').strip()
        code = COUNTRY_CODES.get(country_name)
        if code:
            return f'https://flagcdn.com/{code}.svg'
        
        return 'https://upload.wikimedia.org/wikipedia/commons/c/c4/Globe_icon.svg'
    


class Error(models.Model):
    error_type = models.CharField(max_length = 30)
    error_message = models.CharField()
    attempted_at = models.DateTimeField(auto_now_add = True)