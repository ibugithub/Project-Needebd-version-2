from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
import os
from twilio.rest import Client

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(user.is_active))


generate_token = TokenGenerator()




account_sid = "AC3ef1725fbf53d9a32e97e809f5573704"
auth_token = "738351b12caa70bd1df252c640b951e3"
client = Client(account_sid, auth_token)

def send_sms(user_code, phone_number):
    message = client.messages.create(
                                body=f'Hi! Your Verification code is {user_code}',
                                from_='+16178301515',
                                to=f'{phone_number}'
                            )

    print(message.sid)