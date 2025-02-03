import unittest
import  os
import  sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../application')))
from unittest.mock import MagicMock
from rule_manager import RuleManager
from order import Order

class TestRuleManager(unittest.TestCase):
    def setUp(self):
        self.mock_rule1 = MagicMock()
        self.mock_rule2 = MagicMock()
        self.rules = [self.mock_rule1, self.mock_rule2]
        self.rule_manager = RuleManager(self.rules)
        self.order = Order("2025-02-01", "S", "MR")

    def test_apply_rules_calls_all_rules(self):
        self.mock_rule1.apply_rule.return_value = self.order
        self.mock_rule2.apply_rule.return_value = self.order

        result = self.rule_manager.apply_rules(self.order)

        self.mock_rule1.apply_rule.assert_called_once_with(self.order)
        self.mock_rule2.apply_rule.assert_called_once_with(self.order)
        self.assertEqual(result, self.order)

    def test_apply_rules_returns_last_rule_output(self):
        changed_order = Order("2025-02-01", "L", "LP")
        self.mock_rule1.apply_rule.return_value = self.order
        self.mock_rule2.apply_rule.return_value = changed_order

        result = self.rule_manager.apply_rules(self.order)

        self.assertEqual(result, changed_order)

    def tearDown(self):
        del self.rule_manager
        del self.order

if __name__ == '__main__':
    unittest.main()
