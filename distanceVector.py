class distanceVector:
    table = None
    def __init__(self, current_node_name):
        # initializes current node with a distance of 0 on the vector
        self.table = {current_node_name : 0}
    def add_node(self, node_name, distance_from_node):
        if node_name in self.table:
            print(node_name + " already in table")
        else:
            self.table[node_name] = distance_from_node
    def edit_node_distance(self, node_name, new_distance):
        if node_name not in self.table:
            print(node_name + " not in table")
        else:
            self.table[node_name] = new_distance
    def remove_node(self, node_name):
        if node_name not in self.table:
            print(node_name + " not in table")
        else:
            self.table.pop(node_name, None)
    def get_vector(self):
        return self.table
    def print_table(self):
        for key in self.tables:
            print("Node: " + key + ", Distance: " + self.tables[key])
    


        
