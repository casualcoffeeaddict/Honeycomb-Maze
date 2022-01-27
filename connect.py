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

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.0.105', username='root', password='')

stdin, stdout, sterr = ssh.exec_command('./lineFollowJunction4 1 2 2 2 2 2 2')
# lineFollowJunction4 is the program on the robot, in this case 2 2... are the inputs
