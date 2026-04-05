def grade(actions, env):
    if not env.regions or env.total_supply <= 0:
        return 0.0

    demand_score = 0.0
    for region in env.regions:
        diff = abs(region.supply - region.demand)
        demand_score += max(0.0, 1.0 - diff / (region.demand + 1e-6))
    demand_score /= len(env.regions)

    renewable_score = env.renewable_supply / (env.total_supply + 1e-6)
    efficiency_score = max(0.0, 1.0 - len(actions) / env.max_steps)

    final_score = 0.5 * demand_score + 0.3 * renewable_score + 0.2 * efficiency_score
    return float(max(0.0, min(1.0, final_score)))

