from django.db import models
from django.contrib.auth.models import AbstractUser

def upload_image_to(instance, filename):
    return f"images/{filename}"

# 

class User(AbstractUser):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    # DjangoのでファルとUserモデルとの競合を防ぐため、related_nameを追加した
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",  
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions_set",  
        blank=True
    )

# 注文時に使用する住所モデル（ユーザー情報とは別管理）
class Address(models.Model):
    # user_idを外部キーに設定し、userが消えたらアドレスも消える設定
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_code = models.CharField(max_length=10)
    address = models.TextField()
    name = models.CharField(max_length=100)
    telephone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.post_code}) - {self.address}" 


# 商品情報モデル
class Item(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=upload_image_to, blank=True, null=True)
    price = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)
    information = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    # templatesのitem_detailで呼び出している
    def get_stock(self):
        stock_entry = Stock.objects.filter(item=self).first()
        return stock_entry.quantity if stock_entry else 0
    
    def tax_price(self):
        return int(self.price * 1.1)

# 在庫情報モデル（Item と 1:1の関係）
class Stock(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.item.name} - {self.quantity}個"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def subtotal(self):
        return self.item.tax_price() * self.quantity

# 注文情報
class Order(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    total_price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"注文 {self.id} - {self.user.username} - {self.created_at.strftime('%Y-%m-%d')}"

# 注文商品情報
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    subtotal_price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

# 決済情報
class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    stripe_payment_id = models.CharField(max_length=255)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    





