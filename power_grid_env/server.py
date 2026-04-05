import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI

from power_grid_env.env import PowerGridEnv
from power_grid_env.models import Action


app = FastAPI(title="Smart Power Grid Load Balancer")
env = PowerGridEnv()
env.reset()


@app.post("/reset")
def reset():
    return env.reset().model_dump()


@app.post("/step")
def step(action: Action):
    observation, reward, done, info = env.step(action)
    return {
        "observation": observation.model_dump(),
        "reward": reward,
        "done": done,
        "info": info,
    }


@app.get("/state")
def state():
    return env.state().model_dump()
