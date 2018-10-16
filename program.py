import socket
import threading
import sys

# from server import Server
# from client import Client
from philosopher import Philosopher


# if (len(sys.argv) > 2):
# 	# 1: ip, 2: port
# 	client = Client(sys.argv[1], int(sys.argv[2]))
# else:
# 	# 1: port
# 	server = Server(int(sys.argv[1]))
# 	server.run()

if __name__ == '__main__':

  # local
  # this_port = int(sys.argv[1])
  # next_port = int(sys.argv[2])
  # this_ip = '127.0.0.1'
  # next_ip = '127.0.0.1'

  # remote
  this_ip = 'localhost'
  next_ip = sys.argv[1]
  this_port = int(sys.argv[2])
  next_port = int(sys.argv[2])

  start = True if '-s' in sys.argv else False
  philosopher = Philosopher(this_ip, this_port, next_ip, next_port, start)
