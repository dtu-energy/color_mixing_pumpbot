import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch

def choose_text_color(background_color):
    # Normalize RGB values to the range [0, 1]
    normalized_background_color = [value / 255.0 for value in background_color]

    # Calculate relative luminance
    luminance = 0.299 * normalized_background_color[0] + 0.587 * normalized_background_color[1] + 0.114 * normalized_background_color[2]

    # Choose text color based on luminance
    text_color = 'black' if luminance > 0.5 else 'white'

    return text_color

def visualize_rgb(mixture, rgb, pump_controller, target = 'pump_controller', score = None):

    """
    Visualizes RGB data using a pie chart and circles.

    Parameters:
    - mixture (numpy.ndarray): Array of 4 float values representing the color mixture.
    - rgb (numpy.ndarray): Array of 3 float values representing the measured RGB color.
    - pump_controller (object): An object containing information about the pump controller.
    - target (str, list, np.ndarray, torch.Tensor, optional): Specifies the target color for comparison.
      If 'pump_controller', it uses the target color from the pump_controller object.
      If None, no target is visualized.
      If a list, np.ndarray, or torch.Tensor, it is considered as a specific RGB target color.
    - score (float, optional): A score associated with the visualization.

    Returns:
    - None

    Notes:
    - The function plots a pie chart around a circle representing the color mixture and
      a smaller circle representing the specified or pre-defined pump_controller target color.
    - The function also adds an annotation with the provided score at the center of the plot.
    - RGB values should be in the range [0, 255]. The function normalizes them to [0, 1] for plotting.
    """


    fig, ax = plt.subplots()

    if np.sum(mixture) == 0:
        mixture = np.array([0.25, 0.25, 0.25, 0.25])
    else:
        mixture /= np.sum(mixture) / 1.0

    def add_score(background_color):
        if score != None:
            plt.annotate(np.round(score,2), (0,0), fontsize = 14, 
                        ha = 'center', va = 'center',
                        color = choose_text_color(background_color))

    # Plot the pie chart around the circle with percentage values
    pie = ax.pie(mixture, 
                colors=['red', 'green', 'blue', 'yellow'], radius=1, startangle=90, 
                center = (0,0), wedgeprops=dict(edgecolor='black', linewidth=1))
    
    # Plot the circle with the specified RGB color
    circle = plt.Circle((0, 0), 0.9, edgecolor='black', linewidth=1, 
                        facecolor=np.divide(rgb, 255.0))
    ax.add_artist(circle)


    if isinstance(target, (type(None), str)):
        if target == 'pump_controller':
            # Plot the circle with the target RGB color from the pump_controller
            circle2 = plt.Circle((0, 0), 0.45, edgecolor='black', linewidth=1, 
                                facecolor=np.divide(pump_controller.target_color, 255.0))
            ax.add_artist(circle2)

            add_score(pump_controller.target_color)
        elif target == None:
            pass
        else:
            pass
    else:
        assert isinstance(target, (list, np.ndarray, torch.Tensor)), "Target must be a list, np.array, or torch.Tensor"
        assert len(target) == 3, "Target must have a length of 3"

        # Plot the circle with the specified target RGB color
        circle2 = plt.Circle((0, 0), 0.45, edgecolor='black', linewidth=1, 
                            facecolor=np.divide(target, 255.0))
        ax.add_artist(circle2)

        add_score(target)


    


    ax.set_aspect('equal', adjustable='box')

    plt.xlim(-1.1, 1.1)
    plt.ylim(-1.1, 1.1)

    plt.show()



def visualize_candidates(data_df):

    """
    Visualizes candidate mixture data using pie charts for mixtures, measured colors, and target colors.

    Parameters:
    - data_df (pd.DataFrame): A pandas DataFrame containing four columns:
        - Column 0: List of mixtures.
        - Column 1: List of measurement.
        - Column 2: List of target measurements.
        - Column 3: List of scores.

    Returns:
    - None

    Notes:
    - The function creates a plot with pie charts for mixtures, measured colors, and target colors
      for each candidate, organized in a horizontal layout, with the score on the vertical axis.
    - Pie charts are drawn using the draw_pie helper function.
    - RGB values for measured and target colors should be in the range [0, 255]. The function normalizes them to [0, 1] for plotting.
    """

    def draw_pie(dist, 
             xpos, 
             ypos, 
             size, 
             fill_color = None,
             ax=None):

        # for incremental pie slices
        cumsum = np.cumsum(dist)
        cumsum = cumsum/ cumsum[-1]
        pie = [0] + cumsum.tolist()

        colors = {0: 'red', 1: 'green', 2: 'blue', 3: 'yellow'}

        col = 0
        for r1, r2 in zip(pie[:-1], pie[1:]):
            angles = np.linspace(2 * np.pi * r1, 2 * np.pi * r2)
            x = [0] + np.cos(angles).tolist()
            y = [0] + np.sin(angles).tolist()

            xy = np.column_stack([x, y])

            if fill_color == None:
                ax.scatter([xpos], [ypos], marker=xy, s=size, color = colors[col])
            else:
                ax.scatter([xpos], [ypos], marker=xy, s=size, color = fill_color)


            col += 1

        return ax

    # Reformat the dataframe to make all lists numpy (hacky, but works)
    data_df = data_df[['mixture', 'measurement', 'target_measurement', 'score']]

    data_list = data_df.T.values.tolist()
    data_list = [np.array(col) for col in data_list]

    data_df = pd.DataFrame({'mixture': list(data_list[0]),
                            'measurement': list(data_list[1]),
                            'target': list(data_list[2]),
                            'score': data_list[3].reshape(len(data_list[2]))})

    target_size = 500
    mixture_size = 3000
    measured_size = 2000

    fig, ax = plt.subplots(figsize = (14,10))

    for i in range(len(data_df)):
        draw_pie(data_df.mixture[i], i+1, data_df.score[i], mixture_size, fill_color = None, ax = ax) # Mixture
        draw_pie([1.0], i+1, data_df.score[i], measured_size, fill_color=list(data_df.measurement[i]/255), ax = ax) # Measured color
        draw_pie([1.0], i+1, data_df.score[i], target_size, fill_color=list(data_df.target[i]/255), ax = ax) # Target color

    plt.xlim(0, len(data_df)+1)
    plt.ylim(data_df.score.min() - 8, data_df.score.max() + 8)

    plt.xlabel('Test #')
    plt.ylabel('Score')
    plt.show()

