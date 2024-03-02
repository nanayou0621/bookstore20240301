from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail
from store.models import Cart
from django.utils import timezone
from django.core.validators import MaxValueValidator
from books.models import Book


class CustomUserManager(BaseUserManager):
    use_in_migrations = True
 
    def _create_user(self, username, email, password, **extra_ﬁelds):
        if not username:
            raise ValueError('Users must have a username')
        if not email:
            raise ValueError('Users must have a email')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, cart=Cart.objects.create(), **extra_ﬁelds)
        user.set_password(password)
        user.save(using=self._db)
        return user
 
    def create_user(self, username, email, password, **extra_ﬁelds):
        extra_ﬁelds.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_ﬁelds)
 
    def create_superuser(self, username, email, password, **extra_ﬁelds):
        extra_ﬁelds.setdefault('is_superuser', True)
        extra_ﬁelds.setdefault('is_staff', True)
        if extra_ﬁelds.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username, email, password, **extra_ﬁelds)
 
    


# カスタムユーザーモデルを指定するクラス
class CustomUser(AbstractBaseUser,PermissionsMixin):
    username = models.CharField('ユーザー名', max_length=100,
          unique=True,
          error_messages={
              'unique': ("同じユーザー名が既に登録されています"),
           }, )
    
    address = models.CharField('住所', max_length=64, blank=True)
    email = models.EmailField('メールアドレス', unique=True,max_length=64)
    is_staff = models.BooleanField('スタッフ権限', default=False)
    password = models.CharField('パスワード', max_length=128)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)

    
    
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [EMAIL_FIELD]
     
 
    objects = CustomUserManager()
    
    is_received_email = models.BooleanField(verbose_name='お問い合わせメールを受け取るか', default=True)
 
    @staticmethod
    def get_users_emailed():
        return CustomUser.objects.filter(is_received_email=True)
 
    @staticmethod
    def email_users(users, subject, message, from_email=None):
        for user in users:
            send_mail(subject, message, from_email, [user.email])
            
    def __str__(self):
        return str(self.username)
    
class Purchase(models.Model):
    fk_user = models.ForeignKey(CustomUser, verbose_name ='ユーザー',on_delete =models.PROTECT)
    fk_book = models.ForeignKey(Book, verbose_name ='書籍',on_delete =models.PROTECT)
    purchase_time =models.DateTimeField('購入時刻',default=timezone.now)
    purchase_num = models.PositiveIntegerField('購入数',blank=False,validators=[MaxValueValidator(10),])
    state_flag = models.BooleanField('運用状況', default=True)

    def __str__(self):
        return str(self.fk_user) + ':' + str(self.fk_book)


