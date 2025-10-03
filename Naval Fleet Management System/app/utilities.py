import os
import time

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def sleep(seconds = 1):
    time.sleep(seconds)