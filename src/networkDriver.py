from multiprocessing import Manager, Process
import time
import constants
from processes import broadcast_to, create_receiver_queue, create_sender_queue, receive_from
from convertUtility import convert_dictionary_to_bytes

def drive_network():
    node_name = input("Create a name for this node: ")

    with Manager() as manager:
        table = manager.dict()

        create_sender_queue()
        create_receiver_queue(table)

        receive_from([1,2,3,4])

        table[node_name] = 0

        update_process = Process(target=update_neighbors, args=(table,))

        update_process.start()


def update_neighbors(table):
    while True:
        broadcast_to([1,2,3,4], constants.TABLE_HEADER + convert_dictionary_to_bytes(table))

        time.sleep(constants.UPDATE_TABLE_INTERVAL)

if __name__ == '__main__':
    drive_network()