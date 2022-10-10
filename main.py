import imaplib 
import email 
from email.header import decode_header 
import os 


# account credentials
username = os.environ.get('GMAILADDRESS')
password = os.environ.get('GOOGLEAPPPASSWORD')

# set condition to delete
mailbox_where_to_delete_mail = str(os.environ.get('MAILBOX'))
address_to_delete = str(os.environ.get('ADDRESSOFMAILTODELETE'))
subject_to_delete = str(os.environ.get('SUBJECTOFMAILDELETE'))
date_since_to_delete = str(os.environ.get('DATESINCEOFMAILTODELETE'))
date_before_to_delete = str(os.environ.get('DATEBEFOREOFMAILTODELETE'))

# create an IMAP4 class with SSL
imap = imaplib.IMAP4_SSL("imap.gmail.com")
# imap.enable(UTF8=ACCEPT)
imap.login(username, password)

# select the mailbox where I want to delete 
imap.select(mailbox_where_to_delete_mail)
# imap.select("SPAM")

# search the specific mails by sender 
if (len(address_to_delete)>0):
    status, messages = imap.search(None, 'FROM "{}"'.format(address_to_delete))

# to get mails by subject 
if (len(subject_to_delete)>0):
    print("SUBJECT '{}'".format(subject_to_delete))
    print("SUBJECT %s" % u"{}".format(subject_to_delete).encode("utf-8"))
    # status, messages = imap.search("utf-8", 'SUBJECT "2022-10-06 Todo"')
    # status, messages = imap.search("utf-8", "SUBJECT %s" % u"{}".format(subject_to_delete).encode("utf-8"))
    status, messages = imap.search(None, 'SUBJECT "{}"'.format(subject_to_delete))
# to get mails after a specific date
if (len(date_since_to_delete)>0):
    status, messages = imap.search(None, 'SINCE "{}"'.format(date_since_to_delete))

# to get mails before a specific date
if (len(date_before_to_delete)>0):
    status, messages = imap.search(None, 'BEFORE "{}"'.format(date_before_to_delete))

# to get all mails
# if(False): status, messages = imap.search(None, "ALL")


# convert messages to a list of email_IDs
# messages = messages[0].split(b' ')
messages = messages[0].split()
print(messages)
for mail in messages:
    _, msg = imap.fetch(mail, "(RFC822)")
    # mark the mail as deleted 
    # imap.store(mail, "+FLAGS", "\\Deleted")
    imap.store(mail, "+X-GM-LABELS", "\\Trash")

# permanebtly remove mails that are marked as deleted
imap.expunge()
imap.close()
imap.logout()


