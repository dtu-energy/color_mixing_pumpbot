from typing import Tuple, Optional
import numpy as np
from pathlib import Path
from perqueue.constants import CYCLICALGROUP_KEY


def main(
        mixture: Tuple[float, float, float, float],
        measured_color: Tuple[float, float, float],
        target_color: Tuple[float, float, float],
        target_score: float = 10,
        **kwargs
    ) -> Tuple[bool, Optional[dict]]:

    measured_color = np.array(measured_color)
    target_color = np.array(target_color)
    rmse = np.sqrt(np.mean((measured_color - target_color)**2, axis=-1))
    score = np.sum(rmse)

    fpath = kwargs.get("log_filepath", "color_mixing_data.csv")
    log_path = Path(fpath)

    if not log_path.exists():
        with open(log_path, 'w') as f:
            f.write("red_ratio,green_ratio,blue_ratio,yellow_ratio,score\n")
    
    with open(log_path, 'a') as f:
        f.write("{},{},{},{},{}\n".format(
            *mixture, score
        ))
    # exist cyclical group
    exit_bool = False
    if score < target_score:
        exit_bool = True

    return True, {CYCLICALGROUP_KEY:exit_bool,"score": score, "target_color": target_color}


if __name__ == "__main__":
    _, score = main(
        mixture=[0.1, 0.1, 0.1, 0.1],
        measured_color=[12, 98, 80],
        target_color=[78, 23, 54],
        log_score=True,
    )

