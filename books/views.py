from django.views.generic import ListView
from .models import Book,GoodsGroup
from .forms import GroupCreationForm,BookCreateForm,BookSearchForm
from .forms import Book
from django.shortcuts import render
from django.views import generic
from store.forms import CartUnitForm
from django.views.generic.edit import ModelFormMixin
  
class BookList(ListView):
   model = Book
   form_class = BookSearchForm
   template_name = 'books/book_list.html'
   paginate_by = 5
   ordering = ['id']  # 例えば、idで昇順にソート

   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        q_name = self.request.GET.get('name')
        q_group = self.request.GET.get('group')

        context['form'] = BookSearchForm(initial={'name': q_name, 'group': q_group})
        context['query_string'] = self.request.GET.urlencode()

        return context
   
   def get_queryset(self):
      queryset = Book.objects.all().select_related('group')
      q_name = self.request.GET.get('name')
      q_group = self.request.GET.get('group')

      if q_name:
         queryset = queryset.filter(name__icontains=q_name)
      if q_group:
         queryset = queryset.filter(group=q_group)
      
      return queryset



class GroupCreateView(generic.CreateView):
   model = GoodsGroup
   success_url = '/'
   template_name = 'books/group_create.html'
   form_class = GroupCreationForm

class BookCreateView(generic.CreateView):
   model = Book
   success_url = '/'
   template_name = 'books/goods_create.html'
   form_class = BookCreateForm

class BookDetail(ModelFormMixin,generic.DetailView):
    model = Book
    template_name = 'books/detail.html'
    context_object_name = 'book'
    form_class = CartUnitForm

    def form_valid(self, form):
        return render(self.request, 'book/detail.html', {'form': form})


    
