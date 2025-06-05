class Calculator:
    marks: dict[str, tuple[int, int]]

    def __init__(self) -> None:
        self.marks = {}

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

    def predict_marks(self, course: str, mark: int, credit: int) -> bool:
        add = self.add_mark(course, mark, credit)
        if not add:
            print(f"Error: mark already entered for course: {course}")
            return False
        print(f"Predicted: {self.calculate_wam():.2f}")
        self.remove_mark(course)
        return True

def parse_int(value: str, name: str) -> int | None:
    try:
        return int(value)
    except ValueError:
        print(f"Invalid {name}: {value}")
        return None

if __name__ == "__main__":
    calculator = Calculator()
    while True:
        user_input = input("Enter something (or 'exit' to quit): ")
        split = user_input.strip().split()
        if not split:
            continue
        match split[0]:
            case "exit":
                break
            case "add":
                if len(split) != 4:
                    print("Usage: add <course> <mark> <credit>")
                    continue
                course = split[1]
                mark = parse_int(split[2], "mark")
                credit = parse_int(split[3], "credit")
                if None in (mark, credit):
                    continue
                res = calculator.add_mark(course, mark, credit)
                if not res:
                    print(f"!! Error adding mark for course {course}")
                else:
                    print(f"Added mark for course {course}")
            case "print":
                calculator.print_marks()
            case "calculate":
                print(calculator.calculate_wam())
            case "remove":
                if len(split) != 2:
                    print("Usage: remove <course>")
                    continue
                course = split[1]
                res = calculator.remove_mark(course)
                if not res:
                    print(f"!! Error removing mark for course {course}")
                else:
                    print(f"Removed mark for course {course}")
            case "predict":
                if len(split) != 4:
                    print("Usage: predict <course> <mark> <credit>")
                    continue
                course = split[1]
                mark = parse_int(split[2], "mark")
                credit = parse_int(split[3], "credit")
                if None in (mark, credit):
                    continue
                calculator.predict_marks(course, mark, credit)
            case _:
                print(f"Unknown command: {split[0]}")