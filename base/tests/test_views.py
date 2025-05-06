from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from base.models import Item, Stock, Cart
from django.contrib.auth import get_user_model
User = get_user_model()

__all__ = ["TestIndexView"]

class TestIndexView(TestCase):

    # URLを取得し、client.get()でそのページをGETリクエストしている。その後ステータスコードが200かチェックしている。
    def test_index_view_status_code(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
    
    # ダミーデータを作成し、context（テンプレートに渡されるデータをチェックしている。
    # itemsとその個数が入っているか確認。
    def test_index_view_context_contains_items(self):

        #商品がテンプレートのcontextに正しく渡されるか確認するためのダミーアイテムを作成
        Item.objects.create(name="テスト商品", price=1000, information="説明")

        response = self.client.get(reverse('index'))
        self.assertIn("items", response.context)
        self.assertEqual(len(response.context["items"]), 1)
    
    def test_index_view_display_multiple_items(self):
        Item.objects.create(name="商品A", price=3000, information="テストAです。")
        Item.objects.create(name="商品B", price=5000, information="テストBです。")

        response = self.client.get(reverse('index'))
        # indexページのcontextに入っているitemsの数が、２個であることを確認している。
        self.assertEqual(len(response.context["items"]), 2)
        # 商品の名前で表示されているか確認している。
        self.assertQuerySetEqual(
            response.context["items"],
            ['商品A', '商品B'],
            # このコードはItemインスタンスから.nameのみを取り出すための関数。これでオブジェクトじゃなくて名前で比較できる。
            transform=lambda x: x.name,
            ordered=False
        )
    
    # item_detailビューがアイテム（商品）をテンプレートに渡しているか確認
    def test_item_detail_view_status_code(self):
        item = Item.objects.create(name="テスト商品", price=4000, information="テストです。")
        response = self.client.get(reverse("item_detail", args=[item.id]))
        self.assertEqual(response.status_code, 200)
    
    # コンテキストにitemが含まれているかのテスト
    def test_item_detail_view_context_contains_item(self):
        item = Item.objects.create(name="テスト商品", price=7000, information="テストの説明")
        response = self.client.get(reverse("item_detail", args=[item.id]))
        self.assertIn("item", response.context)
        self.assertEqual(response.context["item"], item)
    
    def test_item_detail_view_stock_item_range(self):
        item = Item.objects.create(name="テスト商品", price=6000, information="テストの商品です")
        Stock.objects.create(item=item, quantity=5)

        response = self.client.get(reverse("item_detail", args=[item.id]))

        self.assertIn("stock_item_range", response.context)
        self.assertEqual(list(response.context["stock_item_range"]), list(range(1, 6)))
    
    def test_add_to_cart_adds_item_to_session(self):
        user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")

        item = Item.objects.create(name="テスト商品", price=8000, information="テストです")
        Stock.objects.create(item=item, quantity=10)

        response = self.client.post(
            reverse("add_to_cart", args=[item.id]),
            {"quantity": 2},
            follow=True
        )

        # DBにCartオブジェクトが存在するか確認
        cart_item = Cart.objects.get(user=user, item=item)
        self.assertEqual(cart_item.quantity, 2)

        # メッセージの確認
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("カートに商品を追加しました" in str(message) for message in messages))