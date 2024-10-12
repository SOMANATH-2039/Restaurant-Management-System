from django.db import models

class Category(models.Model):
    name= models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural='categories'

class MenuItems(models.Model):
    name=models.CharField(max_length=100)
    price=models.DecimalField(default=0,decimal_places=2,max_digits=9)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    description=models.CharField(max_length=250,default='',blank=True,null=True)
    image=models.ImageField(upload_to='upload/menuitems/')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural="Menu Items"