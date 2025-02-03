from datetime import datetime

class DataValidator:
    def __init__(self):
        self.is_valid = True

    def process_validation(self, line, providers):
        if (
            self._is_valid_format(line)
            and self._is_valid_date(line)
            and self._is_valid_size(line, providers)
            and self._is_valid_provider(line, providers)
        ):
            return line
        return f"{line} Ignored"

    def _is_valid_format(self, line):
        self.is_valid = len(line.split()) == 3
        return self.is_valid

    def _is_valid_date(self, line):
        if not self.is_valid:
            return False

        try:
            datetime.strptime(line.split()[0], "%Y-%m-%d")
            return True
        except ValueError:
            self.is_valid = False
            return False

    def _is_valid_size(self, line, providers):
        if not self.is_valid:
            return False

        order_size = line.split()[1]
        provider_name = line.split()[2]

        for provider in providers:
            if provider.name == provider_name and order_size in provider.sizes:
                return True

        self.is_valid = False
        return False

    def _is_valid_provider(self, line, providers):
        if not self.is_valid:
            return False

        provider_name = line.split()[2]
        provider_names = {provider.name for provider in providers}

        if provider_name in provider_names:
            return True

        self.is_valid = False
        return False
