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
        df[column] = df[column].apply(ast.literal_eval)

    # Convert the lists of strings into lists of floats
    for column in df.columns:
        df[column] = df[column].apply(lambda x: [float(i) for i in x])
    
    return df

def write_to_logfile(mixture, measurement, target_mixture, target_measurement, logfile):
        
    """
    Takes the measurement and target data and logs this in the correct format.

    Parameters:
        mixture (list): The input mixture.
        measurement (list): The measurement.
        target_mixture (list): The target mixture.
        target_measurement (list): The target measurement.
        logfile (str): Path to logfile

    Returns:
        None
    """
    
    log_df = read_logfile(logfile)
    
    new_row = {
        'mixture': [','.join(map(str, mixture))], 
        'measurement': [','.join(map(str, measurement))], 
        'target_mixture': [','.join(map(str, target_mixture))], 
        'target_measurement': [','.join(map(str, target_measurement))]
    }

    append_df = pd.DataFrame(new_row, index = [0])

    

    # Convert the string representation of lists into actual lists
    for column in append_df.columns:
        append_df[column] = append_df[column].apply(ast.literal_eval)

    # Convert the lists of strings into lists of floats
    for column in append_df.columns:
        append_df[column] = append_df[column].apply(lambda x: [float(i) for i in x])

    if len(log_df) == 0:
        log_df = append_df
    else:
        log_df = pd.concat([log_df, append_df], ignore_index = True).reset_index(drop=True)


    log_df.to_csv(logfile, index=False)

    

