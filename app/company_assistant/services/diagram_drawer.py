from io import StringIO
from company_assistant.services.prioritizer import PriorityOrderedPracticeDTO
import numpy as np
import matplotlib.pyplot as plt
 

class DiagramDrawer():
    def __init__(
            self,
            prioritized_practices: PriorityOrderedPracticeDTO
        ) -> None:
        self.prioritized_practices = prioritized_practices
        self.fig = None

    def plot_prioritized_practices(self):
        height = 0.
        x_list = []
        y_list = []
        for i, practice in enumerate(self.prioritized_practices):
            y_list.append(height)
            x_list.append(i)
            height += practice.priority

        x = np.array(x_list)
        y = np.array(y_list)
        
        # Plotting the Graph
        self.fig = plt.figure()
        plt.plot(x, y)
        plt.title("The diagram of practices efficiency:")
        plt.xlabel("Prioritized practices")
        plt.ylabel("Value by implementing a practice")

    def draw(self):
        if not self.fig:
            self.plot_prioritized_practices()
        imgdata = StringIO()
        self.fig.savefig(imgdata, format='svg')
        imgdata.seek(0)

        data = imgdata.getvalue()
        return data