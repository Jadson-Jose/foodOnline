from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O usuário deve ter um endereço de e-mail')
        
        if not username:
            raise ValueError('O usuáro deve ter um nome de usuário (username)')
            
        email = self.normalize_email(email)
        user = self.model(
            email = email,
            username = username,
            first_name = first_name,
            last_name = last_name,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        # user = self.create_user(
        #     email=self.normalize_email(email),
        #     username=username,
        #     password=password,
        #     first_name=first_name,
        #     last_name=last_name,
        # )
        # user.is_admin = True
        # user.is_active = True
        # user.is_staff = True
        # user.is_superadmin = True
        # user.save(using=self._db)
        # return user
        
        extra_fields.setdefault('username', 'admin')
        extra_fields.setdefault('first_name', 'Admin')
        extra_fields.setdefault('last_name', 'User')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_admin', True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError("O superusuário deve ter is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("O usuário deve ter is_superuser=True.")
        
        return self.create_user(email=email, password=password, **extra_fields)
        
    
    
class User(AbstractBaseUser, PermissionsMixin):
    RESTAURANT = 1
    CUSTOMER = 2
    
    ROLE_CHOICE = (
        (RESTAURANT, 'restaurant'),
        (CUSTOMER, 'customer'),
    )
    
    first_name = models.CharField(("primeiro nome"), max_length=50)
    last_name = models.CharField(("sobrenome"), max_length=50)
    username = models.CharField(("usuário"), max_length=50, unique=True)
    email = models.EmailField(("email"), max_length=100, unique=True)
    phone_number = models.CharField(("telefone"), max_length=12, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)
    
    # Required fields
    date_joined = models.DateTimeField(("data de adesão"), auto_now_add=True)
    created_date = models.DateTimeField(("data de criação"), auto_now=True)
    modified_date = models.DateTimeField(("data de modificação"), auto_now=True)
    is_admin = models.BooleanField(("admin"), default=False)
    is_staff = models.BooleanField(("staff"), default=False)
    is_active = models.BooleanField(("ativo"), default=False)
    is_superuser = models.BooleanField(("super usuário"), default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']
    
    objects = UserManager()
    
    def __str__(self) -> str:
        return self.email
    
    def has_perm(self, perm: str, obj=None) -> bool:
        return self.is_admin
    
    def has_module_perms(self, app_label: str) -> bool:
        return True
