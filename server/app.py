from fastapi import FastAPI

from power_grid_env.env import PowerGridEnv
from power_grid_env.models import Action


app = FastAPI(
    title="Smart Power Grid Load Balancer",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

@app.get("/")
def home():
    return {"message": "Smart Power Grid Environment is running ⚡"}

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


def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
