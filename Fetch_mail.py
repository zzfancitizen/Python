# -*- coding: utf_8 -*-

import poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import re
import codecs

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
            print('%s%s: %s' % ('  ' * indent, header, value))
            text = '%s%s: %s' % ('  ' * indent, header, value) + '\n'
            file.write(text)

    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            print('%spart %s' % ('  ' * indent, n))
            print('%s--------------------' % ('  ' * indent))
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
            print('%sText: %s' % ('  ' * indent, content + '...'))
            text = '%sText: %s' % ('  ' * indent, content + '...') + '\n'
            file.write(text)
        else:
            print('%sAttachment: %s' % ('  ' * indent, content_type))
            text = '%sAttachment: %s' % ('  ' * indent, content_type) + '\n'
            file.write(text)

server = poplib.POP3(pop3_server)

server.user(email)
server.pass_(password)

resp, mails, octets = server.list()

index = len(mails) - 10

for index in range(len(mails) - 10, len(mails)):
    resp, lines, octets = server.retr(index)
    msg_content = b'\r\n'.join(lines).decode('utf-8')
    msg = Parser().parsestr(msg_content)

    print_info(msg)

file.close()