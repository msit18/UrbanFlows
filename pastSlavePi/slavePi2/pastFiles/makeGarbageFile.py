import time

f = open('garbageFile.txt', 'rw')
f.write("I ran the file and it does a thing huzzah")
time.sleep(5)
f.close()
