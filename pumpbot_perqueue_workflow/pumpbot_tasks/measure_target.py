from pump_controller import PumpController, get_serial_port, list_serial_ports
from pump_controller import visualize_rgb
import numpy as np
from typing import Tuple, Optional, Sequence

from pump_controller import SilicoPumpController, visualize_rgb
import numpy as np


def main(**kwargs) -> Tuple[bool, Optional[dict]]:

    if kwargs.get("dummy_target", False):
        return True, {"target_color": [165, 30, 31]}
    
    pumpbot = PumpController(
        ser_port = get_serial_port(), 
        cell_volume = kwargs.get("cell_volume", 20), 
        drain_time = kwargs.get("drain_time", 15),
        config_file = kwargs.get("config_fpath", "config_files/config.json"),
    )

    measured_color = pumpbot.measure()

    return True, {"target_color": measured_color}

