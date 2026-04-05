# Smart Power Grid Load Balancer

## Problem Description

Modern electric grids must distribute energy efficiently across regions, avoid overloads, and integrate renewable energy without compromising reliability. This project models that challenge as a reinforcement learning environment where an agent chooses how to allocate electricity at each step.

## Why It Matters

Power balancing is a real operational problem for utilities and grid operators. A controllable simulation environment makes it easier to test strategies for demand matching, overload prevention, and renewable prioritization before deployment in higher-fidelity systems.

## Goal

The agent should:

- allocate electricity across regions
- prevent overload conditions
- minimize waste and poor balancing
- make effective use of renewable energy

## Observation Space

Each observation contains:

- `regions`: list of regional demand and current supply
- `total_supply`: total available electricity for the current step
- `renewable_supply`: renewable energy available for the current step
- `time_step`: current episode step

## Action Space

The action is a list of three floating-point allocations, one for each region:

```python
Action(allocations=[north_power, central_power, south_power])
```

## Reward Design

The reward changes every step and combines:

- positive reward for matching each region's demand
- penalties for under-supplying demand
- penalties for overloading a region beyond a safe margin
- penalties for allocating more than total available supply
- bonus for using renewable energy effectively

This creates dense feedback rather than a single final reward.

## Task Details

### Easy: `avoid_overload`

Focus on keeping allocations within safe bounds.

### Medium: `balance_demand`

Focus on matching regional demand as closely as possible.

### Hard: `optimize_grid`

Balance demand satisfaction, total supply utilization, and renewable usage together.

## Project Structure

```text
power_grid_env/
├── env.py
├── models.py
├── __init__.py
├── tasks/
├── graders/
├── inference.py
├── openenv.yaml
├── Dockerfile
├── requirements.txt
├── README.md
└── server/
    ├── __init__.py
    └── app.py
```

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Optional environment variables:

```bash
API_BASE_URL=https://router.huggingface.co/v1
MODEL_NAME=Qwen/Qwen2.5-72B-Instruct
HF_TOKEN=your_token_here
```

Run inference:

```bash
python inference.py
```

Run API server:

```bash
uvicorn server:app --host 0.0.0.0 --port 7860
```

Run with Docker:

```bash
docker build -t power-grid .
docker run -p 8000:8000 power-grid
```

The API will be available at http://localhost:8000/docs

Validate the environment:

```bash
openenv validate
```

## Example Output

```text
[START] task=optimize_grid env=power_grid_env model=Qwen/Qwen2.5-72B-Instruct
[STEP] step=1 action=[76.46,65.26,50.20] reward=0.74 done=false error=null
[STEP] step=2 action=[77.36,69.85,47.24] reward=0.74 done=false error=null
[END] success=true steps=10 score=0.74 rewards=0.74,0.74,0.74,0.74,0.74,0.74,0.74,0.74,0.74,0.74
```
