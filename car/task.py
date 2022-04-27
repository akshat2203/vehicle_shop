from celery import Celery
from django.core.mail import EmailMessage

# Celery Settings
from vehicle_shop.celery import app


@app.task()
def send_mail(message, to_email):
    try:
        print("hello122")
        mail_subject = 'Vehicle Details.'

        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        print("hello")
        print('#### >>>>>>>>>>>>>>>>>>>>>>>> Email has been sent successfully to %s !!' % to_email)
    except Exception as err:
        print('#### >>>>>>>>>>>>>>>>>>>>>>>> Error in sending email to %s.' % to_email)
        print(err)
