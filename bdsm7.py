class DFA:
    def __init__(self, states, alphabet, start_state, accept_states, transitions):
        self.states = states
        self.alphabet = alphabet
        self.start_state = start_state
        self.accept_states = accept_states
        self.transitions = transitions

    def remove_unreachable_states(self):
        reachable = set()
        stack = [self.start_state]

        while stack:
            current = stack.pop()
            if current not in reachable:
                reachable.add(current)
                for symbol in self.alphabet:
                    next_state = self.transitions.get((current, symbol))
                    if next_state and next_state not in reachable:
                        stack.append(next_state)

        self.states = [state for state in self.states if state in reachable]
        self.transitions = {
            (state, symbol): target
            for (state, symbol), target in self.transitions.items()
            if state in reachable
        }

    def minimize(self):
        non_accept_states = [s for s in self.states if s not in self.accept_states]
        partitions = [set(non_accept_states), set(self.accept_states)]

        while True:
            new_partitions = []
            for group in partitions:
                splits = {}
                for state in group:
                    signature = tuple(
                        next((i for i, g in enumerate(partitions) if self.transitions.get((state, a)) in g), None)
                        for a in self.alphabet
                    )
                    if signature not in splits:
                        splits[signature] = set()
                    splits[signature].add(state)
                new_partitions.extend(splits.values())

            if len(new_partitions) == len(partitions):
                break
            partitions = new_partitions

        state_map = {}
        for i, group in enumerate(partitions):
            group_name = chr(65 + i)  # Assign letters A, B, C, etc.
            for state in group:
                state_map[state] = group_name

        self.states = list(state_map.values())
        self.accept_states = [state_map[s] for s in self.accept_states if s in state_map]
        self.start_state = state_map[self.start_state]
        self.transitions = {
            (state_map[s], a): state_map[t]
            for (s, a), t in self.transitions.items()
            if s in state_map and t in state_map
        }

# Example usage
if __name__ == "__main__":
    # Collect user input
    num_states = int(input("Enter the number of states (max 10): "))
    states = [f"q{i}" for i in range(num_states)]

    alphabet = ['a', 'b']
    start_state = "q0"

    accept_states = input("Enter accept states (comma-separated, e.g., q1,q2): ").split(',')

    print("Define transitions as '(current_state, input_symbol) -> next_state'")
    transitions = {}
    for state in states:
        for symbol in alphabet:
            target = input(f"Transition ({state}, {symbol}) -> ")
            transitions[(state, symbol)] = target

    # Create and minimize DFA
    dfa = DFA(states, alphabet, start_state, accept_states, transitions)

    print("\nOriginal DFA:")
    print(f"States: {dfa.states}")
    print(f"Start State: {dfa.start_state}")
    print(f"Accept States: {dfa.accept_states}")
    print(f"Transitions: {dfa.transitions}")

    dfa.remove_unreachable_states()
    dfa.minimize()

    print("\nMinimized DFA:")
    print(f"States: {dfa.states}")
    print(f"Start State: {dfa.start_state}")
    print(f"Accept States: {dfa.accept_states}")
    print(f"Transitions: {dfa.transitions}")
