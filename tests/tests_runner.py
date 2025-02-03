import unittest


def run_tests():
    loader = unittest.TestLoader()
    suits = unittest.TestSuite()

    suits.addTest(loader.discover(start_dir='', pattern='test_*.py'))

    runner = unittest.TextTestRunner()
    runner.run(suits)


if __name__ == "__main__":
    run_tests()