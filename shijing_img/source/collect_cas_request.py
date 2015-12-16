__author__ = 'wenjusun'

import paramiko
import sys
from datetime import datetime
import time


hosts=['amp02-p-e-mmi','amp03-p-e-mmi','amp04-p-e-mmi','amp05-p-e-mmi','amp06-p-e-mmi']
# hosts=['amp02-p-e-mmi']
username='wenjusun'
password='Motosunwj'

def yesterday_in_string():
    now_timestamp = int(round(time.time()))
    yesterday_now = now_timestamp - 24 * 60 * 60

    return datetime.fromtimestamp(yesterday_now).strftime("%Y_%m_%d")

yesterday = yesterday_in_string()

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

def result_from_exec_ssh_cmd(ssh,cmd_str):
    stdin,stdout,stderr=ssh.exec_command(cmd_str , get_pty=True)

    if not stdin.channel.closed :
        # print('the target host is requesting input,try sending passwd:')
        stdin.write(password+'\n')
        stdin.flush()

    # print_tty_output("stdout:",stdout.read().splitlines())
    count_result = get_tty_output(stdout.read().splitlines())
    # print_tty_output("stderr:",stderr.read().splitlines())

    ssh.close()

    return count_result


"grep /ssoauth/login?TARGET= /home/jetty/current/logs/2015_11_01.request.log | grep POST |grep www.motorola.com.cn |wc -l"

def count_validate_requests(dt,site):
    cmd = "grep ssoauth/samlValidate?TARGET= /home/jetty/current/logs/%s.request.log |grep POST |grep %s |wc -l"  %(dt,site)
    counter=0
    print cmd
    for host in hosts:
        print host+"-->>",
        counter += result_from_exec_ssh_cmd(get_ssh_client(host,22),cmd)

    return counter

def count_reset_password_requests():
    pass

def count_verify_user_requests(dt,site):
    cmd = "grep /ssoauth/web/steps_to_verify.html /home/jetty/current/logs/%s.request.log |grep svc=verify_user |grep %s |wc -l"  %(dt,site)
    print cmd
    counter = 0
    for host in hosts:
        print host+"-->>",
        counter += result_from_exec_ssh_cmd(get_ssh_client(host,22),cmd)
    return counter

def count_signup_requests(dt,site):
    cmd = "grep /ssoauth/app/user/signup?type= /home/jetty/current/logs/%s.request.log | grep POST |wc -l"  %(dt)
    print cmd
    counter = 0
    for host in hosts:
        print host+"-->>",
        counter += result_from_exec_ssh_cmd(get_ssh_client(host,22),cmd)

    return counter


def count_login_requests(dt,site):
    cmd = "grep /ssoauth/login?TARGET= /home/jetty/current/logs/%s.request.log | grep POST |grep %s |wc -l"  %(dt,site)
    print cmd
    counter = 0
    for host in hosts:
        print host+"-->>",
        counter += result_from_exec_ssh_cmd(get_ssh_client(host,22),cmd)

    return counter

def count_all_requests(site):
    # for i in range(9,10):
    dt = yesterday

    login_requests = count_login_requests(dt,site)
    signup_requests = count_signup_requests(dt,site)
    verify_user_requests = count_verify_user_requests(dt,site)

    print "login:%d" % login_requests
    print "signup:%d" % signup_requests
    print "verify:%d" % verify_user_requests
    # count_validate_requests(dt,site)

    statistics_result_to_file(login_requests,signup_requests,verify_user_requests)
    # print ""
    print ""
    print ""

def statistics_result_to_file(login_requests,signup_requests,verify_user_requests):
    file_name = "cas_result_"+yesterday

    with open(file_name,"w") as f:
        # f.write("login,signup,verify")
        # f.write("\n")
        f.write("%d,%d,%d" %(login_requests,signup_requests,verify_user_requests))

    f.close()

def bactch_to_file_nov(site):
    month_nov='2015_11'
    with open(month_nov,'w') as f:
        for i in range(14,31):
            day = str(i)
            dt=month_nov+'_'+day
            login_requests = count_login_requests(dt,site)
            signup_requests = count_signup_requests(dt,site)
            verify_user_requests = count_verify_user_requests(dt,site)

            daystr = '2015-11-'+day
            record = "%s,%d,%d,%d\n" %(daystr,login_requests,signup_requests,verify_user_requests)
            f.write(record)

def bactch_to_file(site):
    month_dec='2015_12'
    with open(month_dec,'w') as f:
        for i in range(1,9):
            day = str(i)
            dt=month_dec+'_0'+day
            login_requests = count_login_requests(dt,site)
            signup_requests = count_signup_requests(dt,site)
            verify_user_requests = count_verify_user_requests(dt,site)

            daystr = '2015-12-0'+day
            record = "%s,%d,%d,%d\n" %(daystr,login_requests,signup_requests,verify_user_requests)
            f.write(record)



if __name__ == '__main__':
    print sys.argv
    print "statistics---:"+yesterday
    # ssh_cmd(sys.argv[1])
    site=sys.argv[1]
    # count_all_requests(site)
    bactch_to_file(site)