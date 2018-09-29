from socket import *
import random
import signal

signal.signal(signal.SIGINT, do_exit)

address = '0.0.0.0'
port = 15025
buffsize = 1024

server = socket(AF_INET, SOCK_STREAM)
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server.bind((address, port))
server.listen(2)
print('Server running on port %d successfully.' % port)

while True:
	clients = []
	r = random.randint(0, 1)

	try:
		for i in [r, 1 - r]:
			client, addr = server.accept()
			print('Connection from ', addr)
			clients.append(client)
			client.sendall(str(i))

		if r:
			clients[0], clients[1] = clients[1], clients[0]

		for client in clients:
			client.sendall('start')

		answer = clients[0].recv(buffsize)
		word = '_' * len(answer)
		life = 8
		guessed = []

		while word != answer and life > 0:
			for client in clients:
				client.sendall('guess:%s:%s:%d' % (word, ''.join(guessed), life))
			guess = clients[1].recv(buffsize)
			for letter in guess:
				if letter not in guessed:
					guessed.append(letter)
					if letter in answer:
						word_list = list(word)
						for i in range(len(answer)):
							if answer[i] == letter:
								word_list[i] = letter
						word = ''.join(word_list)
						if word == answer:
							break
					else:
						life -= 1
						if life <= 0:
							break

		if word == answer:
			for client in clients:
				client.sendall('guessed:%s:%s:%d' % (word, ''.join(guessed), life))
		else:
			for client in clients:
				client.sendall('unguessed:%s:%s:%d' % (word, ''.join(guessed), life))
	except error, e:
		print('Client(s) disconnected.')
		for client in clients:
			client.close()
		continue

server.close()
