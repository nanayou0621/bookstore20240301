from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.cache import never_cache
from books.models import Book
from store.helper import SessionCartManager
from accounts.helper import OnlyYouMixin,PostOnlyYouMixin
from accounts.models import CustomUser
from store.models import CartUnit
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import Purchase
from accounts.helper import GetOnlyYouMixin,PostOnlyYouMixin
from django import forms
from django.db.models import F, Sum
from .models import Cart


class Home(generic.ListView):
  template_name = 'store/home.html'

  def get_queryset(self):
        return Book.objects.all()

@method_decorator(never_cache,name ='dispatch')    
class SessionCartContent(generic.TemplateView):
    template_name ='store/content.html'

    def get_context_data(self):
        ctx =super().get_context_data()
        cart = self.request.session.get(SessionCartManager.kname,[])
        ctx['lis_cart'] = SessionCartManager.to_rendered(cart)
        return ctx

class SessionAddCart(generic.RedirectView):
    url = reverse_lazy('store:content')
 
    def post(self, request, *args, **kwargs):
        book_pk = request.POST.get('book_pk')
        quantity = request.POST['quantity']
        cart = request.session.get(SessionCartManager.kname, [])
        cart = SessionCartManager.add_unit(cart, book_pk, quantity)
        request.session[SessionCartManager.kname] = cart
        return super().post(request, *args, **kwargs)
    
class SessionCartDelete(generic.FormView):
    form_class = forms.Form
    success_url = reverse_lazy('store:content')
 
    def form_valid(self, form):
        cart = self.request.session[SessionCartManager.kname]
        deleting_book_pk = int(self.request.POST['book_pk'])
        cart = SessionCartManager.delete_unit(cart, deleting_book_pk)
        self.request.session[SessionCartManager.kname] = cart
        return super().form_valid(form)
   
# ModelCart(ログイン済み）

@method_decorator(never_cache, name='dispatch')
class ModelCartContent(OnlyYouMixin, generic.DetailView):
    model = CustomUser
    context_object_name = 'cart'
    template_name = 'store/content.html'
 
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        return obj.cart

   
class ModelAddCart(LoginRequiredMixin, generic.RedirectView):
    """CartUnitをカートに追加する。
    どのユーザのカートの追加するかは、サーバ側で決定しているので、OnlyYouMixinはいらない
    """
 
    def get_redirect_url(self):
        customUser_pk = self.request.user.pk
        return reverse_lazy('store:modelcontent', args=(customUser_pk,))
 
from django.db import transaction
from django.shortcuts import get_object_or_404

class ModelAddCart(LoginRequiredMixin, generic.RedirectView):

    
    def get_redirect_url(self):
        user_pk = self.request.user.pk
        return reverse_lazy('store:modelcontent', args=(user_pk,))

    def post(self, request, *args, **kwargs):
        with transaction.atomic():  # トランザクションを開始
            user = request.user

            # カートが存在しない場合は、新しいカートを作成してユーザーに関連付けます
            if not hasattr(user, 'cart') or user.cart is None:
                user.cart = Cart.objects.create()
                user.save()

            book_pk = request.POST.get('book_pk')
            quantity = request.POST.get('quantity')
            
            # 存在するBookオブジェクトを取得する
            book = get_object_or_404(Book, pk=book_pk)
            
            # カートにアイテムを追加
            user.cart.add_unit(CartUnit(book=book, quantity=int(quantity)))

        return super().post(request, *args, **kwargs)
           
               
       
class ModelCartDelete(PostOnlyYouMixin,generic.DeleteView):
   
   model=CartUnit

   def get_object(self,queryset = None):
      unit_pk =self.request.POST['unit_pk']
      return CartUnit.objects.get(id = unit_pk)
   
   def get_success_url(self):
      user_pk =self.request.user.pk
      return reverse_lazy('store:modelcontent',args=(user_pk,))


# Purchase
@method_decorator(never_cache, name ='dispatch')
class PurchasePreview(GetOnlyYouMixin,generic.TemplateView):
   template_name ='store/preview.html'

   def get_context_data(self, **kwargs):
      ctx = super().get_context_data(**kwargs)
      cart = self.request.user.cart
      total_price = cart.units.annotate(
      unit_price=F('book__price') * F('quantity')
      ).aggregate(
      total=Sum('unit_price')
      )['total'] or 0
      ctx['price'] = total_price
      return ctx
   def get_context_data(self, **kwargs):
        cart = self.request.user.cart
        ctx = super().get_context_data(**kwargs)
        ctx['total_price'] = cart.total_price
        return ctx
   
@method_decorator(never_cache, name='dispatch')
class PurchaseProcess(PostOnlyYouMixin, generic.FormView):
    """
    TemplateView ではpostは未実装。
    djangoのformは使わない
    """
    form_class = forms.Form
    success_url = reverse_lazy('store:done')

    def form_valid(self, form):
        user = self.request.user

        for unit in user.cart.units.all():
            Purchase.objects.create(fk_user=user, fk_book=unit.book, purchase_num=unit.quantity, state_flag=True)

        # 購入が完了したらカートをクリア
        user.cart.units.clear()

        return super().form_valid(form)
    
class PurchaseDone(generic.TemplateView):
    template_name = 'store/done.html'


