from custom_user.models import User

from .models import StudentDetails, MessageItem

from datetime import datetime

from django.utils import timezone

from django.http import HttpRequest

from django.db.models import Q

from .mailingTools import MailPreProcessor

class RegistrationTools:
    def doesUserExist(self, userEmail:str):
        # number of matches
        userCount = User.objects.filter(email=userEmail).count()

        return userCount > 0, User.objects.filter(email=userEmail).first()

    
    def registeredAlready(self, regNumber:str):
        # student has that reg no already
        studentCount = StudentDetails.objects.filter(studentRegno=regNumber.lower()).count()

        return studentCount > 0

    
    def createNewSystemUser(self, userEmail:str, userPassword:str):
        # save user password
        newSystemUser = User.objects.create(
            email=userEmail
        )

        # set their password
        newSystemUser.set_password(raw_password=userPassword)

        newSystemUser.save()

        return newSystemUser

    
    def saveStudentDetails(self, studentInfo:dict, studentId:str):
        # {'name': 'Elvis Gift', 'email': 'elvisgift@gmail.com', 
        # 'contact': '7352663733', 'regno': '2020/bse/008/ps', 
        # 'faculty': 'FCI', 'programme': 'BACHELOR OF SOFTWARE ENGINEERING', 'campus-area': 'TOWN CAMPUS', 
        # 'accomodation': 'GENTS FLAT TOWN CAMPUS'}

        # email
        studentEmail = studentInfo['email']

        # student regno : Initially its their account password
        studentRegNo = studentInfo['regno'].strip().lower()

        studentName = studentInfo['name'].title()

        studentContact = studentInfo['contact']

        studentFaculty = studentInfo['faculty']

        studentProgramme = studentInfo['programme']

        studentResidence = studentInfo['campus-area']

        studentAccomodation = studentInfo['accomodation']

        if studentId is None:
            # create a new user
            objectOfStudentUser = self.createNewSystemUser(
                userEmail=studentEmail,
                userPassword=studentRegNo
            )

            # write details
            studentInstance = StudentDetails.objects.create(
                studentName=studentName,
                studentContact=studentContact,
                studentRegno=studentRegNo,
                studentFaculty=studentFaculty,
                studentProgramme=studentProgramme,
                studentResidence=studentResidence,
                studentAccomodation=studentAccomodation,
                attachedStudent=objectOfStudentUser
            )


        else:
            # get the student
            studentInstance:StudentDetails = StudentDetails.objects.filter(studentId=studentId).first()

            # update the data
            studentInstance.studentName = studentName
            studentInstance.studentContact = studentContact
            studentInstance.studentRegno = studentRegNo
            studentInstance.studentFaculty = studentFaculty
            studentInstance.studentProgramme = studentProgramme
            studentInstance.studentResidence = studentResidence
            studentInstance.studentAccomodation = studentAccomodation

            # update user object
            objectOfStudentUser = studentInstance.attachedStudent

            objectOfStudentUser.email = studentEmail

            objectOfStudentUser.set_password(studentRegNo)

            objectOfStudentUser.save()


            # update the actual object
            studentInstance.attachedStudent = objectOfStudentUser

        
        # save
        studentInstance.save()

        return


    def studentDetailsFormatter(self, studentDataObject:StudentDetails) -> str:
        studentMetaString = f"""{studentDataObject.studentName}\n--\n{studentDataObject.studentProgramme}\n--\nREGNO: {studentDataObject.studentRegno}\n--\n{studentDataObject.studentFaculty}\n--\n{studentDataObject.attachedStudent.email}\n--\n+256{studentDataObject.studentContact}\n--\n{studentDataObject.studentResidence}\n--\n{studentDataObject.studentAccomodation}"""

        return studentMetaString.strip()

    
    def studentMetaCollector(self, studentTag:str) -> dict:
        if not studentTag is None:
            # get
            studentInstance:StudentDetails = StudentDetails.objects.filter(studentId=studentTag).first()

            formattedFillableInfo = {
                'name': studentInstance.studentName,
                'email': studentInstance.attachedStudent.email,
                'contact': studentInstance.studentContact,
                'regno': studentInstance.studentRegno,
                'faculty': studentInstance.studentFaculty,
                'program': studentInstance.studentProgramme,
                'campus': studentInstance.studentResidence,
                'category': 'RENTAL' if studentInstance.studentAccomodation == 'PRIVATE RESIDENCE' else 'HALLS',
                'accomodation': studentInstance.studentAccomodation
            }

        
        else:
            formattedFillableInfo = {
                'name': "",
                'email': "",
                'contact': "",
                'regno': "",
                'faculty': "COMPUTING & INFORMATICS",
                'program': "BACHELOR OF SOFTWARE ENGINEERING",
                'campus': "TOWN CAMPUS",
                'category': 'HALLS',
                'accomodation': "GENTS FLAT TOWN CAMPUS"
            }

        return formattedFillableInfo


    def loadPresentStudents(self):
        # get all
        presentStudents = StudentDetails.objects.all()

        formattedStudentData = [{
            'name': eachStudent.studentName,
            'regno': eachStudent.studentRegno,
            'id': eachStudent.studentId,
            'details': self.studentDetailsFormatter(studentDataObject=eachStudent)

        } for eachStudent in presentStudents]


        return formattedStudentData

    
    def loadStudentSpecificDetails(self, studentUserObject:User):
        # print(studentUserObject)
        attachedIfo = studentUserObject.student_data

        return {
            'name': attachedIfo.studentName
        }


    def getReceiverEmailsBasedOnTag(self, groupName:str):
        # get the names
        if groupName == 'ALL':
            foundStudents = StudentDetails.objects.all()

        else:
             foundStudents = StudentDetails.objects.filter(studentFaculty=groupName).all()

        
        # get their emails
        attachedEmails = [eachStudent.attachedStudent.email for eachStudent in foundStudents]

        # get the perfect tag
        groupNameMap = {
            'ALL': 'MUSTERIANS',
            'COMPUTING & INFORMATICS': 'FCI STUDENTS',
            'BUSINESS STUDIES': 'BUSINESS STUDENTS',
            'APPLIED SCIENCES': 'APPLIDE SCIENCES STUDENTS',
            'MEDICINE & SURGERY': 'MEDICINE STUDENTS'
        }

        nameOfGroup = groupNameMap[groupName]

        # senf the message to all
        return attachedEmails, nameOfGroup




    def informNecessaryRecipients(self, messageToSend:str, attachedGroup:str):
        # get the receivers
        emailReceivers, receiverName = self.getReceiverEmailsBasedOnTag(groupName=attachedGroup)
    
        # send
        MailPreProcessor().pushMailMessage(
            mailInfo=[receiverName, messageToSend],
            recipients=emailReceivers,
            mailType=1
        )

        # print('sent message')

        return

    def recordNewMessage(self, userTag:str, messageData:str, messageReceivers:str):
        # write
        newMessage = MessageItem.objects.create(
            senderTag=userTag,
            messageContents=messageData,
            messageReceivers=messageReceivers
        )

        newMessage.save()

        if userTag == 'admin':
            # alert the other users
            self.informNecessaryRecipients(
                messageToSend=messageData,
                attachedGroup=messageReceivers
            )

        return

    
    def getNameAndCourseOfSender(self, tagOfSender:str):
        # get the sender
        messageSender:StudentDetails = StudentDetails.objects.filter(studentId=tagOfSender).first()

        return messageSender.studentName, messageSender.studentProgramme


    def formatTimeStamp(self, timeStamp:datetime):
        # to time zone time
        convertedTime = timeStamp.astimezone(timezone.get_current_timezone())
    
        return convertedTime.strftime("%d, %b, %Y At %I:%M %p")



    def formatMessageItem(self, messageInstance:MessageItem, mainReference:str=None):
        formattedMessage = {
            'stamp': self.formatTimeStamp(timeStamp=messageInstance.sentDate),
            'message': messageInstance.messageContents

        }

        # tag of sender
        senderTag = messageInstance.senderTag

        if  senderTag == 'admin':
            formattedMessage['id'] = messageInstance.messageId

            formattedMessage['receivers'] = messageInstance.messageReceivers

        else:
            # get the name and course
            studentName, studentCourse = self.getNameAndCourseOfSender(tagOfSender=senderTag)

            formattedMessage['name'] = studentName

            formattedMessage['course'] = studentCourse

            senderOwnsMessage = senderTag == mainReference

            formattedMessage['align'] = 'end' if senderOwnsMessage is True else 'start'

            formattedMessage['color'] = 'primary' if senderOwnsMessage else 'warning'



        return formattedMessage

    
    def loadAvailableMessages(self, userTag:str, whereToLoad:dict):
        # get
        if userTag == 'admin':
            foundMessages = MessageItem.objects.filter(senderTag='admin').all()

            formattedMessages = [self.formatMessageItem(messageInstance=eachMessage, mainReference=None) for eachMessage in foundMessages]

        else:
            pass

        # load
        if len(formattedMessages) > 0:
            whereToLoad['my_messages'] = formattedMessages

        else:
            pass

        return

    
    def getMessageByTag(self, messageTag:str):
        return MessageItem.objects.filter(messageId=messageTag).first()

    def userOwnsMessage(self, messageTag:str, deleteRequest:HttpRequest):
        # get the tag
        attachedUser = deleteRequest.user

        # get the sender
        messageSender = self.getMessageByTag(messageTag=messageTag).senderTag

        # validate ownership
        if attachedUser.is_superuser:
            isOwner = messageSender == 'admin'

        else:
            isOwner = attachedUser.student_data.studentId == messageSender

        
        return isOwner

    
    def deleteMessageViaTag(self, messageTag:str):
        # get the message
        messageToDelete = self.getMessageByTag(messageTag=messageTag)

        messageToDelete.delete()

        return

    
    def loadStudentNewsGroup(self, studentUserInstance:User, whereToLoad:dict):
        # get their faculty
        studentFaculty = studentUserInstance.student_data.studentFaculty

        # query
        getQuery = (Q(messageReceivers=studentFaculty) | Q(messageReceivers='ALL')) & Q(senderTag='admin')

        matchingMessages = MessageItem.objects.filter(getQuery).order_by('sentDate')

        # format the messages
        formattedMessages = [{
            'message': eachMessage.messageContents,
            'date': self.formatTimeStamp(timeStamp=eachMessage.sentDate)
        } for eachMessage in matchingMessages]

        if len(formattedMessages) > 0:
            # load messages from the admin
            whereToLoad['news_group'] = formattedMessages

        else:
            pass

        return

    
    def fetchTagAndFaculty(self, userInstance:User):
        studentId = userInstance.student_data.studentId

        studentFaculty = userInstance.student_data.studentFaculty

        return studentId, studentFaculty
    
    def loadMyConcernedMessages(self, studentUserInstance:User, whereToLoad:dict):
        # get their tag and faculty
        studentId, studentFaculty = self.fetchTagAndFaculty(userInstance=studentUserInstance)

        # only group messages 
        getQuery = Q(messageReceivers=studentFaculty) & ~Q(senderTag='admin')

        # extract matching messages
        matchingMessages = MessageItem.objects.filter(getQuery).order_by('sentDate')

        formattedMessages = [self.formatMessageItem(messageInstance=eachMessage, mainReference=studentId) for eachMessage in matchingMessages]

        # load faculty chats
        if len(formattedMessages) > 0:
            whereToLoad['our_group'] = formattedMessages

        else:
            pass

        return

    def loadTagAndReceiver(self, userInstance:User, whereToLoad:dict):
        # load tag and receiver
        studentId, studentFaculty = self.fetchTagAndFaculty(userInstance=userInstance)

        # get the id tag and receivers
        whereToLoad['id_tag'] = studentId

        whereToLoad['receivers'] = studentFaculty

        return

    def studentExists(self, studentTag:str):
        studentInstance:StudentDetails = StudentDetails.objects.filter(studentId=studentTag).first()

        return not studentInstance is None, studentInstance