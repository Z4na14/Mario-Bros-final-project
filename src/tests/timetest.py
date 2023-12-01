import time
from re import search

while True:
    print(str(time.process_time()), time.time())
    print(search(r"(.*)\.", str(time.process_time())).group(0))