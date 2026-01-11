class Option:
    def __init__(self, name, pros, cons, importance, risk):
        self.name = name
        self.pros = pros
        self.cons = cons
        self.importance = importance      # 1–10
        self.risk = risk                  # 1–10

    def pros_score(self):
        return len(self.pros) * 2

    def cons_penalty(self):
        return len(self.cons) * 1.5

    def importance_weight(self):
        return self.importance * 2

    def risk_penalty(self):
        return self.risk * 2

    def raw_score(self):
        score = (
            self.pros_score()
            + self.importance_weight()
            - self.cons_penalty()
            - self.risk_penalty()
        )
        return score

    def normalized_score(self):
        raw = self.raw_score()
        normalized = max(min(raw * 5, 100), 0)
        return round(normalized, 2)

    def explanation(self):
        return (
            f"{self.name} has {len(self.pros)} pros and {len(self.cons)} cons. "
            f"Importance is {self.importance}/10 and risk is {self.risk}/10."
        )


class DecisionEngine:
    def __init__(self):
        self.options = []

    def add_option(self, option):
        self.options.append(option)

    def has_enough_options(self):
        return len(self.options) >= 2

    def rank_options(self):
        ranked = sorted(
            self.options,
            key=lambda opt: opt.normalized_score(),
            reverse=True
        )
        return ranked

    def best_option(self):
        ranked = self.rank_options()
        return ranked[0]

    def display_results(self):
        print("\n📊 Decision Analysis Result\n")
        ranked = self.rank_options()

        for idx, option in enumerate(ranked, start=1):
            print(f"{idx}. {option.name}")
            print(f"   Score: {option.normalized_score()}/100")
            print(f"   Reason: {option.explanation()}\n")

        best = self.best_option()
        print(" Recommended Decision:")
        print(f"👉 {best.name} (Best overall balance of benefit and risk)")


class InputHandler:
    @staticmethod
    def get_list(prompt):
        items = input(prompt).split(",")
        return [item.strip() for item in items if item.strip()]

    @staticmethod
    def get_number(prompt, min_val=1, max_val=10):
        while True:
            try:
                value = int(input(prompt))
                if min_val <= value <= max_val:
                    return value
                print(f"Enter a number between {min_val} and {max_val}.")
            except ValueError:
                print("Invalid input. Enter a number.")


def run_decision_craft():
    engine = DecisionEngine()
    print("🧠 Welcome to DecisionCraft – Personal Decision Scoring Engine\n")

    while True:
        name = input("Option name: ")
        pros = InputHandler.get_list("Pros (comma separated): ")
        cons = InputHandler.get_list("Cons (comma separated): ")
        importance = InputHandler.get_number("Importance (1–10): ")
        risk = InputHandler.get_number("Risk (1–10): ")

        option = Option(name, pros, cons, importance, risk)
        engine.add_option(option)

        cont = input("\nAdd another option? (y/n): ").lower()
        if cont != "y":
            break

    if engine.has_enough_options():
        engine.display_results()
    else:
        print("\n⚠️ Add at least two options to make a comparison.")


if __name__ == "__main__":
    run_decision_craft()

