from node.node import Node

node = Node(name="plus and plus", inputs={"input_1":int, "input_2":int}, outputs={"output_final":int})

data = node.input_ports.get("input_1")

# data.data = "ok"
print(data.data)



