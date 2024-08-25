import tkinter as tk
from tkinter import ttk
import basic
from graphviz import Digraph

# def display_ast(node, graph, parent=None):
#     if isinstance(node, basic.NumberNodes):
#         graph.node(str(node.tok.pos_start.line) + '-' + str(node.tok.pos_start.col), str(node.tok.value))
#         if parent:
#             graph.edge(parent, str(node.tok.pos_start.line) + '-' + str(node.tok.pos_start.col))
#     elif isinstance(node, basic.BinOpNode):
#         graph.node(str(node.op_tok.pos_start.line) + '-' + str(node.op_tok.pos_start.col), str(node.op_tok.type))
#         if parent:
#             graph.edge(parent, str(node.op_tok.pos_start.line) + '-' + str(node.op_tok.pos_start.col))
#         display_ast(node.left_node, graph, str(node.op_tok.pos_start.line) + '-' + str(node.op_tok.pos_start.col))
#         display_ast(node.right_node, graph, str(node.op_tok.pos_start.line) + '-' + str(node.op_tok.pos_start.col))
#     elif isinstance(node, basic.UnnaryOpNode):
#         graph.node(str(node.op_tok.pos_start.line) + '-' + str(node.op_tok.pos_start.col), str(node.op_tok.type))
#         if parent:
#             graph.edge(parent, str(node.op_tok.pos_start.line) + '-' + str(node.op_tok.pos_start.col))
#         display_ast(node.node, graph, str(node.op_tok.pos_start.line) + '-' + str(node.op_tok.pos_start.col))
def display_ast(node, graph, parent=None):
    if isinstance(node, basic.NumberNodes):
        value = node.evaluate()
        graph.node(str(node.tok.pos_start.line) + '-' + str(node.tok.pos_start.col), f'{value}\n{node.tok}')
        if parent:
            graph.edge(parent, str(node.tok.pos_start.line) + '-' + str(node.tok.pos_start.col))
    elif isinstance(node, basic.BinOpNode):
        op_value = node.op_tok.type
        result_value = node.evaluate()
        graph.node(str(node.op_tok.pos_start.line) + '-' + str(node.op_tok.pos_start.col), f'{op_value}\n{result_value}')
        if parent:
            graph.edge(parent, str(node.op_tok.pos_start.line) + '-' + str(node.op_tok.pos_start.col))
        display_ast(node.left_node, graph, str(node.op_tok.pos_start.line) + '-' + str(node.op_tok.pos_start.col))
        display_ast(node.right_node, graph, str(node.op_tok.pos_start.line) + '-' + str(node.op_tok.pos_start.col))
    elif isinstance(node, basic.UnnaryOpNode):
        op_value = node.op_tok.type
        result_value = node.evaluate()
        graph.node(str(node.op_tok.pos_start.line) + '-' + str(node.op_tok.pos_start.col), f'{op_value}\n{result_value}')
        if parent:
            graph.edge(parent, str(node.op_tok.pos_start.line) + '-' + str(node.op_tok.pos_start.col))
        display_ast(node.node, graph, str(node.op_tok.pos_start.line) + '-' + str(node.op_tok.pos_start.col))

def generate_string():
    input_string = entry.get()
    result,value, error = basic.run('<stdin>', input_string)
    if error:
        output_label.config(text=error.as_string())
    else:
        output_label.config(text=result)
        graph = Digraph('AST', filename='ast.gv')
        display_ast(result, graph)
        graph.view()
        # output_label.config(text=result)

# Create the main window
root = tk.Tk()
root.title("String Generator")

# Create a label and entry widget for input
label = tk.Label(root, text="Enter a string:")
label.pack(pady=10)
entry = tk.Entry(root)
entry.pack(pady=5)

# Create a button to generate the string
generate_button = tk.Button(root, text="Generate", command=generate_string)
generate_button.pack(pady=5)

# Create a label to display the generated string
output_label = tk.Label(root, text="")
output_label.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()

# (1+2)-5/(-2*3)
# (4/3)-2*3/4
# (-1+2.5)-5/(2*3)
