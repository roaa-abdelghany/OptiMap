from dataclasses import dataclass

@dataclass(frozen=True)
class OptiMapProblem:
    graph: dict
    start: str
    goal: str

    def __post_init__(self):
        if self.start not in self.graph:
            raise ValueError(f"Unknown start location: {self.start}")
        if self.goal not in self.graph:
            raise ValueError(f"Unknown goal location: {self.goal}")

    @property
    def states(self):
        return self.graph.keys()

    def actions(self, state):
        return tuple(self.graph[state].keys())

    def transition(self, state, next_state):
        if next_state not in self.graph[state]:
            raise ValueError(f"No road from {state} to {next_state}")
        return next_state

    def step_cost(self, state, next_state):
        return self.graph[state][next_state]

    def goal_test(self, state):
        return state == self.goal
