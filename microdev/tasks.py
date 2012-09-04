#from celery.task import task


#@task(name="microdev.tasks.send_email")
def send_email(subject, body, from_address, to_address):
    from django.core.mail import EmailMessage
    
    msg = EmailMessage(subject, body, from_address, [to_address])
    msg.send(True)

    print('Sent message to: %s' % to_address)
    print('Sent message from: %s' % from_address)
    return 1
