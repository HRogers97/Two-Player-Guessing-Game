####################################################################################################
# client.py
####################################################################################################
# Written by:  Hunter Rogers
# Date:        November 2019
#
# Descritpion: This is a client that connects to a server to play a guessing game.
#              Two clients will connect to the server and take turns trying to 
#              guess a random number.
#
# Usage:       python client.py port_number
####################################################################################################
import socket
import sys

# default buffer size for reading data from server
buffer = 1024
host = '10.39.167.34'

# input the port number to use 
inputs = sys.argv
if (len(inputs) < 2 ):
     port = 1632
else:
     port=int(inputs[1])

# Recieves a message from the server and prints to the screen
def RecieveMsg():
     msg = cs.recv(buffer).decode()
     print(msg)

# Flag to see if the game has been won
winFlag = "GAME OVER"

# Default to false to start game
gameisWon = False

# connect to the socket
print ("Connecting to ",host,":",port)
cs = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
cs.connect( (host,port) )

# Recieve connection message
RecieveMsg()

# Recieve message to start guessing
RecieveMsg()

# Check for opponent win
gameisWon = cs.recv(buffer).decode() == winFlag

while not gameisWon:
     # Get guess from user
     userinfo = input("Make your guess > ")

     # Encode and send guess to server
     guess = userinfo.encode()
     cs.send(guess)
     
     # receive self guess results
     guessResults = cs.recv(buffer).decode()
     print(guessResults)
     
     # Check for self win
     gameisWon = cs.recv(buffer).decode() == winFlag
     if(gameisWon):
          break
     else:
          # Recieve opponent guess results
          print("Please wait for other player to make their guess...")
          otherPlayerGuess = cs.recv(buffer).decode()
          print(otherPlayerGuess)
          
          # Check for opponent win
          gameisWon = cs.recv(buffer).decode() == winFlag
          if(gameisWon):
               break
