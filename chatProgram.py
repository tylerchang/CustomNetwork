from driver import receiveFrom, broadcastTo

username = input("Choose a username: ")
print("You may now type in chat!")

receiveFrom([1,2,3,4])

while True:
    message = input("")
    totalMessage = "[" + username + "]: " + message
    broadcastTo([1,2,3,4], totalMessage)

