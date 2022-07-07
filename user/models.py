from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have an username')
        user = self.model(
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password=None):
        user = self.create_user(
            username = username,
            password = password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField("사용자 계정", max_length=20, unique=True, null=False, blank=False)
    password = models.CharField("비밀번호", max_length=256, null=False, blank=False)
    email = models.EmailField("이메일 주소", max_length=100, unique=True)
    phone = models.CharField(max_length=20, unique = True, null = False, blank = False)
    join_date = models.DateTimeField("가입일", auto_now_add=True)
    profile_img = models.ImageField(upload_to='static/user/profile_img', blank=True)
    user_type = models.CharField("회원 유형", max_length=10)
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label): 
        return True

    @property
    def is_staff(self): 
        return self.is_admin

