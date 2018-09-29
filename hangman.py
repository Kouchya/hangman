from socket import *
import re
import os
import platform
import sys

buffsize = 1024
status = 0

def clear():
	if platform.system() == 'Windows':
		os.system('cls')
	else:
		os.system('clear')

if __name__ == '__main__':
	args = sys.argv
	if len(args) < 2:
		print('Address and port not given. Exit.')
		sys.exit(1)
	if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+$', args[1]):
		print('Invalid argument.')
		print('Correct argument form is:')
		print('\t[IP addr]:[port]')
		sys.exit(2)
	address, port = args[1].split(':')
	client = socket(AF_INET, SOCK_STREAM)
	client.connect((address, int(port)))
	recv = client.recv(buffsize)
	if recv == '':
		print('Server not found!')
		client.close()
		sys.exit(0)
	status = int(recv)

	clear()
	print('Connected to address: %s on port %s.' % (address, port))
	print('Waiting for another player...')
	recv = client.recv(buffsize)
	print('Another player is in the room.')

	if status == 0:
		answer = ''
		while not re.match(r'^[a-zA-Z]+$', answer) or len(answer) < 6 or len(answer) > 30:
			clear()
			answer = raw_input('Answer word: ')
		answer = answer.upper()
		client.sendall(answer)
	else:
		clear()
		print('Waiting for the executer to input a word...')

	recv = client.recv(buffsize)
	while recv.startswith('guess:'):
		comp = recv.split(':')
		word = comp[1]
		guessed = list(comp[2])
		life = int(comp[3])

		clear()
		print
		print
		word_display = '\t'
		for letter in word:
			word_display += ' ' + letter
		print(word_display)
		print
		print('Life: %d' % life)
		print('Guessed: %s' % str(guessed))
		print

		if status == 1:
			guess = ''
			while not re.match(r'^[a-zA-Z]+$', guess):
				guess = raw_input('Next guess: ')
			guess = guess.upper()
			client.sendall(guess)
		else:
			print('Waiting for another player to guess...')

		recv = client.recv(buffsize)

	if recv.startswith('guessed:'):
		comp = recv.split(':')
		word = comp[1]
		guessed = list(comp[2])
		life = int(comp[3])
		
		clear()
		print
		print
		word_display = '\t'
		for letter in word:
			word_display += ' ' + letter
		print(word_display)
		print
		print('Life: %d' % life)
		print('Guessed: %s' % str(guessed))
		print

		if status == 0:
			print('The other player figured it out. Execution halted.')
		else:
			print('You figured it out. Execution halted.')
	elif recv.startswith('unguessed:'):
		comp = recv.split(':')
		word = comp[1]
		guessed = list(comp[2])
		life = int(comp[3])
		
		clear()
		print
		print
		word_display = '\t'
		for letter in word:
			word_display += ' ' + letter
		print(word_display)
		print
		print('Life: %d' % life)
		print('Guessed: %s' % str(guessed))
		print

		if status == 0:
			print('The other player failed to escape and is hanged.')
		else:
			print('You failed. You are hanged by the executer.')

	client.close()
