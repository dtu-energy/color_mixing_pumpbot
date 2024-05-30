import numpy as np
import os
import datetime
import pandas as pd
from .utils import read_logfile, write_to_logfile

class SilicoPumpController:
    def __init__(self, noise_std):

        """
        Initializes a SilicoPumpController object.

        Parameters:
        - noise_std (float): Standard deviation of noise to be added during color mixing.

        Returns:
        - None

        Notes:
        - Initializes attributes for noise standard deviation, target mixture, and target color.
        - Creates a "silicologs" folder if it doesn't exist and a log file with the current date and time.
        """

        self.noise_std = noise_std

        self.target_mixture = [0.25, 0.25, 0.25, 0.25]
        self.target_color = [255, 255, 255] 

        # Create "logs" folder if it doesn't exist
        if not os.path.exists('silicologs'):
            os.makedirs('silicologs')

        # Create a log file with the current date and time and write column names
        now = datetime.datetime.now()
        self.log_file = f"silicologs/silicolog_{now.strftime('%d%m%Y_%H%M%S')}.csv"
        log_df = pd.DataFrame(columns=['mixture', 'measurement', 'target_mixture', 'target_measurement'])
        log_df.to_csv(self.log_file, index=False)


    def mix_color(self, col_list, changing_target = False):

        """
        Mixes colors based on the provided color coefficients and adds noise.

        Parameters:
        - col_list (list or numpy.ndarray): List of color coefficients for mixing.
        - changing_target (bool, optional): If True, the mixing is considered as changing the target.

        Returns:
        - numpy.ndarray: The mixed color with added noise.

        Notes:
        - Uses true color coefficients to mix colors and adds noise with the specified standard deviation.
        - Appends color mixture and measurement data to the log file unless changing_target is True.
        """

        true_coefficients = np.array([[255, 0, 0],
                                  [0, 255, 0],
                                  [0, 0, 255],
                                  [255, 255, 0]]
                                  )
        
        # If all coefficients are zero, set them to a small value to avoid division by zero
        if col_list == [0, 0, 0, 0]:
            min = 1e-5
            col_list = [min, min, min, min]

        # Normalization
        col_list = np.array(col_list).reshape(4,) # Make sure that input list has np shape (4,)
        col_list[col_list < 0] = 0
        col_list = np.divide(col_list, np.sum(col_list))
        
        mixed_color = np.dot(col_list, true_coefficients)
        noise = np.random.normal(0, self.noise_std, mixed_color.shape)
        mixed_color_with_noise = np.clip(mixed_color + noise, 0, 255)

        if not changing_target:
            # Append color mixture and measurement data to the log file
            write_to_logfile(col_list, mixed_color_with_noise, self.target_mixture, self.target_color, self.log_file)

        return mixed_color_with_noise

    def change_target(self, target_mixture):

        """
        Changes the target mixture and computes the corresponding target color.

        Parameters:
        - target_mixture (list or numpy.ndarray): New target color mixture.

        Returns:
        - numpy.ndarray: The new target color.

        Notes:
        - Updates target_mixture and target_color attributes.
        - Prints information about the change.
        """

        self.target_mixture = target_mixture
        self.target_color = self.mix_color(target_mixture, changing_target = True)

        print(f"Silico target changed to {self.target_color}. Created by {self.target_mixture}.")

        return self.target_color

    



    
    


       