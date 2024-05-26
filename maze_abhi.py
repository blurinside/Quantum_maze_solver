from qiskit import QuantumCircuit as QC
from qiskit_aer import AerSimulator

import tkinter as tk

class QuantumWalkGUI:
    def __init__(self, master):
        self.master = master
        master.title("Quantum Walk GUI")

        self.canvas_width = 300
        self.canvas_height = 300

        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        self.run_simulation()

    def draw_maze(self, maze):
        cell_width = self.canvas_width / len(maze[0])
        cell_height = self.canvas_height / len(maze)

        for i in range(len(maze)):
            for j in range(len(maze[0])):
                x0, y0 = j * cell_width, i * cell_height
                x1, y1 = (j + 1) * cell_width, (i + 1) * cell_height
                if maze[i][j] == 1:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="black")
                else:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="white")

    def draw_path(self, maze, path):
        cell_width = self.canvas_width / len(maze[0])
        cell_height = self.canvas_height / len(maze)

        for i, j in path:
            x0, y0 = j * cell_width + cell_width / 4, i * cell_height + cell_height / 4
            x1, y1 = (j + 1) * cell_width - cell_width / 4, (i + 1) * cell_height - cell_height / 4
            self.canvas.create_oval(x0, y0, x1, y1, fill="red")

    def run_simulation(self):
        
        maze = [
            [0, 0, 1, 0, 1],
            [1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 1, 1, 0]

        ]

        
        num_qubits = 10  

        # Initialize the quantum circuit
        qc = QC(num_qubits, num_qubits)  
        for i in range(len(maze)):
            for j in range(len(maze[0])):
                if maze[i][j] == 0:  
                    # Encode the current position in the maze using qubits
                    qc.x(i)  # Set the qubit corresponding to the row index to |1>
                    qc.x(len(maze) + j)  

                   
                    qc.h(i)
                    qc.h(len(maze) + j)

                    
                    qc.measure(i, i)  
                    qc.measure(len(maze) + j, len(maze) + j)  

                   
                    qc.reset(i)
                    qc.reset(len(maze) + j)

       
        simulator = AerSimulator()
        result = simulator.run(qc).result()

      

        # Draw the maze and the path
        self.draw_maze(maze)
        self.draw_path(maze, [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2), (2, 3), (2, 4), (3, 4), (4, 4)])  

root = tk.Tk()
my_gui = QuantumWalkGUI(root)
root.mainloop()
