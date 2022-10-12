from processes import broadcast_to
import constants
from convertUtility import convert_dictionary_to_bytes
import time

def update_table(table):
    while True:
        broadcast_to([1,2,3,4], constants.TABLE_HEADER + convert_dictionary_to_bytes(table.get_table()))
        
        time.sleep(60)