from django.db import models

class GoodsGroup(models.Model):
    name = models.CharField(verbose_name='商品グループ', unique=True, max_length=10, null=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    name = models.CharField('書籍名', max_length=100, null=True)
    management_code = models.CharField(verbose_name='管理コード', unique=True, max_length=20, default='default_code')
    price = models.PositiveIntegerField('価格', blank=False,)
    description = models.CharField('説明', max_length=500,)
    image = models.ImageField('イメージ', null=True, blank=True, upload_to='goods_image/')
    group = models.ForeignKey(GoodsGroup, verbose_name='商品グループ', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        # return self.name+str(self.price)
        return self.name

class Category(models.Model):
    name = models.CharField('カテゴリー名', max_length=100)

    def __str__(self):
        return self.name