class DFA:
    def __init__(self, states, alphabet, start_state, accept_states, transitions):
        self.states = states
        self.alphabet = alphabet
        self.start_state = start_state
        self.accept_states = accept_states
        self.transitions = transitions

    def remove_unreachable_states(self):
        # Ulaşılamayan durumları kaldırmak için kullanılacak
        reachable = set()
        stack = [self.start_state]  # Başlangıç durumundan başla

        while stack:
            current = stack.pop()
            if current not in reachable:
                reachable.add(current)
                # Mevcut durumdan alfabedeki her sembol için ulaşılabilir durumları bul
                for symbol in self.alphabet:
                    next_state = self.transitions.get((current, symbol))
                    if next_state and next_state not in reachable:
                        stack.append(next_state)

        # Ulaşılamayan durumları ve geçişleri kaldır
        self.states = [state for state in self.states if state in reachable]
        self.transitions = {
            (state, symbol): target
            for (state, symbol), target in self.transitions.items()
            if state in reachable
        }

    def minimize(self):
        # Durumları indirgemek için kullanılacak (denk durumları birleştirme)
        non_accept_states = [s for s in self.states if s not in self.accept_states]
        partitions = [set(non_accept_states), set(self.accept_states)]  # Kabul ve diğer durumları ayır

        while True:
            new_partitions = []
            for group in partitions:
                splits = {}
                for state in group:
                    # Her durum için, alfabedeki sembollerle hangi gruba geçiş yaptığını kontrol et
                    signature = tuple(
                        next((i for i, g in enumerate(partitions) if self.transitions.get((state, a)) in g), None)
                        for a in self.alphabet
                    )
                    # Aynı imzaya sahip durumları aynı gruba ekle
                    if signature not in splits:
                        splits[signature] = set()
                    splits[signature].add(state)
                new_partitions.extend(splits.values())

            if len(new_partitions) == len(partitions):
                break  
            partitions = new_partitions

        # Durumları yeniden gruplandır ve kullanıcıya denk durumları göster
        state_map = {}
        for group in partitions:
            representative = next(iter(group))  # Grubun temsilcisi olarak ilk durumu al
            print(f"Denk Durumlar: {group} -> Temsilci Durum: {representative}")  
            for state in group:
                state_map[state] = representative

        self.states = list(set(state_map.values()))
        self.accept_states = list(set(state_map[s] for s in self.accept_states if s in state_map))
        self.start_state = state_map[self.start_state]
        self.transitions = {
            (state_map[s], a): state_map[t]
            for (s, a), t in self.transitions.items()
            if s in state_map and t in state_map
        }


if __name__ == "__main__":
    num_states = int(input("Durum sayısını girin (en fazla 10): "))
    states = [f"q{i}" for i in range(num_states)]  # Durumları q0, q1, ... şeklinde oluştur

    alphabet = ['a', 'b']  
    start_state = "q0"  

    accept_states = input("Kabul durumlarını girin (virgülle ayrılmış, örn: q1,q2): ").split(',')

    print("Geçişleri '(mevcut_durum, giriş_simgesi) -> hedef_durum' formatında tanımlayın")
    transitions = {}
    for state in states:
        for symbol in alphabet:
            target = input(f"Geçiş ({state}, {symbol}) -> ")
            transitions[(state, symbol)] = target

    # DFA oluştur ve indirgeme işlemlerini yap
    dfa = DFA(states, alphabet, start_state, accept_states, transitions)

    print("\nOrijinal DFA:")
    print(f"Durumlar: {dfa.states}")
    print(f"Başlangıç Durumu: {dfa.start_state}")
    print(f"Kabul Durumları: {dfa.accept_states}")
    print(f"Geçişler: {dfa.transitions}")

    dfa.remove_unreachable_states()  # Ulaşılamayan durumları kaldır
    dfa.minimize()  # Durumları indirgeme işlemi

    print("\nİndirgenmiş DFA:")
    print(f"Durumlar: {dfa.states}")
    print(f"Başlangıç Durumu: {dfa.start_state}")
    print(f"Kabul Durumları: {dfa.accept_states}")
    print(f"Geçişler: {dfa.transitions}")
