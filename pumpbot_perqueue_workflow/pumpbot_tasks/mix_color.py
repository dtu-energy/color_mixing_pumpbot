from pump_controller import PumpController, get_serial_port, list_serial_ports
# from pump_controller import visualize_rgb
import numpy as np
from typing import Tuple, Optional, Sequence

from pump_controller import SilicoPumpController, visualize_rgb
import numpy as np

def main(mixture: Tuple[float, float, float, float], **kwargs) -> Tuple[bool, Optional[dict]]:

    if not isinstance(mixture, Sequence) or len(mixture) != 4:
        raise ValueError("mixture must be form (R, G, B, Y)")
    
    pumpbot = PumpController(
        ser_port = get_serial_port(), 
        cell_volume = kwargs.get("cell_volume", 20), 
        drain_time = kwargs.get("drain_time", 15),
        config_file = kwargs.get("config_fpath", "config_files/config.json"),
    )

    measured_color = pumpbot.mix_color(mixture)

    return True, {"measured_color": measured_color, "mixture": mixture, "target_color": kwargs["target_color"]}

if __name__ == "__main__":
    _, data = main([0.1, 0.2, 0.3, 0.4])
