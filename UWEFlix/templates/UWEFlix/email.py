from django.core.mail import send_mail
from django.http import HttpResponse

#
def sendEmail(request, emailto, message):
    #
    res = send_mail("hello paul", message, "admin@UWEFLix.com", [emailto])
    #
    return HttpResponse('%s'%res) 