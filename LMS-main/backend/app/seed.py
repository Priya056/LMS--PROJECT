from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Course, Problem


def seed_if_empty() -> None:
    db = SessionLocal()
    try:
        if db.query(Course).count() > 0:
            return
        _seed(db)
        db.commit()
    finally:
        db.close()


def _seed(db: Session) -> None:
    cs50p = Course(
        id=1,
        slug="cs50p",
        title="CS50 Python",
        description="Harvard CS50’s Introduction to Programming with Python — variables, control flow, data structures, exceptions, libraries, file I/O, OOP, and more.",
    )
    cs50ai = Course(
        id=2,
        slug="cs50ai",
        title="CS50 Artificial Intelligence",
        description="Harvard CS50’s Introduction to Artificial Intelligence with Python — search, knowledge, uncertainty, optimization, learning, neural networks, and language.",
    )
    db.add_all([cs50p, cs50ai])

    problems_data: list[tuple[int, str, str, str, str, str, int]] = [
        (
            1,
            "indoor",
            "Indoor Voice",
            """Implement `indoor.py` that prompts the user for input and then outputs that same input in lowercase. Punctuation and numbers should be preserved.

Sample:
Input: `HELLO`
Output: `hello`""",
            "cs50/problems/2022/python/indoor",
            "Week 1",
            10,
        ),
        (
            1,
            "playback",
            "Playback Speed",
            """Implement `playback.py` that prompts the user for input and then outputs that input, replacing each space with `...`.

Sample:
Input: `This is CS50`
Output: `This...is...CS50`""",
            "cs50/problems/2022/python/playback",
            "Week 1",
            20,
        ),
        (
            1,
            "einstein",
            "Einstein",
            """Implement `einstein.py` that prompts the user for mass (kg) and prints the equivalent energy in Joules using E = mc² (use `300000000` for c).

Sample:
Input: `m: 1`
Output: `E: 90000000000000000`""",
            "cs50/problems/2022/python/einstein",
            "Week 1",
            30,
        ),
        (
            1,
            "nutrition",
            "Nutrition Facts",
            """Implement `nutrition.py` that prompts for an item and prints calories from the USDA CSV (`nutrition_facts.csv`) using a dict keyed by description.""",
            "cs50/problems/2022/python/nutrition",
            "Week 3",
            40,
        ),
        (
            1,
            "shirtificate",
            "CS50 Shirtificate",
            """Implement `shirtificate.py` that prompts for a name and generates `shirtificate.pdf` with fpdf2 using `shirtificate.png`, matching CS50’s specifications.""",
            "cs50/problems/2022/python/shirtificate",
            "Week 8",
            50,
        ),
        (
            2,
            "degrees",
            "Degrees",
            """Implement `degrees.py` that determines the shortest path between two actors in the IMDb dataset using breadth-first search.""",
            "cs50/ai/2020/x/degrees",
            "Search",
            10,
        ),
        (
            2,
            "tictactoe",
            "Tic-Tac-Toe",
            """Implement optimal play for Tic-Tac-Toe using minimax (with alpha-beta pruning where appropriate) in `tictactoe.py`.""",
            "cs50/ai/2020/x/tictactoe",
            "Search",
            20,
        ),
        (
            2,
            "minesweeper",
            "Minesweeper",
            """Implement logical inference in `minesweeper.py` so the AI safely opens or flags cells based on knowledge.""",
            "cs50/ai/2020/x/minesweeper",
            "Knowledge",
            30,
        ),
        (
            2,
            "traffic",
            "Traffic",
            """Train a convolutional neural network on German Traffic Sign Recognition Benchmark images to classify signs.""",
            "cs50/ai/2020/x/traffic",
            "Neural Networks",
            40,
        ),
    ]

    for course_id, slug, title, desc, check50, week, order in problems_data:
        db.add(
            Problem(
                course_id=course_id,
                slug=slug,
                title=title,
                description=desc,
                check50_slug=check50,
                week_label=week,
                sort_order=order,
            )
        )
