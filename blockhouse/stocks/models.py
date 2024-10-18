from django.db import models

# Create your models here.
class StockData(models.Model):
    symbol = models.CharField(max_length=10)
    date = models.DateField()
    open_price = models.DecimalField(max_digits=10, decimal_places=3)
    close_price = models.DecimalField(max_digits=10, decimal_places=3)
    high_price = models.DecimalField(max_digits=10, decimal_places=3)
    low_price = models.DecimalField(max_digits=10, decimal_places=3)
    volume = models.BigIntegerField()

    class Meta:
        unique_together = ('symbol', 'date')
        ordering = ['-date']

    def __str__(self):
        return f'{self.symbol} - {self.date}'