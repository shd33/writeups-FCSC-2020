import socket
import numpy as np
from zlib import compress, decompress
from base64 import b64encode as b64e, b64decode as b64d


q     = 2 ** 11
n     = 280
n_bar = 4
m_bar = 4

zeros_comb = [[0, 0, 2, 2], [0, 2, 0, 2], [0, 2, 2, 0], [2, 0, 0, 2], [2, 0, 2, 0], [2, 2, 0, 0]]

def ones_comb(key_zeros):
	key_line1 = []
	key_line2 = []
	sig = 1
	for i in key_zeros:
		if i == 0:
			key_line1.append(0)
			key_line2.append(0)
		else:
			key_line1.append(sig)
			key_line2.append(1 - sig)
			sig = 0
	return key_line1, key_line2

def test_key(sock, U, C, key):
	sock.sendall(b"1\n")
	recv_until(sock, b"U = ", 30)
	sock.sendall(b64e(compress(U.tobytes())) + b"\n")
	recv_until(sock, b"C = ", 30)
	sock.sendall(b64e(compress(C.tobytes())) + b"\n")
	recv_until(sock, b"key_b = ", 30)
	sock.sendall(b64e(compress(key.tobytes())) + b"\n")

	rep = recv_until(sock, b">>>", 100)
	if rep.find(b"Success") != -1:
		return True
	else:
		return False

def test_flag(sock, S_a, E_a):
	sock.sendall(b"2\n")
	recv_until(sock, b"S_a = ", 30)
	sock.sendall(b64e(compress(S_a.tobytes())) + b"\n")
	recv_until(sock, b"E_a = ", 30)
	sock.sendall(b64e(compress(E_a.tobytes())) + b"\n")
	rep = recv_until(sock, b"\n", 300)
	print(rep.decode("utf-8"))

def assemble_key(key_zeros, key_ones):
	key_line = []
	for i in range(n_bar):
		if key_zeros[i] == 0:
			key_line.append(0)
		elif key_ones[i] == 1:
			key_line.append(-1)
		else:
			key_line.append(1)
	return key_line

def find_Sa_line(sock, line):
	U = np.zeros((m_bar, n), dtype = np.int64)
	U[0][line] = q // 2
	C = np.zeros((m_bar, n_bar), dtype = np.int64)
	key = np.zeros((m_bar, n_bar), dtype = np.int64)

	key_zeros = []
	for key_line in zeros_comb:
		key[0] = key_line
		if test_key(sock, U, C, key):
			key_zeros = key_line
			break

	key_ones = []
	U[0][line] = q // 10
	C[0] = [q // 10 for i in range(n_bar)]
	for key_line in ones_comb(key_zeros):
		key[0] = key_line
		if test_key(sock, U, C, key):
			key_ones = key_line
			break

	return assemble_key(key_zeros, key_ones)

def find_Ea(A, B, S_a):
	def modneg(a, q):
		if a == q-1:
			return -1
		else:
			return a

	return np.vectorize(modneg)(np.mod(B - np.dot(A, S_a), q), q)


##############
# CONNECTION #
##############

def recv_until(sock, s, s_buf):
	rep = sock.recv(s_buf)
	msg = rep
	while rep.find(s) == -1:
		rep = sock.recv(s_buf)
		msg += rep
	return msg

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("challenges1.france-cybersecurity-challenge.fr", 2002))

msg = recv_until(sock, b">>>", 4000)

beg_A = msg.find(b"A =")
beg_B = msg.find(b"B =")
beg_menu = msg.find(b"Possible actions")

A = np.reshape(np.frombuffer(decompress(b64d(msg[beg_A+4:beg_B-1])), dtype = np.int64), (n, n))
B = np.reshape(np.frombuffer(decompress(b64d(msg[beg_B+4:beg_menu-1])), dtype = np.int64), (n, n_bar))

S_a = []
for line in range(n):
	print(line)
	S_a.append(find_Sa_line(sock, line))
S_a = np.array(S_a)

E_a = find_Ea(A, B, S_a)

test_flag(sock, S_a, E_a)
