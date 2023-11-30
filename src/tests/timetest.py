from time import process_time
from re import search

while True:
    print(str(process_time()))
    print(search(r"(.*)\.", str(process_time())).group(0))