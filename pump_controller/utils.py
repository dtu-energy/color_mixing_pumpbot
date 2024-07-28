import pandas as pd
import ast

def read_logfile(logfile):

    """
    Reads the logfile, converts lists in logfile to correct format and stores the data in a pd.DataFrame

    Parameters:
        logfile (str): Path to logfile

    Returns:
        pd.DataFrame: DataFrame with logfile data.
    """

    df = pd.read_csv(logfile)

    # Convert the string representation of lists into actual lists
    for column in df.columns:
        if column not in ['ph_measurement', 'target_ph']:
            df[column] = df[column].apply(ast.literal_eval)
        else:
            pass

    # Convert the lists of strings into lists of floats
    for column in df.columns:
        if column not in ['ph_measurement', 'target_ph']:
            df[column] = df[column].apply(lambda x: [float(i) for i in x])
        else:
            df[column] = df[column].apply(lambda x: float(x))
    
    return df

def write_to_logfile(mixture, measurement, ph_measurement, target_mixture, target_measurement, target_ph_measurement, logfile):
        
    """
    Takes the measurement and target data and logs this in the correct format.

    Parameters:
        mixture (list): The input mixture.
        measurement (list): The measurement.
        ph_measurement (float): The pH measurement.
        target_mixture (list): The target mixture.
        target_measurement (list): The target measurement.
        target_ph_measurement (float): The target ph measurement
        logfile (str): Path to logfile

    Returns:
        None
    """
    
    log_df = read_logfile(logfile)
    
    new_row = {
        'mixture': [','.join(map(str, mixture))], 
        'measurement': [','.join(map(str, measurement))], 
        'ph_measurement': str(ph_measurement),
        'target_mixture': [','.join(map(str, target_mixture))], 
        'target_measurement': [','.join(map(str, target_measurement))],
        'target_ph': str(target_ph_measurement)
    }

    append_df = pd.DataFrame(new_row, index = [0])

    

    # Convert the string representation of lists into actual lists
    for column in append_df.columns:
        if column not in ['ph_measurement', 'target_ph']:
            append_df[column] = append_df[column].apply(ast.literal_eval)
        else:
            pass

    # Convert the lists of strings into lists of floats
    for column in append_df.columns:
        print(column)
        if column not in ['ph_measurement', 'target_ph']:
            append_df[column] = append_df[column].apply(lambda x: [float(i) for i in x])
        else:
            append_df[column] = append_df[column].apply(lambda x: float(x))

    if len(log_df) == 0:
        log_df = append_df
    else:
        log_df = pd.concat([log_df, append_df], ignore_index = True).reset_index(drop=True)


    log_df.to_csv(logfile, index=False)

    

