class FileHandler:
    def __init__(self, input_file='input.txt', output_file='output.txt', portion=10):
        self.input_file = input_file
        self.output_file = output_file
        self.portion = portion
        self.cursor_position = 0
        self.has_file_ended = False

    def read_by_portion(self):
        try:
            with open(self.input_file, 'r') as file:
                return self._process_reading(file)
        except FileNotFoundError:
            return f"Error: The file '{self.input_file}' does not exist."
        except Exception as e:
            return f"An unexpected error occurred: {e}"

    def write_to_file(self, result: str):
        try:
            with open(self.output_file, 'a') as file:
                file.write(f'{result}\n')
        except Exception as e:
            return f"Error writing to file: {e}"

    def clear_output(self):
        try:
            with open(self.output_file, 'w') as file:
                pass
        except Exception as e:
            return f"Error clearing file: {e}"

    def _check_end(self, lines):
        return len(lines) < self.portion

    def _read(self, file):
        lines = []
        for _ in range(self.portion):
            line = file.readline()
            if not line:
                break
            lines.append(line.strip())
        return lines

    def _process_reading(self, file):
        file.seek(self.cursor_position)
        lines = self._read(file)

        self.has_ended = self._check_end(lines)
        self.cursor_position = file.tell()

        return lines
