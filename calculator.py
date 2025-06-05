# calculator.py

from typing import Dict, Tuple

class Calculator:
    marks: Dict[str, Tuple[int, int]]
    current_wam: float | None
    current_uoc: int | None

    def __init__(self) -> None:
        self.marks = {}
        self.current_wam = None
        self.current_uoc = None

    def add_mark(self, course: str, mark: int, credit: int) -> bool:
        if course in self.marks:
            return False
        self.marks[course] = (mark, credit)
        return True

    def remove_mark(self, course: str) -> bool:
        if course not in self.marks:
            return False
        del self.marks[course]
        return True

    def print_marks(self) -> None:
        if not self.marks:
            print("No marks entered")
            return
        print("Mark Summary:")
        for i, (course, (mark, credit)) in enumerate(self.marks.items(), start=1):
            print(f"{i}) Course code: {course} Mark: {mark}, Credits: {credit}")

    def calculate_wam(self) -> float:
        total_mark = 0
        total_credit = 0
        for mark, credit in self.marks.values():
            total_mark += mark * credit
            total_credit += credit
        return total_mark / total_credit if total_credit > 0 else 0.0

    def predict_marks(self, course: str, mark: int, credit: int) -> float | None:
        add = self.add_mark(course, mark, credit)
        if not add:
            return None
        predicted = self.calculate_wam()
        self.remove_mark(course)
        return predicted

    def set_current_overall(self, wam: float, uoc: int) -> None:
        self.current_wam = wam
        self.current_uoc = uoc

    def predict_from_current(self, mark: int, credit: int) -> float | None:
        if self.current_wam is None or self.current_uoc is None:
            return None
        total_mark = self.current_wam * self.current_uoc + mark * credit
        total_credit = self.current_uoc + credit
        return total_mark / total_credit if total_credit > 0 else 0.0

def parse_int(value: str, name: str) -> int | None:
    try:
        return int(value)
    except ValueError:
        return None