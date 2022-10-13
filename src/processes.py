from convertUtility import convert_dictionary_to_bytes
from sender import transmit_message
from receiver import listen_for_data
from convertUtility import bytes_to_message, message_to_bytes
from dataProcessor import process_data
from multiprocessing import Process, Queue, Array
import constants

busy_ports = Array('b', (False, False, False, False))
sender_queue = None
receiver_queue = None

def listen(port, data):
    listen_for_data(port, data)

def broadcast(message, ports):
    for port in ports:
        if not busy_ports[port - 1]:
            busy_ports[port - 1] = True

    transmit_message(message, ports)

    for port in ports:
        if busy_ports[port - 1]:
            busy_ports[port - 1] = False

def handle_sender_queue(queue):
    next_up = None
    while True:
        if queue.qsize() > 0:
            data = next_up if next_up else queue.get()
            message = data[0]
            ports = data[1]
            
            blocked_port = False
            for port in ports:
                if busy_ports[port - 1]:
                    next_up = data
                    blocked_port = True
                    break

            if blocked_port: 
                continue

            b1 = Process(target=broadcast, args=(message, ports))
            b1.start()

def create_receiver_queue(table):
    global receiver_queue
    receiver_queue = Queue()
    queue_thread = Process(target=process_data, args=(receiver_queue,table))
    queue_thread.start()


def create_sender_queue():
    global sender_queue
    sender_queue = Queue()
    queue_thread = Process(target=handle_sender_queue, args=(sender_queue,))
    queue_thread.start()

def receive_from(ports):
    for port in ports:
        thread = Process(target=listen, args=(port, receiver_queue))
        thread.start()

def broadcast_to(ports, message):
    global sender_queue
    total_message = message
    if (constants.LINK_MODE == "WAVE"):
        total_message += constants.STOP_SEQUENCE
    sender_queue.put((total_message, ports))

def broadcast_characters(ports, character_message):
    global sender_queue
    total_message = character_message
    converted_bytes = message_to_bytes(total_message)
    if (constants.LINK_MODE == "WAVE"):
        converted_bytes += constants.STOP_SEQUENCE
    sender_queue.put((converted_bytes, ports))
