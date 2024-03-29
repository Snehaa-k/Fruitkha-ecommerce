from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.core.validators import MaxValueValidator, MinValueValidator
from products.models import Products, Variant


# Create your models here.
class Usermodelss(models.Model):
    username = models.CharField(max_length=800)
    email = models.EmailField(max_length=254)
    phonenumber = models.BigIntegerField(
        validators=[
            MinValueValidator(
                limit_value=1000000000,
                message="Phone number must have at least 10 digits.",
            ),
            MaxValueValidator(
                limit_value=9999999999,
                message="Phone number must have at most 10 digits.",
            ),
        ]
    )
    password1 = models.IntegerField()
    password2 = models.IntegerField()
    otp = models.CharField(max_length=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_block = models.BooleanField(default=True)


def __str__(self):
    return self.username


def generate_otp(instance):
    otp = get_random_string(length=6, allowed_chars="1234567890")
  
    instance.otp = otp
    instance.save()

    subject = "Your OTP for Signup"
    message = f"Your OTP is {otp}. Enter this code to complete your signup."
    from_email = "snehaksnehak470@gmail.com"
    to_email = [instance.email]
    send_mail(subject, message, from_email, to_email)


@receiver(post_save, sender=Usermodelss)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        generate_otp(instance)


class Useraddress(models.Model):
    user_id = models.ForeignKey(Usermodelss, on_delete=models.CASCADE)
    Name = models.CharField(max_length=225)
    country = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    address = models.TextField()
    pin = models.BigIntegerField()
    post = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.BigIntegerField()
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Wishlist(models.Model):
    user_id = models.ForeignKey(Usermodelss, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    vaiant_id = models.ForeignKey(Variant, on_delete=models.CASCADE, null=True)


class Walletuser(models.Model):
    userid = models.ForeignKey(Usermodelss, on_delete=models.CASCADE)
    amountt = models.IntegerField(default=0)
