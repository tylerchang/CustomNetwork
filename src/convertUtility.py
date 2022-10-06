def message_to_bytes(message):
    encodedString = ''.join(format(ord(i), '08b') for i in message)
    return encodedString

def bytes_to_message(byte):

    return ''.join(chr(int(''.join(x), 2)) for x in zip(*[iter(byte)]*8))