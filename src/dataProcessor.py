from convertUtility import bytes_to_message, convert_bytes_to_dictionary
import constants

def process_chat(message):
     print(bytes_to_message(message))

def process_table_update(table, table_update):
     neighbor_table = convert_bytes_to_dictionary(table_update)
     if neighbor_table is None:
         return
     for key in neighbor_table:
          if key in table:
               table[key] = min(table[key], 1 + neighbor_table[key])
          else:
               table[key] = 1 + neighbor_table[key]

     print(dict(table))
     
def process_data(queue, table):
     while True:
          length = queue.qsize()
          if length == 0:
               continue

          #process_chat(queue.get())

          bit_message = queue.get()
          print(bit_message)
          header = bit_message[:constants.HEADER_LENGTH]
          if (header == constants.TABLE_HEADER):
               print("received table update")
               process_table_update(table, bit_message[constants.HEADER_LENGTH:])
