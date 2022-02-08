import paramiko
from paramiko import SSHClient

SSHClient.connect('192.168.0.105',
                  port=22,
                  username=None,
                  password=None,
                  pkey=None,
                  key_filename=None,
                  timeout=None,
                  allow_agent=True,
                  look_for_keys=True,
                  compress=False,
                  sock=None,
                  gss_auth=False,
                  gss_kex=False,
                  gss_deleg_creds=True,
                  gss_host=None,
                  banner_timeout=None,
                  auth_timeout=None,
                  gss_trust_dns=True,
                  passphrase=None,
                  disabled_algorithms=None)



robot1 = paramiko.SSHClient()
robot1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
robot1.connect('192.168.0.103', username='root', password='')

robot2 = paramiko.SSHClient()
robot2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
robot2.connect('192.168.0.104', username='root', password='')

robot3 = paramiko.SSHClient()
robot3.set_missing_host_key_policy(paramiko.AutoAddPolicy())
robot3.connect('192.168.0.105', username='root', password='')

# send commands to robots
stdin, stdout, sterr = robot1.exec_command('./lineFollowJunction4 1 2 2 2 2 2 2')

stdin, stdout, sterr = robot2.exec_command('./lineFollowJunction4 1 2 2 2 2 2 2')

stdin, stdout, sterr = robot3.exec_command('./lineFollowJunction4 1 2 2 2 2 2 2')
# lineFollowJunction4 is the program on the robot, in this case 2 2... are the inputs
