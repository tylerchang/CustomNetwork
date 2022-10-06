from driver import receiveFrom, broadcastCharacters

username = input("Choose a username: ")
print("You may now type in chat!")

broadcastCharacters([1,2,3,4], username + " has joined the chat")

receiveFrom([1,2,3,4])

while True:
    message = input("")
    totalMessage = "[" + username + "]: " + message
    broadcastCharacters([1,2,3,4], totalMessage)