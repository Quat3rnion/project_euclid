import math
from fractions import Fraction

from rich.console import Console
from rich.table import Table


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def distance_from_point(self, p1) -> float:
        return math.sqrt((self.x - p1.x) ** 2 + (self.y - p1.y) ** 2)

    def distance_from_line(self, line) -> float:
        return abs(line.A * self.x + line.B * self.y + line.C) / math.sqrt(line.A ** 2 + line.B ** 2)

    def is_on_line(self, line) -> bool:
        return self.distance_from_line(line) == 0

    # TODO: ratio using section formula

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


def integerize_coefficients(a: float, b: float, c: float) -> tuple:
    a = Fraction(a).limit_denominator()
    b = Fraction(b).limit_denominator()
    c = Fraction(c).limit_denominator()
    lcm = math.lcm(a.denominator, b.denominator, c.denominator)
    a = a.numerator * (lcm // a.denominator)
    b = b.numerator * (lcm // b.denominator)
    c = c.numerator * (lcm // c.denominator)
    return a, b, c


class Line:
    def __init__(self, a: float, b: float, c: float):
        # a, b, and c are the coefficients of the line
        (a, b, c) = integerize_coefficients(a, b, c)
        self.A = a
        self.B = b
        self.C = c
        # x, and y intercepts
        self.x_int = -self.C / self.A
        self.y_int = -self.C / self.B
        # slope
        self.m = -self.A / self.B

    @classmethod
    def from_slope(cls, m: float, p1) -> "Line":
        A = m
        B = -1
        C = p1.y - m * p1.x
        return Line(A, B, C)

    @classmethod
    def from_points(cls, p1, p2) -> "Line":
        # p1 and p2 are points on the line
        m = (p2.y - p1.y) / (p2.x - p1.x)
        return Line.from_slope(m, p1)

    @classmethod
    def from_y_intercept(cls, y_int: float, m: float) -> "Line":
        A = m
        B = -1
        C = y_int
        return Line(A, B, C)

    @classmethod
    def from_x_intercept(cls, x_int: float, m: float) -> "Line":
        A = m
        B = -1
        C = -m * x_int
        return Line(A, B, C)

    @classmethod
    def from_intercepts(cls, x_int: float, y_int: float) -> "Line":
        A = y_int
        B = x_int
        C = -x_int * y_int
        return Line(A, B, C)

    @classmethod
    def from_equation(cls, eqn: str) -> "Line":
        # eqn is a string of the form ax + by + c = 0
        eqn = eqn.replace(" ", "")
        # now it is ax+by+c=0
        eqn = eqn.split("=")[0]
        a = float(eqn.split("x")[0] or "1")
        try:
            b = float(eqn.split("x")[1].split("y")[0])
        except ValueError:
            b = 1
        try:
            c = float(eqn.split("x")[1].split("y")[1])
        except ValueError:
            c = 0
        return Line(a, b, c)

    def perpendicular(self, p1: Point) -> "Line":
        m = -1 / self.m
        line = Line.from_slope(m, p1)
        return line

    def angle(self, line) -> float:
        if self.m == line.m:
            return 0
        elif self.m == 0 and line.m == math.inf:
            return 90
        elif self.m == math.inf and line.m == 0:
            return 90
        return math.degrees(math.atan((self.m - line.m) / (1 + self.m * line.m)))

    def distance_from_point(self, p1) -> float:
        return abs(self.A * p1.x + self.B * p1.y + self.C) / math.sqrt(self.A ** 2 + self.B ** 2)

    def distance_from_line(self, line) -> float:
        return abs(self.C - line.C) / math.sqrt(self.A ** 2 + self.B ** 2)

    def __str__(self):
        # string of form ax + by = c
        return f"{self.A}x + {self.B}y + {self.C} = 0".replace("+ -", "- ")

    def __repr__(self):
        return f"Line({self.A}, {self.B}, {self.C})"


# format string to replace "+ -" with " - "
def format_eqn(eqn: str):
    eqn = eqn.replace("+ -", "-")
    return eqn


lines = {}
points = {}

lines_table = Table(title="Lines")
lines_table.add_column("Name", justify="center", style="cyan")
lines_table.add_column("Equation", justify="center", style="magenta")

points_table = Table(title="Points")
points_table.add_column("Name", justify="center", style="cyan")
points_table.add_column("Coordinates", justify="center", style="magenta")

console = Console()


def add_line(name: str, line: str) -> str:
    if line[0] == ".":
        line = eval("Line" + line)
    else:
        line = Line.from_equation(line)
    lines[name] = line
    lines_table.add_row(name, format_eqn(str(line)))
    return "Ok!"


def add_point(name: str, p: str) -> str:
    p_tuple = eval(p)
    point = Point(p_tuple[0], p_tuple[1])
    points[name] = point
    points_table.add_row(name, str(point))
    return "Ok!"


def show() -> None:
    console.print(lines_table)
    console.print(points_table)


def show_lines() -> None:
    console.print(lines_table)


def show_points() -> None:
    console.print(points_table)


def distance(arg1: Point or Line, arg2: Point or Line) -> float:
    if isinstance(arg1, Point) and isinstance(arg2, Point):
        return arg1.distance_from_point(arg2)
    elif isinstance(arg1, Point) and isinstance(arg2, Line):
        return arg2.distance_from_point(arg1)
    elif isinstance(arg1, Line) and isinstance(arg2, Point):
        return arg1.distance_from_point(arg2)
    elif isinstance(arg1, Line) and isinstance(arg2, Line):
        return arg1.distance_from_line(arg2)


def angle(line1: Line, line2: Line) -> float:
    return line1.angle(line2)


def perpendicular(line: Line, point: Point) -> Line:
    return line.perpendicular(point)


def slope(line: Line) -> float:
    return line.m


def clear() -> None:
    lines.clear()
    points.clear()
    console.print("Cleared all lines and points.")


commands = {
    "line": add_line,
    "point": add_point,
    "lines": show_lines,
    "points": show_points,
    "show": show,
    "slope": slope,
    "distance": distance,
    "angle": angle,
    "perpendicular-on": perpendicular,
    "clear": clear,
    "exit": exit,
}

separators = {
    "line": "is",
    "point": "is",
    "distance": "and",
    "angle": "and",
    "perpendicular-on": "through",
    "slope": "is",
}


def run_command(cmd: str) -> str:
    globals().update(lines)
    globals().update(points)
    base = cmd.split(" ")[0]
    command = commands.get(base)
    args = cmd.split(" ")[1:]
    if base in separators:
        if args[0] == "between":
            args = args[1:]
        sep = separators[base]
        args = " ".join(args).split(sep)
        args = [arg.strip() for arg in args]
        for i in args:
            if i in points:
                args[args.index(i)] = points[i]
            elif i in lines:
                args[args.index(i)] = lines[i]
    if base == "whats":
        return eval(" ".join(args))
    if command is None:
        raise ValueError(f"Command {base} not found.")
    return command(*args)


def repl() -> None:
    try:
        while True:
            try:
                _in = input("> ")
                try:
                    out = run_command(_in)
                    if out != "Ok!" and out is not None:
                        print("It's ", out)
                    else:
                        print(out or " ")
                except SyntaxError:
                    out = exec(_in)
                    if out is not None:
                        print(out)
            except Exception as e:
                print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nExiting...")


if __name__ == "__main__":
    repl()
