from django import forms
from .models import Book,GoodsGroup


class GroupCreationForm(forms.ModelForm):
  class Meta:
    model = GoodsGroup
    fields = '__all__'

class BookCreateForm(forms.ModelForm):
  class Meta:
    model = Book
    fields = ('name','management_code','price','description','image','group')
    

class BookSearchForm(forms.Form):
    group = forms.ModelChoiceField(queryset =GoodsGroup.objects,label ='グループ',required =False,empty_label = '選択してください')
    name = forms.CharField(label ='書籍名',required=False)
    
