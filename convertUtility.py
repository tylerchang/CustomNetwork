import json

def message_to_bytes(message):
    encodedString = ''.join(format(ord(i), '08b') for i in message)
    return encodedString

def bytes_to_message(byte):
    return ''.join(chr(int(''.join(x), 2)) for x in zip(*[iter(byte)]*8))

def convert_dictionary_to_bytes(distanceVector):
    encodedDictionary = json.dumps(distanceVector)
    return message_to_bytes(encodedDictionary)
    
def convert_bytes_to_dictionary(table):
    dict_string = bytes_to_message(table)
    res_dict = json.loads(dict_string)
    return res_dict
