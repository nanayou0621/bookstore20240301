import urllib.parse
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView,TemplateView
from store.helper import SessionCartManager
from accounts.models import Cart
from django.http import HttpResponseRedirect
from django.contrib.auth import login
from accounts.forms import SignupForm

class Home(TemplateView):
    template_name ='accounts/home.html'

# ログインビューは Django のデフォルトのものを使用
class Login(LoginView):
    template_name = 'accounts/login.html'
    
    def get_success_url(self):
        try:
            session_cart = self.request.session[SessionCartManager.kname]
            self.request.user.cart.import_session(session_cart)
            del self.request.session[SessionCartManager.kname]
        except KeyError:
            return reverse_lazy('store:home')
        
        next_page = self.request.GET.get('next_page', 'home')
        print(next_page)
        if next_page == 'purchase':
            next_url = reverse_lazy('store:preview') + '?' + urllib.parse.urlencode(
                {'uname': self.request.user.username})
            return next_url
        else:
            return reverse_lazy('store:home')
        
# ログアウトビューもデフォルトのものを使用
class Logout(LogoutView):
    next_page = '/'
    

class SignUpView(CreateView):
    form_class = SignupForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy('accounts:signup_success')

    def form_valid(self, form):
        new_customUser = form.save(commit=False)
        new_customUser.save()
        new_customUser_cart = Cart.objects.create()  # 新しい Cart を作成
        new_customUser_cart = new_customUser_cart  # ユーザーに Cart を関連付ける
        new_customUser_cart.save()

        next_page = self.request.GET.get('next_page','home')
        if next_page =='purchase':
            session_cart = self.request.session.get(SessionCartManager.kname, [])

            login(self.request, new_customUser)

            new_customUser_cart.import_session(session_cart)
            del self.request.session[SessionCartManager.kname]  # この行の書き方を修正

            next_url = reverse_lazy('store:preview') + '?' + urllib.parse.urlencode(
                {'uname': self.request.user.username})
            return HttpResponseRedirect(next_url)
        else:
            return HttpResponseRedirect(self.success_url)

        
class SignUpSuccessView(TemplateView):
    template_name = "accounts/signup_success.html"




