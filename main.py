import FetchHive
import time

t = 60*5

def ConsoleHive():
  while True:
      FetchHive.main()
      time.sleep(t)


ConsoleHive()