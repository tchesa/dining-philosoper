# Dining Philosophers
A distributed implementation of the Dining Philosopher's Problem, using token-ring architecture

## instructions
To instantiate a philosopher:
```
python3 program.py $IP $PORT
```
where:
* $IP: the IP address of the next philosopher in the ring
* $PORT: the port for the connection

or:
```
python3 program.py $IP $PORT -s
```
to start a philosopher who gonna instantiate a token. Only one philosopher shoud instantiate a token.
