from django.db import models

from custom_user.models import User

from django.utils import timezone

import uuid

def generateTagIds():
    return str(uuid.uuid4())


class SystemUser(models.Model):
    userId = models.TextField(default=generateTagIds)

    userTag = models.IntegerField(default=0)

    attachedUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_meta')



class StudentDetails(models.Model):
    studentId = models.TextField(default=generateTagIds)

    registeredDate = models.DateTimeField(auto_now_add=True, null=True)

    studentName = models.TextField()

    studentContact = models.TextField()

    studentRegno = models.TextField()

    # course
    studentFaculty = models.TextField()

    studentProgramme = models.TextField()

    studentResidence = models.TextField()

    # accomodation
    studentAccomodation = models.TextField()

    attachedStudent = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_data')

    class Meta:
        ordering = ("-registeredDate", )



class MessageItem(models.Model):
    messageId = models.TextField(default=generateTagIds)

    sentDate = models.DateTimeField(auto_now_add=True)

    senderTag = models.TextField()

    messageContents = models.TextField()

    messageReceivers = models.TextField()

    sendingUser = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='my_messages', blank=True)


