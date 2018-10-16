import threading
import socket
from time import sleep
import random
import sys
import time
import uuid
import json

# this_port, next_port

N = 5 # numero de filosofos

class Philosopher:
  this_ip = '127.0.0.1'
  this_port = 8080
  next_ip = '127.0.0.1'
  next_port = 8080
  flag = True
  n_eats = 0
  time_eating = 120
  eating = False
  release = False
  index = -1

  def __init__(self, this_ip, this_port, next_ip, next_port, start=False):
    self.id = str(uuid.uuid1()) # based on ip and time
    print('Philosopher initialized # ' + self.id)

    self.this_ip = this_ip
    self.this_port = this_port
    self.next_ip = next_ip
    self.next_port = next_port

    self.start = time.time()

    # tSender = threading.Thread(target=sender, args=[next_port])
    # tSender.start()

    self.tReceiver = threading.Thread(target=self.receiver)
    self.tReceiver.start()

    print('press any key to connect...')
    input()
    self.sender = socket.socket()
    self.sender.connect((self.next_ip, self.next_port))

    if (start):
      # self.sender.send('token'.encode('utf-8'))
      newToken = {}
      self.index = 0
      print("index: ", self.index)
      newToken[self.id] = [self.index, 0, 0] # index, status, n_eats
      self.sender.send(self.encodeToken(newToken))
      # data = self.sender.recv(1024)
      # print('received from server: ' + str(data))
      # message = input('-> ')
    # self.sender.close()

  def receiver(self):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', self.this_port))
    s.listen(1)
    print('listening')
    c, addr = s.accept()
    print('connection from ' + str(addr))
    while self.flag:
      data = c.recv(1024)
      if not data:
        break
      # token = data.decode('utf-8')
      token = self.decodeToken(data)
      if not self.id in token.keys():
        self.index = self.highestIndex(token) + 1
        print("index: ", self.index)
        token[self.id] = [self.index, 0, self.n_eats]
      else:
        token[self.id][2] = self.n_eats # update n_eats
      # print('received: ' + str(token))
      # print('eating...')
      # self.n_eats -= 1
      # sleep(1)
      # print('eats remaining: {}, time remaining: {}'.format(self.n_eats, self.time_eating - time.time() + self.start))
      if (self.eating):
        "do nothing"
      elif (self.release):
        token = self.releaseForks(token) # release the forks
      else:
        token = self.eat(token) # try to eat
      self.push(token)
      # if (time.time() - self.start > self.time_eating or self.n_eats <= 0):
      if (time.time() - self.start > self.time_eating):
        self.flag = False
    c.close()
    self.sender.close()

  def push(self, token):
    # print('sending token...')
    # self.sender.send(str(token).encode('utf-8'))
    self.sender.send(self.encodeToken(token))

  def encodeToken(self, token):
    str_token = str(token)
    return str_token.encode('utf-8')

  def decodeToken(self, encoded):
    str_token = encoded.decode('utf-8')
    return json.loads(str_token.replace("'", "\""))

  def highestIndex(self, token):
    index = -1
    for t in token.keys():
      if token[t][0] > index:
        index = token[t][0]
    return index

  def eat(self, token):
    # print("trying to eat...")
    next_id = self.getNextId(token)
    prev_id = self.getPreviousId(token)
    
    if (next_id and token[self.id][1] == 0 and token[next_id][1] == 0): # pode comer
      if (prev_id and token[prev_id][2] < self.n_eats): # o filosofo anterior comeu menos
        print("refuse by fareness")
      else:
        print("start eating")
        token[self.id][1] = 1 # pega o garfo 1
        token[next_id][1] = 1 # pega o garfo 2
        threading.Thread(target=self.eatDelay).start()
        self.eating = True
    return token

  def releaseForks(self, token):
    next_id = self.getNextId(token)
    token[self.id][1] = 0 # devolve o garfo 1
    token[next_id][1] = 0 # devolve o garfo 2
    self.release = False
    print("releasing forks")
    return token

  def eatDelay(self):
    sleep(random.random()*3)
    self.eating = False
    self.release = True
    self.n_eats += 1
    print("stop eating. this philosopher ate ", self.n_eats, " times.")

  def getPreviousId(self, token):
    prev_id = ""
    for id in token.keys():
      if (token[id][0] == (self.index - 1) % N):
        prev_id = id
        break
    return prev_id

  def getNextId(self, token):
    next_id = ""
    for id in token.keys():
      if (token[id][0] == (self.index + 1) % N):
        next_id = id
        break
    return next_id

