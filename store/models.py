from django.conf import settings
from django.db import models
from books.models import Book 
from django.core.validators import MinValueValidator

class CartUnit(models.Model):
    book = models.ForeignKey(to=Book, verbose_name='書籍', on_delete=models.CASCADE, blank=False)
    quantity =models.PositiveIntegerField('購入数',default =1,blank = False, validators=[MinValueValidator(1, )])

    def __str__(self):
        return '{}:{}'.format(self.book.name, self.quantity)


class Cart(models.Model):    
    units = models.ManyToManyField(to=CartUnit, verbose_name='ユニット', blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_carts',null=True)
    @property
    def total_price(self):
        """:returns total price of books in a cart"""
        each_books_price = [unit.book.price * unit.quantity for unit in self.units.all()]
        return sum(each_books_price)

    def add_unit(self, unit_add):
        """CartUnitをカートに追加する際に呼び出す。
        既に同じ種類の本がカートに存在する際は、個数を足し算するようにする。
        """
        if unit_add.book in [unit.book for unit in self.units.all()]:
            unit_origin = self.units.get(book_id=unit_add.book.id)
            unit_origin.quantity += unit_add.quantity
            unit_origin.save()
        else:
            unit_add.save()
            self.units.add(unit_add)

    def _add_session_unit(self, book_pk, quantity):
        """Session CartのカートユニットをModel CartのCartUnitに変換した上で、追加する。
        既に同じ種類の本がカートに存在する際は、個数を足し算するようにする。
        """
        book_pk = int(book_pk)
        if book_pk in [unit.book.pk for unit in self.units.all()]:
            unit_origin = self.units.get(book_id=book_pk)
            unit_origin.quantity += quantity
            unit_origin.save()
        else:
            unit_add = CartUnit(book=Book.objects.get(pk=book_pk), quantity=quantity)
            unit_add.save()
            self.units.add(unit_add)

    def import_session(self, session_cart):
        """Session Cartの中身をすべてモデルカートに移す"""
        for cart_unit in session_cart:
            self._add_session_unit(cart_unit['book_pk'], cart_unit['quantity'])

    def __str__(self):
        # return "{}'s model cart".format(self.user.username)
        return "{}'s model cart".format(self.id)
    

# Create your models here.
