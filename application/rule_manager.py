from order import Order

class RuleManager:
    def __init__(self, rules):
        self.rules = rules

    def apply_rules(self, order : Order):
        changed_order = None
        for rule in self.rules:
            changed_order = rule.apply_rule(order)

        return changed_order