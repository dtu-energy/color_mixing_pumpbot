# PumpBot

Controller code for the colour mixing platform developed by K. Gambhir, L. Nyeland, and R. Ziskason at DTU Energy

See also the [original repository](https://gitlab.com/auto_lab/47332-student-excercises) and its [API reference site](https://47332-student-excercises-auto-lab-a9486c744362dd41066bcfeabead9.gitlab.io/).

## Getting Started

### Dependencies

* python>=3.9
* pyserial
* numpy


### Installing

Clone the repo and change into the base directory. Then run

```
pip install .
```

### Usage

The package contains both functions to interface with the pumpbot hardware as well as an analogous set of functions for an in-silico digital twin, which can be used to demonstrate the colour mixing optimisation without the hardware.

For interfacing with the hardware, first initialise the pumpbot

```
from pump_controller import PumpController, get_serial_port, list_serial_ports
pumpbot = PumpController(
      ser_port = get_serial_port(), 
      cell_volume = 20, # mL 
      drain_time = 15, # seconds
      config_file = "config_files/config.json", # calibrated config that determines the flow rate of the pumps
  )
```

To measure the current RGB value of the cell (i.e. to measure a target mixed by hand)
```
target = pumpbot.measure()
```

Alternatively, a target color can be created by providing a mixture
```
mixture = [0.1, 0.5, 0.1, 0.5] # ratio of Red, Green, Blue, Yellow
pumpbot.change_target(mixture)
```

Colors can then be mixed and the resulting RGB value determined as follows. This can be implemented in an optimization loop to optimize to the target color

```
mixture = [0.2, 0.2, 0.5, 0.5] # ratio of Red, Green, Blue, Yellow
measured_color = pumpbot.mix_color(mixture) 
```

The in-silico digital twin has the same basic function handles for mixing colors but is initialised as

```
silicobot = SilicoPumpController(noise_std = 3)
```


