__author__ = 'wenjusun'


import smtplib

sender='admin@yinyushijing.cn'
receiver="msgates@126.com"



def sendmail(user,email_type=1):

    try:
        message="""From: From Person <%s>
        To: To Person <%s>
        Subject: SMTP e-mail test

        %s
        """

        smtpObject = smtplib.SMTP('localhost')

        msg = message %(sender,user,"This is a test body")
        smtpObject.sendmail(sender,receiver,msg)
        print "Successfully sent to "+user
    except smtplib.SMTPException ,e:
        print "Failed:"+e.message


if __name__ == '__main__':
    sendmail(receiver)


