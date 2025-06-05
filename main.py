class Calculator:
    def __init__(self):
        self.marks = {}

    def add_mark(self, course: int, mark: int, credit: int) -> bool:
        if self.marks.get(course):
            return False
        self.marks[course] = (int(mark), int(credit))
        return True

    def remove_mark(self, course: str) -> bool:
        if course not in self.marks:
            return False
        del self.marks[course]
        return True

    def print_marks(self) -> None:
        if len(self.marks) == 0:
            print("No marks entered")
            return
        print("Mark Summary:")
        i = 0
        for entry in self.marks:
            i += 1
            print(f"{i}) Course code: {entry} Mark: {self.marks[entry][0]}, Credits: {self.marks[entry][1]}")

    def calculate_wam(self) -> float:
        """
        - Input: List of tuples containing (mark, credits)
        - Output: Weighted Average Mark (WAM)
        """
        total_mark = 0
        total_credit = 0
        for entry in self.marks:
            total_mark += self.marks[entry][0] * self.marks[entry][1]
            total_credit += self.marks[entry][1]
        return total_mark / total_credit

    def predict_marks(self, course: int, mark: int, credit: int) -> bool:
        add = self.add_mark(course, mark, credit)
        if add == False:
            print("Error: mark already entered for course: {course}")
            return False
        print(f"Predicted: {self.calculate_wam()}")
        rem = self.remove_mark(course)
        return True




if __name__ == "__main__":
    calculator = Calculator()
    while True:
        user_input = input("Enter something (or 'exit' to quit): ")
        split = user_input.split(" ")
        if split[0] == 'exit':
            break
        elif split[0] == 'add':
            res = calculator.add_mark(split[1], split[2], split[3])
            if res == False:
                print("!! Error adding mark")
            else:
                print(f"Added mark for course {split[1]}")
        elif split[0] == 'print':
            calculator.print_marks()
        elif split[0] == 'calculate':
            print(calculator.calculate_wam())
        elif split[0] == 'remove':
            res = calculator.remove_mark(split[1])
            if res == False:
                print("!! Error removing mark")
            else:
                print(f"Removed mark for course {split[1]}")
        elif split[0] == 'predict':
            calculator.predict_marks(split[1], split[2], split[3])
    # calculator.add_mark("COMP1511", 75, 6)
    # calculator.print_marks()
    # print(calculator.calculate_wam())
    # calculator.predict_marks("COMP2511", 85, 6)
    # calculator.add_mark("COMP2521", 67, 6)
    # calculator.print_marks()
    # calculator.remove_mark("COMP1511")
    # calculator.print_marks()


