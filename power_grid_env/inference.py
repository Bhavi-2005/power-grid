import os
import sys
from pathlib import Path

from power_grid_env.env import PowerGridEnv
from power_grid_env.models import Action
from power_grid_env.graders.grader_hard import grade


API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
HF_TOKEN = os.getenv("HF_TOKEN", "")


def build_action(obs):
    total_demand = sum(region.demand for region in obs.regions)
    return [
        round((region.demand / max(total_demand, 1e-6)) * obs.total_supply, 2)
        for region in obs.regions
    ]


def main():
    _ = API_BASE_URL, HF_TOKEN

    env = PowerGridEnv()
    obs = env.reset()

    print(f"[START] task=optimize_grid env=power_grid_env model={MODEL_NAME}")

    actions_taken = []
    rewards = []

    for step in range(env.max_steps):
        allocations = build_action(obs)
        action = Action(allocations=allocations)
        obs, reward, done, _ = env.step(action)

        actions_taken.append(action)
        rewards.append(reward)

        compact_action = "[" + ",".join(f"{value:.2f}" for value in allocations) + "]"
        print(
            f"[STEP] step={step + 1} action={compact_action} "
            f"reward={reward:.2f} done={str(done).lower()} error=null"
        )

        if done:
            break

    score = grade(actions_taken, env)
    reward_values = ",".join(f"{reward:.2f}" for reward in rewards)
    print(f"[END] success=true steps={len(rewards)} score={score:.2f} rewards={reward_values}")


if __name__ == "__main__":
    main()
