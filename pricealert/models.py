from django.db import models
import datetime

# Create your models here.
class PriceAlert(models.Model):

    SYMBOL = (
        ('EURUSD','EURUSD'),
        ('USDJPY','USDJPY'),
        ('GBPUSD','GBPUSD'),
        ('USDCHF','USDCHF'),
        ('EURCHF','EURCHF'),
        ('AUDUSD','AUDUSD'),
        ('USDCAD','USDCAD'),
        ('NZDUSD','NZDUSD'),
        ('EURJPY','EURJPY'),
        ('GBPJPY','GBPJPY'),
        ('EURGBP','EURGBP'),
        ('CHFJPY','CHFJPY'),
        ('GBPCHF','GBPCHF'),
        ('EURAUD','EURAUD'),
        ('EURCAD','EURCAD'),
        ('AUDCAD','AUDCAD'),
        ('AUDJPY','AUDJPY'),
        ('CADJPY','CADJPY'),
        ('NZDJPY','NZDJPY'),
        ('GBPAUD','GBPAUD'),
        ('AUDNZD','AUDNZD'),
        ('AUDCHF','AUDCHF'),
        ('EURNZD','EURNZD'),
        ('USDHKD','USDHKD'),
        ('USDMXN','USDMXN'),
        ('GBPNZD','GBPNZD'),
        ('USDSEK','USDSEK'),
        ('EURSEK','EURSEK'),
        ('EURNOK','EURNOK'),
        ('USDNOK','USDNOK'),
        ('USDZAR','USDZAR'),
        ('GBPCAD','GBPCAD'),
        ('USDTRY','USDTRY'),
        ('EURTRY','EURTRY'),
        ('NZDCHF','NZDCHF'),
        ('CADCHF','CADCHF'),
        ('NZDCAD','NZDCAD'),
        ('US30','US30'),
        ('SPX500','SPX500'),
        ('NAS100','NAS100'),
        ('UK100','UK100'),
        ('GER30','GER30'),
        ('ESP35','ESP35'),
        ('FRA40','FRA40'),
        ('HKG33','HKG33'),
        ('JPN225','JPN225'),
        ('AUS200','AUS200'),
        ('USOil','USOil'),
        ('UKOil','UKOil'),
        ('XAUUSD','XAUUSD'),
        ('XAGUSD','XAGUSD'),
        ('USDOLLAR','USDOLLAR'),
        ('USDILS','USDILS'),
        ('TRYJPY','TRYJPY'),
        ('USDCNH','USDCNH'),
        ('NGAS','NGAS'),
        ('Copper','Copper'),
        ('EUSTX50','EUSTX50'),
        ('Bund','Bund'),
    )
    symbol = models.CharField(max_length=15, choices=SYMBOL, null=False) 
    effective_date = models.DateTimeField('Effective Date', default=datetime.datetime.now, editable=True)
 
    QUOTE = (
        ('Bid', 'Bid'),
        ('Ask', 'Ask'),
        ('High', 'High'),
        ('Low', 'Low'),
    )
    quote = models.CharField(max_length=8, choices=QUOTE, null=False) 
    
    COMPARATOR = (
        ('>', '>'),
        ('>=', '>='),
        ('<', '<'),
        ('<=', '<='),
    )
    comparator = models.CharField(max_length=3, choices=COMPARATOR, null=False) 
    
    price_operand = models.DecimalField(max_digits=12, decimal_places=6, null=False)
    
    alert_note = models.CharField(max_length=150, null=True)
    alert_date = models.DateTimeField('alert date', editable=False, null=True)
    alert_price = models.DecimalField(max_digits=12, editable=False, decimal_places=6, null=True)
    
    STATUS = (
        ('0', 'Inactive'),
        ('1', 'Active'),
        ('2', 'Alerted'),
    )
    
    alert_status = models.CharField(max_length=1, choices=STATUS, default='1', null=False)

    def get_message(self):
        return "<b>Alert:</b> " + str(self.symbol) + " - " + self.quote + " " + self.comparator + " " + str(self.price_operand) + "\n" + "Note: " + self.alert_note + ", " + self.get_alert_status_display() + ""
    
    def __str__(self):
        return "Alert: " + str(self.symbol) + " - " + self.quote + " " + self.comparator + " " + str(self.price_operand) + " (Note: " + self.alert_note + ", " + self.get_alert_status_display() + ")"
