import messagebird
from decouple import config

access_key = config('MESSAGEBIRD_ACCESS_KEY')
client = messagebird.Client(access_key)

def send_sms(phone: str, message: str):
    message = client.message_create(
          'BOOKIT',
          phone,
          message,
          { 'reference' : 'Foobar' }
      )
    return message