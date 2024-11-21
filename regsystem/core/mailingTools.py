from django.core.mail import EmailMessage

from django.template.loader import render_to_string

class MailPreProcessor:
    def pushMailMessage(self, mailInfo:list, recipients:list, mailType:int):
        # for invoice
        messageInfo = {
                        'name': mailInfo[0],
                        'message': mailInfo[1],

                        }            


        # format message
        formattedInfo = {
            'meta': messageInfo,
            'type': mailType

        }

        # alert
        MailingEngine().sendEmailMessage(emailInformation=formattedInfo, mailList=recipients)

        return


class MailingEngine:
    def __init__(self) -> None:
        pass


    
    def createEmailMessageAndBody(self, emailMeta:dict):
        # get the mail type
        # 1 - New message

        headingsMap = {
            1: '🥳 You have a new message from the administrator',  
        }


        # mail type
        emailType = emailMeta['type']

        # heading message
        emailHeading = headingsMap[emailType]

        # messages
        if emailType == 1:
            emailBody = render_to_string("mail/notification.html", emailMeta['meta'])

        else:
            pass

        return emailHeading, emailBody
    
    
    def sendEmailMessage(self, emailInformation:dict, mailList:list):
        emailHeading, emailBody = self.createEmailMessageAndBody(emailMeta=emailInformation)

        # print(emailHeading, emailBody)

        # create a new email message
        emailMessage = EmailMessage(emailHeading, emailBody, 'bse.group5.mailer@gmail.com', mailList)

        # message contains html
        emailMessage.content_subtype = 'html'

        # send the message
        emailMessage.send()

        # print('sent the email')

        return


