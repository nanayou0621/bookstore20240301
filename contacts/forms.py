from django.forms import ModelForm
from contacts.models import IndividualContact
 
class IndividualContactForm(ModelForm):
    class Meta:
        model = IndividualContact
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(IndividualContactForm, self).__init__(*args, **kwargs)
        self.fields['fullname'].label = '氏名'
        self.fields['kana'].label = 'フリガナ'
        self.fields['email'].label = 'メールアドレス'
        self.fields['content'].label = 'お問い合わせ内容'

        # フィールドの順序を設定
        self.order_fields(('fullname', 'kana', 'email', 'content'))
