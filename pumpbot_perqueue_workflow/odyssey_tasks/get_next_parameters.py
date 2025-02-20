import torch
import os
import json
import pandas as pd


from typing import Tuple, Optional

from odyssey.mission import Mission
from odyssey.navigators import SingleGP_Navigator

def read_data_csv(data_fpath):
    if not os.path.exists(data_fpath):
        return None
    
    return pd.read_csv(data_fpath)


def load_config(config_file: str) -> dict:
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config


def main(
        config_filepath: str,
        data_filepath: str,
        **kwargs
    ) -> Tuple[bool, Optional[dict]]:

    # read config file and set up BO (from kwargs or default)
    config = load_config(config_filepath)

    # return params
    params = config["params"]
    objectives = config["objectives"]

    mission = Mission(
        name = config["mission"]["name"],
        parameters=params,
        objectives=objectives,
        log_data=config["mission"]["log_data"],
    )

    navigator_args = config["navigator"]
    # set up navigator
    navigator = SingleGP_Navigator(
        mission = mission,
        **navigator_args,
    )

    # check log to see if any data (from kwargs or default)
    data_df = read_data_csv(data_filepath)

    # if data, update navigator
    if data_df is not None:
        param_names = [ x["name"] for x in params ]
        obj_names = [ x["name"] for x in objectives ]

        param_df = data_df[param_names]
        obj_df = data_df[obj_names]

        param_data = torch.Tensor(param_df.to_numpy())
        obj_data = torch.Tensor(obj_df.to_numpy())

        navigator.relay(param_data, obj_data)
        navigator.upgrade()
    

    # predict next sample(s)
    params = navigator.get_next_trial()
    params = params.squeeze().tolist() # convert to python list and remove empty dimension

    return True, {"mixture": params, "target_color": kwargs["target_color"]} # assuming order of data csv is correct

if __name__ == "__main__":
    _, params = main(
        config_filepath="odyssey_config.json",
        data_filepath="test_data.csv",
    )

    print(params)