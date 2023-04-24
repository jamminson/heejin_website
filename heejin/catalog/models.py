from django.db import models
from django.urls import reverse

# Create your models here.

class Resin(models.Model):
    material_type = models.CharField(max_length=10, blank=True, null=True)
    client_name = models.ForeignKey('Client', on_delete=models.RESTRICT, blank=True, null=True)
    resin_name = models.CharField(max_length=50, primary_key=True)

    def get_absolute_url(self):

        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('resin-detail', args=[str(self.resin_name)])
    
    def __str__(self):
        return self.resin_name
    
    def get_stringed_product_list(self):
        q_set = self.product_set.all()

        l = []
        em = ", "
        for product in q_set:
            l.append(product.product_name)

        return em.join(l)

class Product(models.Model):
    client_name = models.ForeignKey('Client', on_delete=models.RESTRICT, blank=True, null=True)
    model = models.CharField(max_length=10, blank=True, null=True)
    product_code = models.CharField(max_length=50, blank=True, null=True)
    product_name = models.CharField(max_length=50, primary_key=True)
    machine_tonnage = models.CharField(max_length=10, blank=True, null=True)
    resin = models.ForeignKey('Resin', on_delete=models.RESTRICT, blank=True, null=True)
    cavity = models.CharField(max_length=10, blank=True, null=True)
    ct = models.CharField(max_length=20, blank=True, null=True)
    week_produce = models.CharField(max_length=10, blank=True, null=True)
    night_produce = models.CharField(max_length=10, blank=True, null=True)
    real_weight = models.CharField(max_length=10, blank=True, null=True)
    weight = models.CharField(max_length=10, blank=True, null=True)

    def get_absolute_url(self):

        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('product-detail', args=[str(self.product_name)])
    
    def __str__(self):
        return self.product_name
    
class Client(models.Model):
    client_name = models.CharField(max_length=50, primary_key=True)
    
    def get_absolute_url(self):

        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('model-detail-view', args=[str(self.client_name)])
    
    def get_stringed_client_list(self):

        """Returns a string of resin names separated by commas."""

        q_set = self.resin_set.all()

        l = []
        em = ", "
        for resin in q_set:
            l.append(resin.resin_name)
        return em.join(l)
    
    def get_stringed_product_list(self):
        q_set = self.product_set.all()

        l = []
        em = ", "
        for product in q_set:
            l.append(product.product_name)

        return em.join(l)

    def __str__(self):
        return self.client_name

class Order(models.Model):

    order_date = models.DateField(blank=True, null=True)
    product = models.ForeignKey('Product', on_delete=models.RESTRICT, blank=True, null=True)
    vol = models.IntegerField(default=0)
    notes = models.CharField(max_length=50, blank=True, null=True)

    def get_absolute_url(self):

        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('product-detail', args=[str(self.id)])

    def __str__(self):
        return str(self.id)
    
    class Meta:
        ordering = ["order_date"]

