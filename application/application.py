from creation_manager import CreationManager
from data_validator import DataValidator
from file_handler import FileHandler
from rule_manager import RuleManager

class Application:
    def __init__(self):
        self.handler = FileHandler()
        self.validator = DataValidator()
        self.creation_manager = CreationManager()
        self.rule_manager = RuleManager(self.creation_manager.create_rules())

    def run(self):
        self.handler.clear_output()
        providers = self.creation_manager.create_providers()

        while not self.handler.has_ended:
            for line in self.handler.read_by_portion():
                processed_line = self.validator.process_validation(line, providers)

                if self.validator.is_valid:
                    order = self.creation_manager.create_order(processed_line)
                    order.price = self._assign_price(order, providers)
                    result = self.rule_manager.apply_rules(order)

                    self._format_result(result)
                    self.handler.write_to_file(result)
                else:
                    self.handler.write_to_file(processed_line)

    def _assign_price(self, order, providers):
        for provider in providers:
            if provider.name == order.provider_name:
                return {
                    'S': provider.s_price,
                    'M': provider.m_price,
                    'L': provider.l_price
                }.get(order.size, None)

        return None

    def _format_result(self, result):
        result.discount = '-' if result.discount == 0 else f'{result.discount:.1f}'
        result.price = f'{result.price:.1f}' if isinstance(result.price, float) else result.price

        return result