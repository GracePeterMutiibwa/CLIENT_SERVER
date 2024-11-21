from django.urls import path

from django.conf.urls.static import static

from django.conf import settings


from . import views

app_name = 'reg'


urlpatterns = [
    path("", view=views.websiteHome, name='home'),

    path("login/", view=views.validateLogin, name='login'),

    path("manager/", view=views.adminHome, name='manager'),

    path("profile/", view=views.loadStudentProfile, name='student'),

    path("register/", view=views.studentRegister, name='register'),

    path("add-student/", view=views.registerNewStudent, name='add-student'),

    path("initiate-edit/<str:attachedId>/", view=views.triggerDetailsEdit, name='start-edit'),

    path("wipe-message/<str:messageId>/", view=views.deleteMessage, name='wipe-message'),

    path("send-message/", view=views.submitMessageItem, name='send-message'),
    
    path("route/", view=views.routeManager, name='route'),

    path("logout/", view=views.logoutUser, name='logout'),

    path("wipe-student/<str:studentTag>/", view=views.deleteStudent, name='wipe-student'),
]




# avoid redirects
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# load static files even in debug -> False
if (settings.FORCE_STATIC_FILE_SERVING is True and settings.DEBUG is False):
    # first revert debug
    settings.DEBUG = True

    # load these urls
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # change to debug
    settings.DEBUG = False

else:
    # the loaded urls are enough
    pass