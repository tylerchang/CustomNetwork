from convertUtility import bytes_to_message

def process_chat(message):
     print(bytes_to_message(message))

def process_data(queue):
     while True:
          length = queue.qsize()
          if length == 0:
               continue
          process_chat(queue.get())