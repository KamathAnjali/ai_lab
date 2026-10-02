# Independent verification additions

The accompanying notebook describes a breadth-first STRIPS planner. These checks
are intended to be added as an independent validation layer:

```python
def replay_plan(initial_state, actions, plan):
    state = set(initial_state)
    for action in plan:
        assert action.applicable(state), f"Invalid action: {action}"
        state = action.apply(state)
    return state


def satisfies_goal(state, goal):
    return set(goal).issubset(state)


plan = breadth_first_search(initial_state, goal, actions)
assert plan is not None
final_state = replay_plan(initial_state, actions, plan)
assert satisfies_goal(final_state, goal)

# A valid planner must reject a plan that only moves the robot.
robot_only = [move_a_b, move_b_c]
robot_state = replay_plan(initial_state, actions, robot_only)
assert not satisfies_goal(robot_state, goal)
```

These assertions verify the actual state transitions rather than relying only on
the displayed plan text.
