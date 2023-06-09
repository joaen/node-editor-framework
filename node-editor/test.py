from node.sum_node import SumNode
from node.float_node import FloatNode
import node.editor as ne

sum_node = SumNode()
float_node_1 = FloatNode(10)
float_node_2 = FloatNode(2)
ne.create_connection(float_node_2.output_port, sum_node.input_port_1)
ne.create_connection(float_node_1.output_port, sum_node.input_port_2)

print(sum_node.output())

# ne.break_connection(float_node_1.output_port)
# print(sum_node.exsist)


float_node_2.output_port.data = 10
print(sum_node.output())

    
