
import subprocess
from pathlib import Path

converter = "C:\Program Files\headlessGMLogToCSV\headlessGMLogToCSV.exe"  
flags = ["-HourlyLog",  "-DailyLog", "-MonthlyLog"]
log_location = Path("C:\\Users\\u7j9\\Documents\\logs\\testing")
print(log_location)
results = ''
for flag in flags:
    results = subprocess.run([converter, flag, str(log_location)], shell=False, capture_output=True)
    print(flag[1:], 'completed')
print(results)