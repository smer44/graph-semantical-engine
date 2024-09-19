import tkinter as tk


class ViewNodeDummyDisplay(tk.Tk):
    def __init__(self, nodes):
        super().__init__()
        self.title("ViewNode Display")
        self.canvas = tk.Canvas(self, width=800, height=600, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.nodes = nodes
        self.colors = ["black", "lightgreen", "lightcoral", "lightgoldenrod", "lightpink", "lightsalmon",
                       "lightseagreen"]


        self.draw_nodes()

    def draw_nodes(self):
        self.counter = 0
        for n,node in enumerate(self.nodes):
            self.draw_node(node)

    def draw_node(self, node):
        color = self.colors[self.counter%len(self.colors)]
        print("draw: " , node)
        self.counter+=1
        # Draw the rectangle corresponding to the ViewNode
        self.canvas.create_rectangle(
            #*node.rect,
            node.left,node.bottom,node.right,node.top,
            outline=color, fill=None
        )
        # Optionally, you can add text inside the rectangle to display the node information
        self.canvas.create_text(
            (node.left + node.right) / 2,
            (node.top + node.bottom) / 2,
            text=str(node.value),
            fill=color
        )
        # If the node has children, recursively draw them
        #for child in node.view_children:
        #    self.draw_node(child)
