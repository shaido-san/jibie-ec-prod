from django.contrib import admin
from .models import Item, Stock, Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "address", "total_price", "created_at")  # 一覧表示
    list_filter = ("created_at",)  # 作成日でフィルタリング
    search_fields = ("user__username", "address__name")  # 検索フィールド

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "item", "quantity", "subtotal_price")  # 一覧表示
    list_filter = ("order",)  # 注文ごとにフィルタリング
    search_fields = ("item__name",)  # 商品名で検索

class StockInline(admin.TabularInline):  # ← Stacked から Tabular に変更
    model = Stock
    extra = 1                # 追加フォームは0個（余計なの表示させない）
    max_num = 1              # 在庫は1つしか作れないようにする
    can_delete = False       # 削除ボタンも出さない（誤操作防止）


class ItemAdmin(admin.ModelAdmin):
    list_display = ["name", "get_stock", "created_at"]
    inlines = [StockInline]

    def get_stock(self, obj):
        stock = Stock.objects.filter(item=obj).first()
        return stock.quantity if stock else 0
    get_stock.short_description = "在庫"
    
admin.site.register(Item, ItemAdmin)
