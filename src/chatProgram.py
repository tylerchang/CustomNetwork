from driver import receive_from, broadcast_characters

username = input("Choose a username: ")
print("You may now type in chat!")

receive_from([1,2,3,4])

while True:
    message = input("")
    totalMessage = "[" + username + "]: " + message

    broadcast_characters([1,2,3,4], totalMessage)
