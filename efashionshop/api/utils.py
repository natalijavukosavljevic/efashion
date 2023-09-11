from email.message import EmailMessage
import smtplib

from django.template.loader import render_to_string
def validate_password_strength(value):
    
    min_length = 7

    if len(value) < min_length:
        return(('Password must be at least {0} characters '
                                'long.').format(min_length))

    # check for digit
    if not any(char.isdigit() for char in value):
        return(('Password must contain at least 1 digit.'))

    # check for letter
    if not any(char.isalpha() for char in value):
        return(('Password must contain at least 1 letter.'))
    
    return ("OK")

def orderMail(data,customerEmail):
     #ovo treba u funkciju i staviti kod nonregistred order
    html_message = render_to_string('api/order.html', data)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # # start TLS for security
    s.starttls()
        
    # # Authentication
    s.login("vuknatcol@gmail.com", "xmnlwceyzoipkdnc")
    
    sender = "vuknatcol@gmail.com"
    recipient = customerEmail
  
    email = EmailMessage()
    email["From"] = sender
    email["To"] = recipient
    email["Subject"] = "Order"
    email.set_content(html_message, subtype="html")
    s.sendmail(sender, recipient, email.as_string())
    s.quit()

def mailToken(customerMail,customer):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    
    s.login("vuknatcol@gmail.com", "xmnlwceyzoipkdnc")
    text="Your security token is  " +customer.generateTemporaryToken() +" \nSincerely, Efashion team."
    message = 'Subject: {}\n\n{}'.format('Requested token', text)
    

    
    s.sendmail("vuknatcol@gmail.com", customerMail, message)
    
    s.quit()



