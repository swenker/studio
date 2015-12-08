__author__ = 'wenjusun'

import paramiko
import sys
from datetime import datetime
import time


hosts=['amp02-p-e-mmi','amp03-p-e-mmi','amp04-p-e-mmi','amp05-p-e-mmi','amp06-p-e-mmi']
# hosts=['amp02-p-e-mmi']
username='wenjusun'
password='Motosunwj'

def today_in_string():
    now_timestamp = int(round(time.time()))
    yesterday_now = now_timestamp - 24 * 60 * 60

    return datetime.fromtimestamp(yesterday_now).strftime("%Y_%m_%d")

today = today_in_string()

def get_ssh_client(host,PORT):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host,PORT,username,password)

    return ssh

def get_tty_output(lines):
    counter=0
    if lines:
        for line in lines:
            if not line.startswith(password):
                print line

                if(line.strip()):
                    counter = int(line.strip())
                    break

    return counter

def print_tty_output(output_type,lines):

    if lines:
        print "Result__%s: " % output_type,
        for line in lines:
            if not line.startswith(password):
                print line+"    ,",

        print "<"*20

def exec_ssh_cmd(ssh,cmd_str):
    stdin,stdout,stderr=ssh.exec_command(cmd_str , get_pty=True)

    if not stdin.channel.closed :
        # print('the target host is requesting input,try sending passwd:')
        stdin.write(password+'\n')
        stdin.flush()

    print_tty_output("stdout:",stdout.read().splitlines())
    # count_result = get_tty_output(stdout.read().splitlines())
    print_tty_output("stderr:",stderr.read().splitlines())

    ssh.close()

    #return count_result

def count_request(keyword,file,host):
    cmd_str="grep %s %s |wc -l" %(keyword,file)
    return exec_ssh_cmd(get_ssh_client(host,22),cmd_str)


def count_all_hosts(keyword,file):
    total=0
    for host in hosts:
        print host+"-->>"
        total +=count_request(keyword,file,host)
    print "total requests:"+str(total)

def count_cas_saml(keywords='samlValidate',file='2015_11_01.request.log'):
    count_all_hosts(keywords,'/home/jetty/current/logs/'+file)

def check_cas_requests():
    keywords=None
    file=None
    if sys.argv and len(sys.argv)>0:
        keywords=sys.argv[1]
    if sys.argv and len(sys.argv)>1:
        file = sys.argv[2]
    count_cas_saml(keywords,file)

def ssh_cmd(cmd):
    for host in hosts:
        print host+"-->>"
        exec_ssh_cmd(get_ssh_client(host,22),cmd)


"grep /ssoauth/login?TARGET= /home/jetty/current/logs/2015_11_01.request.log | grep POST |grep www.motorola.com.cn |wc -l"

def count_validate_requests(dt,site):
    cmd = "grep ssoauth/samlValidate?TARGET= /home/jetty/current/logs/%s.request.log |grep POST |grep %s |wc -l"  %(dt,site)
    print cmd
    for host in hosts:
        print host+"-->>",
        exec_ssh_cmd(get_ssh_client(host,22),cmd)

def count_reset_password_requests():
    pass

def count_verify_user_requests(dt,site):
    cmd = "grep /ssoauth/web/steps_to_verify.html /home/jetty/current/logs/%s.request.log |grep svc=verify_user |grep %s |wc -l"  %(dt,site)
    print cmd
    for host in hosts:
        print host+"-->>",
        exec_ssh_cmd(get_ssh_client(host,22),cmd)

def count_signup_requests(dt,site):
    cmd = "grep /ssoauth/app/user/signup?type= /home/jetty/current/logs/%s.request.log | grep POST |wc -l"  %(dt)
    print cmd
    for host in hosts:
        print host+"-->>",
        exec_ssh_cmd(get_ssh_client(host,22),cmd)

def count_login_requests(dt,site):
    cmd = "grep /ssoauth/login?TARGET= /home/jetty/current/logs/%s.request.log | grep POST |grep %s |wc -l"  %(dt,site)
    print cmd
    for host in hosts:
        print host+"-->>",
        exec_ssh_cmd(get_ssh_client(host,22),cmd)


def count_all_requests(site):
    # for i in range(9,10):
    dt = today
    count_login_requests(dt,site)
    count_signup_requests(dt,site)
    count_verify_user_requests(dt,site)
    # count_validate_requests(dt,site)

    print ""
    print ""
    print ""

def statistics_result_to_file():
    pass

if __name__ == '__main__':
    print sys.argv
    print "statistics---:"+today
    ssh_cmd(sys.argv[1])
    # site=sys.argv[1]
    # count_all_requests(site)
