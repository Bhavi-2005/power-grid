def grade(actions, env):
    if not actions:
        return 0.0

    safe_allocations = 0
    total_allocations = 0
    for action in actions:
        if hasattr(action, 'allocations'):
            vals = action.allocations
        elif isinstance(action, dict) and 'allocations' in action:
            vals = action['allocations']
        else:
            continue

        for value in vals:
            total_allocations += 1
            if value <= 120.0:
                safe_allocations += 1

    score = safe_allocations / total_allocations if total_allocations else 0.0
    return float(max(0.0, min(1.0, score)))
