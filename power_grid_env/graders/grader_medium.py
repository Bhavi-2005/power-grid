def grade(actions, env):
    imbalance = env.get_imbalance()
    return max(0.0, 1.0 - imbalance)
