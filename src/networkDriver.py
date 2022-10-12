from vectorTable import vectorTable
from processes import receive_from, start_table_update_process

table = None
def drive_network():
    global table
    node_name = input("Create a name for this node: ")

    table = vectorTable(node_name)

    receive_from([1,2,3,4])

    start_table_update_process(table)

def get_table():
    global table
    return table