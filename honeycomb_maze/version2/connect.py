import paramiko

username = 'root'
password = ''
ip_address = '192.168.0.101'

cmd = './honeycomb_fast 1 1 1 1 1 1 1 1 1 1 1 1 '

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip_address, port=22, username=username, password=password,
        pkey=None, key_filename=None, timeout=None, allow_agent=True,
        look_for_keys=True, compress=False)



# ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)




# robot1 = paramiko.SSHClient()
# robot1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# robot1.connect('192.168.0.103', username='root', password='')

# robot2 = paramiko.SSHClient()
# robot2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# robot2.connect('192.168.0.104', username='root', password='')
#
# robot3 = paramiko.SSHClient()
# robot3.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# robot3.connect('192.168.0.105', username='root', password='')

# send commands to robots
# stdin, stdout, sterr = robot1.exec_command('./lineFollowJunction4 1 2 2 2 2 2 2')

# stdin, stdout, sterr = robot2.exec_command('./lineFollowJunction4 1 2 2 2 2 2 2')
#
# stdin, stdout, sterr = robot3.exec_command('./lineFollowJunction4 1 2 2 2 2 2 2')
# lineFollowJunction4 is the program on the robot, in this case 2 2... are the inputs
