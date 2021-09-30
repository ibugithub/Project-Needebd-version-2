from .models import User, Code
from django.db.models.signals import post_save
from django.dispatch import receiver
from coupons.models import Voucher, VoucherOffer
from django.core.exceptions import ObjectDoesNotExist


@receiver(post_save, sender= User)
def post_save_generate_code(sender, instance, created, *args, **kwargs):
    if created:
        Code.objects.create(user=instance)
        try:
            registrationoffer = VoucherOffer.objects.get(title = 'RegistrationOffer', active = True)
            if instance.timestamp > registrationoffer.offer_valid_from and instance.timestamp < registrationoffer.offer_valid_to:
                Voucher.objects.create(
                    user = instance, 
                    title = registrationoffer.title,
                    valid_from = registrationoffer.user_valid_from, 
                    valid_to =registrationoffer.user_valid_to, 
                    discount = registrationoffer.discount, 
                    condition_rate = registrationoffer.condition_rate,
                    limit          =  registrationoffer.limit
                    )  
        except: ObjectDoesNotExist
      