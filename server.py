####################################################################################################
# server.py
####################################################################################################
# Written by:  Hunter Rogers
# Date:        November 2019
#
# Descritpion: This is a server that takes in two clients and generates a random number, then
#              the two clients then have to take turns trying to guess the random number.
#              After guessing, the client is told if they were too high, too low, or correct.
#              First client to correctly guess the random number wins the game.
#
# Usage:       python server.py port_number
####################################################################################################
import socket
import sys
import random
import time

####################################################################################################
# Gets the guess from the client and checks if it is correct
# If it is not correct, it will tell the client if they are too high or too low
# This returns a boolean that is true if the guess was correct
def GetGuess(client_obj, clientNum):
    # Flag to end the game
    # Return true if the guess was correct, false if not
    correct = False

    # Get guess from client
    data = client_obj.recv(buffer)

    # convert data into a string, and print to screen
    datastr = data.decode()
    print("DEBUG: Client #" + str(clientNum) + "'s guess: " + datastr)

    # Tell the client about their guess
    if(int(datastr) == randNum):
        print("DEBUG: Correct, client #" + str(clientNum) + " wins")
        client_obj.send("Correct, you win!".encode())
        correct = True
    elif(int(datastr) > randNum):
        print("DEBUG: Too high")
        client_obj.send("Too high, try again".encode())
    else:
        print("DEBUG: too low")
        client_obj.send("Too low, try again".encode())

    return correct
####################################################################################################

# Max number of clients that can be waiting to connect
backlog = 2

# Default buffer size (for reading in data from client)
buffer = 1024

# Computer that is hosting the server
host = "10.39.167.34"

# Input the port number to use
# Default to 1632 if no port number is entered
inputs = sys.argv
if (len(inputs) < 2 ):
    port = 1632
else:
    port=int(inputs[1])

print("Openning socket on port " + str(port))

# create the socket (TCP/IP)
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind ( (host,port) )  # note that input into bind is a tuple

# set us up as a listening server (listens for clients to connect)
s.listen(backlog)

# Flags
winFlag = "GAME OVER"
notWinFlag = "GAME NOT OVER"

# Sleep time to seperate messages sent to clients
sleepTime = 0.1

# Get random number
randNum = random.randint(0,1000)

while True:
    # Greet client 1
    print ("DEBUG: waiting for client #1 to connect")
    client_obj1, client_addr = s.accept()
    print ("DEBUG: Client #1 has connected")
    client_obj1.send("Connected: you are player #1 \nPlease wait for player #2 to connect".encode())

    # Greet client 2
    print ("DEBUG: waiting for client #2 to connect")
    client_obj2, client_addr = s.accept()
    print ("DEBUG: Client #2 has connected")
    client_obj2.send("Connected: you are player #2 \nEveryone has connected, game will now begin \nPlease wait for player #1 to make a guess...".encode())

    print("DEBUG: Everyone has connected, game will now begin")
    client_obj1.send("Player #2 has connected, game will now begin".encode())

    time.sleep(sleepTime) # Make sure messages are sent separately

    # Send false win flag to client #1 to start game
    client_obj1.send(notWinFlag.encode())

    # Loop until client disconnects or finishes the game
    while True:

        # Get guess from client #1
        correctGuess = GetGuess(client_obj1, 1)
        time.sleep(sleepTime) # Make sure messages are sent separately

        if(correctGuess):

            # Tell client 2 that they lost
            winMsg = "Player #1 has won, number was" + str(randNum)
            client_obj2.send(winMsg.encode())

            time.sleep(sleepTime) # Make sure messages are sent separately

            # Send flags to clients to end the game
            client_obj1.send(winFlag.encode())
            client_obj2.send(winFlag.encode())

            break
        else:
            # Tell client 2 that it is their time to guess
            client_obj2.send("Player #1 has guessed wrong".encode())

            time.sleep(sleepTime) # Make sure messages are sent separately

            # Send flags to clients to keep the game going
            client_obj1.send(notWinFlag.encode())
            client_obj2.send(notWinFlag.encode())

        # Get guess from client #2
        correctGuess = GetGuess(client_obj2, 2)
        time.sleep(sleepTime) # Make sure messages are sent separately

        if(correctGuess):

            # Tell client 1 that they lost
            winMsg = "Player #2 has won, number was" + str(randNum)
            client_obj1.send(winMsg.encode())

            time.sleep(sleepTime) # Make sure messages are sent separately
            
            # Send flags to clients to end the game
            client_obj1.send(winFlag.encode())
            client_obj2.send(winFlag.encode())

            break
        else:
            # Tell client 1 that it is their time to guess
            client_obj1.send("Player #2 has guessed wrong".encode())

            time.sleep(sleepTime) # Make sure messages are sent separately

            # Send flags to clients to keep the game going
            client_obj1.send(notWinFlag.encode())
            client_obj2.send(notWinFlag.encode())
    
    print ("DEBUG: Game has ended")
    break