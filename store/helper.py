from books.models import Book

class SessionCartManager:
    kname = 'cart'

    @staticmethod
    def _make_unit(book_pk, quantity=1):
        return {'book_pk': int(book_pk), 'quantity': int(quantity)}

    @staticmethod
    def add_unit(lis_cart, book_pk, quantity=1):
        if lis_cart is None:
            lis_cart = []

        book_pk = int(book_pk)
        quantity = int(quantity)
        for cart_unit in lis_cart:
            if cart_unit['book_pk'] == int(book_pk):
                cart_unit['quantity'] += quantity
                return lis_cart
        lis_cart.append(SessionCartManager._make_unit(book_pk, quantity))
        return lis_cart

    @staticmethod
    def delete_unit(lis_cart, book_pk):
        if lis_cart is None:
            return []

        book_pk = int(book_pk)
        for cart_unit in lis_cart:
            if cart_unit['book_pk'] == book_pk:
                lis_cart.remove(cart_unit)
                break  # 削除後はループを抜ける
        return lis_cart if lis_cart is not None else []  # もしlis_cartがNoneなら空のリストを返す

    @staticmethod
    def to_rendered(lis_cart):
        return [{'book': Book.objects.get(pk=cart_unit['book_pk']).name,
                 'quantity': cart_unit['quantity'],
                 'book_pk': cart_unit['book_pk']}
                for cart_unit in lis_cart]
