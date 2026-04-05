def grade(actions, env):
    if not env.regions:
        return 0.0

    score = 0.0
    for region in env.regions:
        diff_ratio = abs(region.supply - region.demand) / max(region.demand, 1.0)
        score += max(0.0, 1.0 - diff_ratio)

    score /= len(env.regions)
    return float(max(0.0, min(1.0, score)))

