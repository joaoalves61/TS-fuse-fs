#!/usr/bin/env python
# coding=utf-8

import webbrowser
import smtplib
import random
import string
import sys

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

if(len(sys.argv)!=3) :
    sys.exit("Argumentos inválidos")

fromaddr = "fabionarcos88@gmail.com"
toaddr = sys.argv[1]

msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "FileSystem - Código de Validação"
 
body = "Insira este código na aplicação, para ter acesso ao FileSystem:\n" + sys.argv[2]

msg.attach(MIMEText(body, 'plain'))
 
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "Escapes-")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()

webbrowser.open('http://localhost:12345')