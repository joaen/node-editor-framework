from node.multiply_node import SumNode
from node.float_node import FloatNode

mult_node = SumNode()
float_node_1 = FloatNode(10)
float_node_2 = FloatNode(2)
mult_node.create_connection(float_node_2.output, mult_node.input_port_1)
mult_node.create_connection(float_node_1.output, mult_node.input_port_2)

# mult_node.create_connection(float_node_2.output, mult_node.input_port_2)
print(mult_node.output())


# node.create_connection(node.output_port_1, node_2.input_port_1)
# node.break_connection(node.output_port)

# print(node.output)
# print(node_2.input_1.is_connected)
# print(node.output.is_connected)

# node_2.node_operation()
# node.node_operation()

# print(node.output.data)
# print(node_2.output.data)