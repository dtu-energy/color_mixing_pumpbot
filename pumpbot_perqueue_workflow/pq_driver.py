from pathlib import Path

from perqueue import PersistentQueue, Task, Workflow, CyclicalGroup

here = Path(__file__).parent
target_score = 10
pumpbot_tasks_dir = here / "pumpbot_tasks"
bayesopt_tasks_dir = here / "odyssey_tasks"
data_csv_filepath = here / "color_mixing_data.csv"

# measure target colour
task1 = Task(pumpbot_tasks_dir / "measure_target.py", None, "local:5m")

# flush target colour
task2 = Task(pumpbot_tasks_dir / "reset_cell.py", None, "local:5m")

# Bayesian optimisation to predict next parameters
next_measurement = Task(
    bayesopt_tasks_dir / "get_next_parameters.py", 
    {
        "config_filepath": "odyssey_tasks/odyssey_config.json", 
        "data_filepath": "color_mixing_data.csv"
    }, 
    "local:5m")

# mix and measure predicted parameters
mix_and_measure = Task(pumpbot_tasks_dir / "mix_color.py", None, "local:5m")

# calculate score and write to data csv
calculate_score = Task(
    pumpbot_tasks_dir / "calculate_score.py", 
    {
        "log_filepath": "color_mixing_data.csv",
        "target_score": target_score
    }, 
    "local:5m")

# Define bayesian loop.
bayesian_loop = CyclicalGroup(
    [next_measurement,
    mix_and_measure,
    calculate_score], max_tries = 16
)

# Overall workflow
wf = Workflow({
    task1: [],
    task2: [task1],
    bayesian_loop: [task1, task2]
})

# Submit the worflow through PerQueue
with PersistentQueue() as pq:
    pq.submit(wf)
