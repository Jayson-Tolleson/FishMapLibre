import subprocess
from subprocess import Popen, PIPE, STDOUT, run

start = ('sudo nohup python3 /var/www/webserver.py & sudo nohup python3 /var/www/cgi-bin/upload.py & sudo nohup python3 /var/www/fishmaplibre.py &')
subprocess.run(start, shell=True, stderr=subprocess.STDOUT)



