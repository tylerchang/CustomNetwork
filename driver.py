from sender import transmit_message
from receiver import listen_for_data
from convertUtility import bytes_to_message, message_to_bytes
from dataProcessor import process_data
from multiprocessing import Process, Queue

def listen(port, data):
    listen_for_data(port, data)

def broadcast(message, ports):
    transmit_message(message, ports)

def receive_from(ports):
    data = Queue()

    create_queue_thread(data)

    for port in ports:
        thread = Process(target=listen, args=(port, data))
        thread.start()

def broadcast_to(ports, message):
    b1 = Process(target=broadcast, args=(message, ports))
    b1.start()

def broadcast_characters(ports, character_message):
    converted_bytes = bytes_to_message(character_message)
    b1 = Process(target=broadcast, args=(converted_bytes, ports))
    b1.start()

def create_queue_thread(queue):
    queue_thread = Process(target=process_data, args=(queue,))
    queue_thread.start()