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
        self.x_list = list()
        self.y_list = list()
        self.fig = None

    def plot_prioritized_practices(self):
        height = 0.
        self.x_list = list()
        self.y_list = []
        for i, practice in enumerate(self.prioritized_practices):
            self.y_list.append(height)
            self.x_list.append(i)
            height += practice.priority

        x = np.array(self.x_list)
        y = np.array(self.y_list)
        
        # Plotting the Graph
        self.fig = plt.figure()
        plt.plot(x, y)
        plt.title("The diagram of practices efficiency:")
        plt.xlabel("Prioritized practices")
        plt.ylabel("Value by implementing a practice")
    
    def plot_eval_score(self, score: float):
        self.plot_prioritized_practices()
        x_value = 0.
        for index, height in enumerate(self.y_list[1:], 1):
            if height >= score >= self.y_list[index-1]:
                x_start = self.x_list[index-1]
                x_end = self.x_list[index]
                y_start = self.y_list[index-1]
                y_end = height
                shift = (score-y_start) / (y_end-y_start)
                x_value = x_start + (x_end-x_start) * shift
                break
        x = np.array([0, x_value, x_value])
        y = np.array([score, score, 0])
        plt.plot(x, y)
        plt.text(0, score, 'Score = {:0.3}'.format(score), fontsize = 12)

    def draw(self):
        if not self.fig:
            self.plot_prioritized_practices()
        imgdata = StringIO()
        self.fig.savefig(imgdata, format='svg')
        imgdata.seek(0)

        data = imgdata.getvalue()
        return data