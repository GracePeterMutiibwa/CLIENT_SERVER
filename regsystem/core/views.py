from django.shortcuts import render, redirect

from django.views.decorators.cache import cache_control

from django.contrib.auth.decorators import login_required, user_passes_test

from custom_user.models import User

from django.contrib.auth import login, logout

from django.contrib import messages

from django.http import HttpRequest

from .systemUtils import RegistrationTools

def isAdmin(userInstance:User):
    return userInstance.is_superuser

def isStudent(userInstance:User):
    return isAdmin(userInstance) is False

def notAuthenticated(userInstance:User):
    return userInstance.is_authenticated is False



@cache_control(no_cache=True, no_store=True, must_revalidate=True)
@user_passes_test(notAuthenticated, login_url='reg:route')
def websiteHome(request):
    return render(request, 'public/login-page.html')

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
@login_required(login_url='reg:home')
def routeManager(request):
    if request.user.is_superuser:
        returnRoute = 'reg:manager'

    else:
        returnRoute = 'reg:student'

    return redirect(returnRoute)


@login_required(login_url='reg:home')
def logoutUser(request:HttpRequest):
    logout(request=request)

    return redirect('reg:home')

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def validateLogin(request):
    # {'email': '2020bse008@std.must.ac.ug', 'password': 'PNzia0Ha'}
    loginData = request.POST.dict()

    userExists, userInfo = RegistrationTools().doesUserExist(loginData['email'])

    if (userExists is True):
        if userInfo.check_password(loginData['password']):
            # login
            login(request, userInfo)

            return redirect('reg:route')

        else:
            messages.warning(request, "Either the email or password is invalid")

    else:
        messages.error(request, "No account was found for the provided details")

    return redirect('reg:home')


@cache_control(no_cache=True, no_store=True, must_revalidate=True)
@user_passes_test(isAdmin, login_url='reg:route')
@login_required(login_url='reg:home')
def adminHome(request):
    studentList = RegistrationTools().loadPresentStudents()

    # context
    dataContext = {}

    if len(studentList) > 0:
        # load the students
        dataContext['info'] = studentList

    else:
        pass

    # load messages
    RegistrationTools().loadAvailableMessages(userTag='admin', whereToLoad=dataContext)

    # print(dataContext)

    return render(request, 'restricted/admin-panel.html', context=dataContext)


@cache_control(no_cache=True, no_store=True, must_revalidate=True)
@user_passes_test(isAdmin, login_url='reg:route')
@login_required(login_url='reg:home')
def studentRegister(request):
    if 'feed' in request.session:
        studentData, studentTag = request.session['feed']

        feedContext = {
            'text': 'Save Changes',
            'color': 'info',
            'data': studentData,
            'save': studentTag
        
        }

        # wipe
        request.session.pop('feed')

        request.session.modified = True

    else:
        feedContext = {
            'text': 'Register',
            'color': 'primary',
            'data': RegistrationTools().studentMetaCollector(studentTag=None),
            'save': 'new'
        }

    
    # print(feedContext)

    return render(request, 'restricted/student-register.html', context=feedContext)


@cache_control(no_cache=True, no_store=True, must_revalidate=True)
@user_passes_test(isStudent, login_url='reg:route')
@login_required(login_url='reg:home')
def loadStudentProfile(request):
    # data for the student
    studentContext = {}

    # load the student name and their messages
    foundDetails = RegistrationTools().loadStudentSpecificDetails(studentUserObject=request.user)

    studentContext['info'] = foundDetails

    # load details
    RegistrationTools().loadTagAndReceiver(userInstance=request.user, whereToLoad=studentContext)

    # print(studentContext)

    # load news group messages
    RegistrationTools().loadStudentNewsGroup(studentUserInstance=request.user, whereToLoad=studentContext)

    RegistrationTools().loadMyConcernedMessages(studentUserInstance=request.user, whereToLoad=studentContext)
    # print(studentContext)

    return render(request, 'restricted/student-account.html', context=studentContext)




@user_passes_test(isAdmin, login_url='reg:route')
@login_required(login_url='reg:home')
def registerNewStudent(request):
    # {'name': 'Elvis Gift', 'email': 'elvisgift@gmail.com', 
    # 'contact': '7352663733', 'regno': '2020/bse/008/ps', 
    # 'faculty': 'FCI', 'campus-area': 'TOWN CAMPUS', 
    # 'accomodation': 'GENTS FLAT TOWN CAMPUS'
    # 'tag': 'new' }
    studentData = request.POST.dict()

    # print(studentData, request.method)

    nextRoute = 'reg:register'

    # status
    isValid = False

    if studentData['tag'] == 'new':
        # check if the user exists
        existStatus, _ = RegistrationTools().doesUserExist(studentData['email'])

        if existStatus is True:
            messages.warning(request, "A User with that email exists already")

        elif RegistrationTools().registeredAlready(studentData['regno'].lower()):
            messages.warning(request, "A student with that Registration Number exists already")

        else:
            # save the student
            isValid = True

            studentId = None

    else:
        # get status
        existStatus, _ = RegistrationTools().doesUserExist(studentData['email'])

        if existStatus is True:
            isValid = _.is_superuser is False

        else:
            # prepare
            isValid = True

        studentId = studentData['tag']


    if isValid is True:
        RegistrationTools().saveStudentDetails(studentInfo=studentData, studentId=studentId)

        if studentId is None:
            messages.success(request, "A new student named {} was registered successfully".format(studentData['name'].title()))

        else:
            messages.info(request, "Details for the student named {} were updated successfully".format(studentData['name'].title()))

    else:
        messages.info(request, "It appears like you used an email that is not for a student...")

    # route to visit next
    nextRoute = 'reg:manager'

    return redirect(nextRoute)


@cache_control(no_cache=True, no_store=True, must_revalidate=True)
@user_passes_test(isAdmin, login_url='reg:route')
@login_required(login_url='reg:home')
def triggerDetailsEdit(request, attachedId:str):
    # studentMetaCollector
    foundData = RegistrationTools().studentMetaCollector(studentTag=attachedId)    

    # print(foundData)
    request.session['feed'] = [foundData, attachedId]

    request.session.modified = True

    return redirect('reg:register')



@cache_control(no_cache=True, no_store=True, must_revalidate=True)
@login_required(login_url='reg:home')
def submitMessageItem(request):
    # message data
    messageData = request.POST.dict()

    # print(messageData)

    # determine if the user is an admin
    isAdmin = request.user.is_superuser

    if isAdmin:
        userTag = 'admin'
    
    else:
        userTag = messageData['tag']

    # details
    messageContents = messageData['message']

    messageReceivers = messageData['receiver']

    # save
    RegistrationTools().recordNewMessage(userTag=userTag, messageData=messageContents, messageReceivers=messageReceivers)

    if isAdmin:
        messages.success(request, "Your message was forwaded successfully")

    else:
        messages.success(request, "you just sent a new message to the discuession..")

    return redirect(request.META['HTTP_REFERER'])



@cache_control(no_cache=True, no_store=True, must_revalidate=True)
@user_passes_test(isAdmin, login_url='reg:route')
@login_required(login_url='reg:home')
def deleteMessage(request, messageId:str):
    # check if the user owns the message
    userOwnsMessage = RegistrationTools().userOwnsMessage(messageTag=messageId, deleteRequest=request)

    if userOwnsMessage:
        # delete
        RegistrationTools().deleteMessageViaTag(messageTag=messageId)

        messages.info(request, "Your message was deleted successfully!")

    else:
        messages.error(request, "Ooops, It appears like you followed a badlink..!")

    return redirect('reg:route')


@cache_control(no_cache=True, no_store=True, must_revalidate=True)
@user_passes_test(isAdmin, login_url='reg:route')
@login_required(login_url='reg:home')
def deleteStudent(request, studentTag:str):
    # check if the student exists
    studentPresent, _ = RegistrationTools().studentExists(studentTag=studentTag)

    if studentPresent is True:
        # get the name
        studentName = _.studentName

        # delete the student user object
        _.attachedStudent.delete()

        messages.info(request, f"A student named {studentName} was deleted successfully!")

    else:
        messages.error(request, "Ooops, It appears like you followed a badlink..!")


    return redirect('reg:route')
