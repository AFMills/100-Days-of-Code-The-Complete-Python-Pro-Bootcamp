import requests
import os
import smtplib

BOT_TOKEN = os.environ.get("BOT_TOKEN")
BOT_CHATID = os.environ.get("BOT_CHATID")

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.smtp_address = os.environ["EMAIL_PROVIDER_SMTP_ADDRESS"]
        self.email = os.environ["MY_EMAIL"]
        self.email_password = os.environ["MY_EMAIL_PASSWORD"]
        self.connection = smtplib.SMTP(self.smtp_address)

    # def send_emails(self, email_list, email_body):
    #     with self.connection:
    #         self.connection.starttls()
    #         self.connection.login(self.email, self.email_password)
    #
    #         for email in email_list:
    #             self.connection.sendmail(from_addr=self.email, to_addrs=email,
    #                                      msg=f"Subject:New Low Price Flight!\n\n{email_body}".encode('utf-8'))

def telegram_bot_send_text(bot_message):
    send_text = ("https://api.telegram.org/bot" + BOT_TOKEN + "/sendMessage?chat_id="
                 + BOT_CHATID + "&parse_mode=Markdown&text=" + str(bot_message))
    resp = requests.get(send_text)
    return resp.json()

def send_email(email_list, email_body):
    smtp_address = os.environ["EMAIL_PROVIDER_SMTP_ADDRESS"]
    email = os.environ["MY_EMAIL"]
    email_password = os.environ["MY_EMAIL_PASSWORD"]
    connection = smtplib.SMTP(smtp_address)
    with connection:
        connection.starttls()
        connection.login(email, email_password)
        for address in email_list:
            connection.sendmail(from_addr=email, to_addrs=address,
                                msg=f"Subject:New Low Price Flight!\n\n{email_body}".encode('utf-8'))

