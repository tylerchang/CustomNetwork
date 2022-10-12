from convertUtility import bytes_to_message, convert_bytes_to_dictionary
import constants

def process_chat(message):
     print(bytes_to_message(message))

def process_table_update(table_update):
     hash_table = convert_bytes_to_dictionary(table_update)
     
def process_data(queue):
     while True:
          length = queue.qsize()
          if length == 0:
               continue

          #process_chat(queue.get())

          bit_message = queue.get()

          header = bit_message[:constants.HEADER_LENGTH]

          if (header == constants.TABLE_HEADER):
               process_table_update(bit_message[constants.HEADER_LENGTH:])