import re
from typing import List, Any

from hstest.testing.settings import Settings
from hstest import *


class SortingToolStage1Test(StageTest):

    def generate(self) -> List[TestCase]:
        Settings.allow_out_of_input = True
        return stage1_tests()

    def check(self, reply: str, clue: Any) -> CheckResult:
        return check_for_long(clue, reply)


class SortingToolClue:
    def __init__(self, console_input, reveal_test, args):
        self.console_input = console_input
        self.reveal_test = reveal_test
        self.args = args


def reveal_raw_test(clue, reply):
    return f"Args:\n{' '.join(clue.args)}\nInput:\n{clue.console_input}\nYour output:\n{reply}\n\n"


def create_test(console_input, reveal_test, args=None):
    if args is None:
        args = ['-dataType', 'long']
    return TestCase(args=args, stdin=console_input, attach=SortingToolClue(console_input, reveal_test, args))


def stage1_tests() -> List[TestCase]:
    return [create_test('1 -2   33 4\n42\n1                 1'.strip(), True),
            create_test("1 2 2 3 4 5 5", True),
            create_test("1 1 2 2 3 4 4 4", False)]


def check_for_long(clue, reply):
    reply = reply.strip()
    match = re.search(r"(?P<total_numbers>\d+)\D+(?P<greatest_number>\d+)\D+(?P<greatest_number_count>\d+)", reply)
    if match is None:
        if clue.reveal_test:
            return CheckResult.wrong("Can't parse your output. Please check if your output contains three numbers\n"
                                     + reveal_raw_test(clue, reply))
        else:
            return CheckResult.wrong("Can't parse your output.")
    total_numbers, greatest_number, greatest_number_count = \
        int(match.group('total_numbers')), int(match.group('greatest_number')), int(
            match.group('greatest_number_count'))

    nums = []
    for actual_number in clue.console_input.split():
        nums.append(int(actual_number))

    if len(nums) != total_numbers:
        if clue.reveal_test:
            return CheckResult.wrong(f"Total amount of numbers ({total_numbers}) is incorrect. Expected: {len(nums)}.\n"
                                     + reveal_raw_test(clue, reply))
        else:
            return CheckResult.wrong("Printed total amount of numbers is incorrect for some testcases.")

    if max(nums) != greatest_number:
        if clue.reveal_test:
            return CheckResult.wrong(f"Greatest number ({greatest_number}) is incorrect. Expected: {max(nums)}.\n"
                                     + reveal_raw_test(clue, reply))
        else:
            return CheckResult.wrong("Printed greatest number is incorrect for some testcases.")

    if nums.count(max(nums)) != greatest_number_count:
        if clue.reveal_test:
            return CheckResult.wrong(
                f"Greatest number times ({greatest_number_count}) is incorrect. Expected: {nums.count(max(nums))}.\n"
                + reveal_raw_test(clue, reply))
        else:
            return CheckResult.wrong("Printed greatest number times is incorrect for some testcases.")

    return CheckResult.correct()


if __name__ == '__main__':
    Settings.allow_out_of_input = True
    SortingToolStage1Test().run_tests()