from __future__ import annotations

import random
from typing import Dict, List, Tuple

from .models import Action, Observation, Region


class PowerGridEnv:
    """Deterministic power grid environment with step-varying demand and supply."""

    def __init__(self) -> None:
        self.max_steps = 10
        self.current_step = 0
        self.tasks = [
            {"id": "easy"},
            {"id": "medium"},
            {"id": "hard"}
        ]
        self.region_names = ["North", "Central", "South"]
        self.base_demands = [80.0, 65.0, 50.0]
        self.demand_patterns = [
            [0.95, 1.00, 1.05],
            [1.00, 1.08, 0.92],
            [1.10, 0.96, 1.00],
            [1.18, 1.02, 0.90],
            [1.05, 1.12, 0.98],
            [0.98, 1.05, 1.08],
            [0.92, 0.97, 1.15],
            [1.08, 0.94, 1.10],
            [1.12, 1.00, 0.95],
            [1.00, 1.10, 1.02],
        ]
        self.total_supply_schedule = [
            205.0,
            198.0,
            210.0,
            202.0,
            207.0,
            200.0,
            196.0,
            204.0,
            208.0,
            201.0,
        ]
        self.renewable_supply_schedule = [
            72.0,
            68.0,
            76.0,
            64.0,
            70.0,
            78.0,
            60.0,
            74.0,
            69.0,
            73.0,
        ]
        self.regions: List[Region] = []
        self.total_supply = 0.0
        self.renewable_supply = 0.0

    def reset(self) -> Observation:
        self.current_step = 0
        self._sync_state(fluctuate=False)
        return self._get_obs()

    def step(self, action: Action | Dict[str, List[float]] | List[float]) -> Tuple[Observation, float, bool, Dict[str, float]]:
        parsed_action = self._parse_action(action)
        allocations = [max(0.0, value) for value in parsed_action.allocations]

        if len(allocations) != len(self.regions):
            raise ValueError("Action must include one allocation per region.")

        total_allocated = sum(allocations)
        reward = 0.0

        for region, allocated in zip(self.regions, allocations):
            region.supply = allocated
            demand = region.demand

            reward += max(0.0, 1.0 - abs(allocated - demand) / (demand + 1e-6))

            if allocated < demand:
                reward -= 0.3

            if allocated > demand * 1.2:
                reward -= 0.5

        renewable_ratio = min(total_allocated, self.renewable_supply) / (self.total_supply + 1e-6)
        reward += renewable_ratio * 0.5

        reward += max(0.0, 1.0 - self.current_step / self.max_steps) * 0.2

        if total_allocated > self.total_supply:
            reward -= 0.4

        reward += max(0.0, 1.0 - total_allocated / (self.total_supply + 1e-6)) * 0.3

        reward = round(max(0.0, min(1.0, reward)), 2)

        info = {
            "total_allocated": float(total_allocated),
            "renewable_ratio": float(renewable_ratio),
        }

        self.current_step += 1
        done = self.current_step >= self.max_steps
        if not done:
            self._sync_state()

        observation = self._get_obs()
        return observation, float(reward), bool(done), info

    def state(self) -> Observation:
        return self._get_obs()

    def _sync_state(self, fluctuate: bool = True) -> None:
        pattern = self.demand_patterns[self.current_step]
        updated_regions = []
        for name, base, factor in zip(self.region_names, self.base_demands, pattern):
            demand = base * factor
            if fluctuate:
                demand = max(10.0, demand + random.uniform(-5.0, 5.0))
            updated_regions.append(Region(name=name, demand=demand, supply=0.0))

        self.regions = updated_regions
        self.total_supply = self.total_supply_schedule[self.current_step]
        self.renewable_supply = self.renewable_supply_schedule[self.current_step]

    def _parse_action(self, action: Action | Dict[str, List[float]] | List[float]) -> Action:
        if isinstance(action, Action):
            return action
        if isinstance(action, list):
            return Action(allocations=action)
        if isinstance(action, dict):
            return Action(**action)
        raise TypeError("Unsupported action format.")

    def _get_obs(self) -> Observation:
        return Observation(
            regions=[Region(**region.model_dump()) for region in self.regions],
            total_supply=float(self.total_supply),
            renewable_supply=float(self.renewable_supply),
            time_step=int(self.current_step),
        )

    def close(self) -> None:
        """Placeholder for cleanup hooks."""
        return None

    def get_tasks(self) -> List[Dict[str, str]]:
        return self.tasks

