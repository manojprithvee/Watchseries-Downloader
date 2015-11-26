import sys,time
sys.stdout.write('hello')
sys.stdout.flush()
for _ in range(5):
    time.sleep(1)
    sys.stdout.write('\033[D \033[D')
    sys.stdout.flush()