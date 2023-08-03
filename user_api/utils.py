# utils.py

from random import randint
from twilio.rest import Client

# Generate OTP
def generate_otp():
    return str(randint(1000, 9999))  # Generate a 4-digit OTP

# Send OTP to user's mobile number
def send_otp_to_mobile(mobile, otp):
    # Implement your logic to send the OTP to the user's mobile number
    # This could involve using a third-party SMS gateway or service like Twilio
    # Here's an example using Twilio

    account_sid = 'YOUR_TWILIO_ACCOUNT_SID'
    auth_token = 'YOUR_TWILIO_AUTH_TOKEN'
    from_number = 'YOUR_TWILIO_PHONE_NUMBER'

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f'Your OTP is: {otp}',
        from_=from_number,
        to=mobile
    )

    print(message.sid)  # Optional: Print the Twilio message SID for reference
    
    
