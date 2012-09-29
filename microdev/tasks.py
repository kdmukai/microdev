#from celery.task import task


#@task(name="microdev.tasks.send_email")
def send_email(subject, body, from_address, to_address, as_html=True):
    from django.core.mail import EmailMessage
    
    msg = EmailMessage(subject, body, from_address, [to_address])
    if as_html:
        msg.content_subtype = "html"  # Main content is now text/html
    msg.send(True)

    return 1
