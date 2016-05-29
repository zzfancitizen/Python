# -*- coding: utf_8 -*-

import poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart, MIMEBase
from email.utils import formataddr
import re
import codecs
import smtplib

# email = input('Email: ')
# password = input('Password: ')
# pop3_server = input('POP3 server: ')

email = 'zzfancitizen@163.com'
password = 'zz54142332'
pop3_server = 'pop.163.com'

file = codecs.open('/Users/zhangzhifan/Desktop/mail_log.txt', 'w', 'utf-8')

global text

def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset

def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value

def print_info(msg, indent=0):
    global value, hdr, addr
    if indent == 0:
        value = msg.get('From', '')
        hdr, addr = parseaddr(value)
        if re.match(r'\w+@sjtu.edu.cn', addr):
            pass
        else:
            return

        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header == 'Subject':
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            # print('%s%s: %s' % ('  ' * indent, header, value))
            text = '%s%s: %s' % ('  ' * indent, header, value) + '\n'
            file.write(text)

    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            # print('%spart %s' % ('  ' * indent, n))
            # print('%s--------------------' % ('  ' * indent))
            print_info(part, indent + 1)
            text = '%spart %s' % ('  ' * indent, n) + '\n'
            file.write(text)
            text = '%s--------------------' % ('  ' * indent) + '\n'
            file.write(text)
            text = '%s--------------------' % ('  ' * indent) + '\n'
            file.write(text)

    else:
        content_type = msg.get_content_type()
        if content_type=='text/plain' or content_type=='text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            # print('%sText: %s' % ('  ' * indent, content + '...'))
            text = '%sText: %s' % ('  ' * indent, content + '...') + '\n'
            file.write(text)
        else:
            # print('%sAttachment: %s' % ('  ' * indent, content_type))
            text = '%sAttachment: %s' % ('  ' * indent, content_type) + '\n'
            file.write(text)


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

server = poplib.POP3(pop3_server)

server.user(email)
server.pass_(password)

resp, mails, octets = server.list()

index = len(mails)

for index in range(1, len(mails)):
    resp, lines, octets = server.retr(index)
    msg_content = b'\r\n'.join(lines).decode('utf-8')
    msg = Parser().parsestr(msg_content)

    print_info(msg)

file.close()

server.close()

from_addr = email
to_addr = 'zzfancitizen@gmail.com'
smtp_server = 'smtp.163.com'

text = 'Dear' + '\n\n' + u'交大邮件通知,请查收附件。' + '\n\n' + 'best regards' + '\n' + 'Andy Zhang'

msg = MIMEMultipart()
msg['From'] = _format_addr('Andy Zhang <%s>' % from_addr)
msg['To'] = _format_addr('Gmail <%s>' % to_addr)
msg['Subject'] = Header(u'交大邮件通知', 'utf-8')

msg.attach(MIMEText(text, 'plain', 'utf-8'))

with codecs.open('/Users/zhangzhifan/Desktop/mail_log.txt', 'rb', encoding='utf-8') as f:
    mime = MIMEText(f.read())
    mime.add_header('Content-Disposition', 'attachment', filename='mail_log.txt')
    msg.attach(mime)

server = smtplib.SMTP(smtp_server, 25)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()