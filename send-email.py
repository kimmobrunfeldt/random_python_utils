# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText


me = 'my.name@gmail.com'
you = 'other.guy@gmail.com'

text = """Test mail

Testing stuff
"""

# Create a text/plain message
msg = MIMEText(text)

# me == the sender's email address
# you == the recipient's email address
msg['Subject'] = 'My mail subject'
msg['From'] = me
msg['To'] = you
msg['Cc'] = me

# Send the message
s = smtplib.SMTP('smtp.dnainternet.net')
s.sendmail(me, [you], msg.as_string())
s.quit()
