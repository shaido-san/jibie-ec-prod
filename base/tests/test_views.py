from django.test import TestCase
from django.urls import reverse
from base.models import Item

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


        