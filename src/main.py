import imaplib
import email 
from email.header import decode_header 
import nltk
from nltk.corpus import stopwords
import nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
import heapq
import requests
from datetime import datetime, timedelta  
import os
from dotenv import load_dotenv 
import schedule
import time 
import logging
from textblob import TextBlob 
import base64

load_dotenv()

logging.basicConfig(filename='email_bot.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

nltk.download('punkt')
nltk.download('stopwords')

def connect_to_email(email_address, password, imap_server):
    try :
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_address, password)
        return mail 
    except Exception as e:
        logging.error(f"Error connecting to email : {str(e)}")
        return None 

def get_unread_emails(mail, num_emails=20):
    try:
        mails.select('inbox')
        _, search_data = mail.search(None, 'UNSEEN')
        email_ids = search_data[0].split()
        return email_ids[-num_emails:]
    except Exception as e:
        logging.error(f"Error getting unread emails : {str(e)}")
        return []

def get_email_content(mail, email_id):
    try :
        _, msg_data = mail.fetch(email_id, '{RFC822}')
        email_body = msg_data[0][1]
        message = email.message_from_bytes(email_body)

        subject = decode_header(message["subject"])[0][0]
        if isinstance(subject, bytes):
            subject = subject.decode()

        body = ""
        attachements = []

        if message.is_multipart():
            for part in message.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    body += part.get_payload(decode=True).decode()
                elif content_type.startswith("application/") or content_type.startswith("image/"):
                    filename = part.get_filename()
                    if filename:
                        attachements.append(filename)
        else:
            body = message.get_payload(decode = True).decode()

        return subject, body, attachements
    except Exception as e:
        logging,error(f"Error getting email content : {str(e)}")
        return None, None, []


