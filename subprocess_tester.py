import subprocess

proc = subprocess.Popen('firefly -i INPUTS/test.inp', 
                        shell = True,
                        stdout = subprocess.PIPE)

while proc.poll() is None:
    output = proc.stdout.readline()
    
    if 'TOTAL ENERGY' in output:
        print output
