"""
Generates eval/tasks_smoke200.jsonl — a 200+ task, GOLD-LABELED benchmark set
for the FrugalRoute README table. Same schema as eval/tasks.jsonl (task,
category, difficulty, gold) so it runs through the existing, already-proven
run.py -> score.py pipeline unchanged.

math/classification/extraction gold values are COMPUTED here in code (not
hand-typed), so there is zero risk of an arithmetic or extraction-answer
mistake in the ground truth itself. qa/reasoning are hand authored (need
real-world factual/logical correctness that can't be derived mechanically)
and hand-verified.
"""
import json
import random
from collections import Counter

random.seed(42)
tasks = []


def add(task, category, difficulty, gold):
    tasks.append({"task": task, "category": category, "difficulty": difficulty, "gold": str(gold)})


# ---- MATH — computed gold, no manual arithmetic risk ----
for _ in range(35):
    a, b = random.randint(10, 999), random.randint(10, 999)
    op = random.choice(["+", "-", "*"])
    if op == "+":
        add(f"What is {a} + {b}?", "math", "easy", a + b)
    elif op == "-":
        if a < b:
            a, b = b, a
        add(f"What is {a} - {b}?", "math", "easy", a - b)
    else:
        a, b = random.randint(2, 30), random.randint(2, 30)
        add(f"What is {a} * {b}?", "math", "easy", a * b)

for _ in range(35):
    kind = random.choice(["percent", "avg", "compound", "rate", "power"])
    if kind == "percent":
        base = random.choice([200, 240, 320, 400, 500, 600, 800])
        pct = random.choice([5, 10, 15, 20, 25])
        add(f"What is {pct}% of {base}?", "math", "med", base * pct / 100)
    elif kind == "avg":
        nums = [random.randint(1, 50) for _ in range(4)]
        add(f"What is the average of {', '.join(map(str, nums))}?", "math", "med",
            round(sum(nums) / len(nums), 2))
    elif kind == "compound":
        principal = random.choice([1000, 2000, 5000])
        rate = random.choice([4, 5, 6])
        years = 2
        val = round(principal * ((1 + rate / 100) ** years - 1), 2)
        add(f"Compute the compound interest on {principal} at {rate}% for {years} years.", "math", "hard", val)
    elif kind == "rate":
        km = random.choice([60, 90, 120, 150])
        mins = random.choice([30, 45, 60])
        add(f"A train travels {km} km in {mins} minutes; how many km/h is that?", "math", "hard",
            round(km / (mins / 60), 1))
    else:
        base = random.choice([2, 3])
        exp = random.choice([6, 7, 8, 9])
        add(f"What is {base} to the power of {exp}?", "math", "hard", base ** exp)

# ---- CLASSIFICATION — templated, gold known from the template choice ----
sentiments = [
    ("I absolutely love this, best purchase all year!", "positive"),
    ("This completely ruined my week, total disaster.", "negative"),
    ("It arrived on Tuesday as scheduled.", "neutral"),
    ("Incredible service, will definitely buy again!", "positive"),
    ("Awful experience, I want my money back.", "negative"),
    ("The box was medium sized and grey.", "neutral"),
    ("Best decision I've made this year, thank you!", "positive"),
    ("Never buying from this company again, terrible.", "negative"),
    ("The item weighs about two kilograms.", "neutral"),
    ("Exceeded every expectation, absolutely fantastic!", "positive"),
    ("Broken on arrival, extremely disappointed.", "negative"),
    ("The manual has twelve pages.", "neutral"),
    ("Couldn't be happier with the results!", "positive"),
    ("Waste of money, do not recommend.", "negative"),
    ("The store opens at nine in the morning.", "neutral"),
    ("Five stars, exactly what I needed!", "positive"),
    ("Completely unusable, returning immediately.", "negative"),
    ("Delivery takes three to five business days.", "neutral"),
    ("Outstanding quality, thrilled with this!", "positive"),
    ("Regret this purchase entirely, poor quality.", "negative"),
]
for text, gold in sentiments:
    add(f"Classify the sentiment: '{text}'", "classification", "easy" if gold != "neutral" else "med", gold)

spam_examples = [
    ("CONGRATULATIONS!! You've WON a free iPhone, click now!!!", "spam"),
    ("Hi, attaching the Q2 budget spreadsheet for your review.", "not spam"),
    ("URGENT: verify your account now or it will be suspended!!!", "spam"),
    ("Reminder: our meeting is rescheduled to 3pm tomorrow.", "not spam"),
    ("You have been selected for a cash prize, act now!", "spam"),
]
for text, gold in spam_examples:
    add(f"Is this email spam? '{text}'", "classification", "easy", gold)

topics = [
    ("The central bank raised interest rates by half a point.", "economics"),
    ("The striker scored twice in the final ten minutes.", "sports"),
    ("Astronomers detected a new exoplanet in a nearby star system.", "science"),
    ("The senate passed the new infrastructure bill today.", "politics"),
    ("The new smartphone features a faster processor and better camera.", "technology"),
]
for text, gold in topics:
    add(f"Classify the topic of: '{text}'", "classification", "med", gold)

# ---- EXTRACTION — synthetic sentences with a known embedded answer ----
domains = ["example.com", "company.org", "mail.net", "corp.io"]
for i in range(40):
    kind = random.choice(["email", "phone", "total", "count"])
    if kind == "email":
        name = random.choice(["john", "alice", "bob", "priya", "diego"])
        dom = random.choice(domains)
        email = f"{name}@{dom}"
        add(f"Extract the email address from: 'Please contact {email} for details.'",
            "extraction", "easy", email)
    elif kind == "phone":
        num = f"555-{random.randint(1000, 9999)}"
        add(f"Extract the phone number from: 'Call me at {num} anytime.'", "extraction", "easy", num)
    elif kind == "total":
        n_items = random.randint(2, 5)
        price = random.choice([4, 5, 6, 8, 10])
        shipping = random.choice([2, 3, 5])
        total = n_items * price + shipping
        add(f"Extract the total price from: '{n_items} items at ${price} each plus ${shipping} shipping.'",
            "extraction", "med", total)
    else:
        a, b = random.randint(10, 90), random.randint(10, 90)
        total = a + b
        add(f"Extract the combined total from: 'Team A shipped {a} units and Team B shipped {b} units.'",
            "extraction", "med", total)

# ---- QA — stable, hand-verified factual answers only (no volatile prices/news) ----
qa_pairs = [
    ("What is the capital of France?", "Paris"),
    ("What is the capital of Japan?", "Tokyo"),
    ("What is the capital of Australia?", "Canberra"),
    ("What is the chemical symbol for gold?", "Au"),
    ("What is the chemical symbol for iron?", "Fe"),
    ("How many continents are there?", "7"),
    ("Who wrote Romeo and Juliet?", "Shakespeare"),
    ("Who wrote Hamlet?", "Shakespeare"),
    ("What year did the Berlin Wall fall?", "1989"),
    ("What year did World War II end?", "1945"),
    ("What is the boiling point of water at sea level in Celsius?", "100"),
    ("What is the freezing point of water in Celsius?", "0"),
    ("What is the largest planet in our solar system?", "Jupiter"),
    ("What is the smallest planet in our solar system?", "Mercury"),
    ("Who painted the Mona Lisa?", "Leonardo da Vinci"),
    ("Who developed the theory of general relativity?", "Einstein"),
    ("What is the tallest mountain in the world?", "Everest"),
    ("What is the longest river in the world?", "Nile"),
    ("What is the hardest natural substance on Earth?", "diamond"),
    ("What gas do plants absorb during photosynthesis?", "carbon dioxide"),
    ("What is the SI unit of electric current?", "ampere"),
    ("What is the main function of red blood cells?", "carry oxygen"),
    ("What is the currency of Japan?", "yen"),
    ("What is the currency of the United Kingdom?", "pound"),
    ("Who was the first President of the United States?", "Washington"),
    ("What is the square root of 144?", "12"),
    ("What is the atomic number of hydrogen?", "1"),
    ("What is the national language of Brazil?", "Portuguese"),
    ("What is the largest ocean on Earth?", "Pacific"),
    ("What does CPU stand for?", "central processing unit"),
    ("What is the speed of light in km per second, roughly?", "300000"),
    ("What planet is known as the Red Planet?", "Mars"),
    ("What is the capital of Germany?", "Berlin"),
    ("What is the capital of Canada?", "Ottawa"),
    ("Who is credited with inventing the telephone?", "Alexander Graham Bell"),
    ("What is the powerhouse of the cell called?", "mitochondria"),
    ("What is the chemical formula for water?", "H2O"),
    ("What is the capital of Italy?", "Rome"),
    ("How many sides does a hexagon have?", "6"),
    ("What is the currency of the United States?", "dollar"),
]
for q, g in qa_pairs:
    add(q, "qa", "easy", g)

# ---- REASONING — logic puzzles with a single crisp, deterministic answer ----
reasoning = [
    ("Deduce who is oldest: Ann is older than Bob, Bob is older than Cy.", "med", "Ann"),
    ("Deduce who is youngest: Ann is older than Bob, Bob is older than Cy.", "med", "Cy"),
    ("If all A are B and all B are C, are all A C?", "med", "yes"),
    ("If no cats are dogs, and all poodles are dogs, can a poodle be a cat?", "med", "no"),
    ("A farmer has 17 sheep, all but 9 die. How many are left?", "med", "9"),
    ("If a bat and a ball cost $1.10 together, and the bat costs $1.00 more than the ball, how much does the ball cost?", "hard", "0.05"),
    ("What is the next number in the sequence 2, 6, 12, 20, 30?", "med", "42"),
    ("What is the next number in the sequence 1, 1, 2, 3, 5, 8?", "med", "13"),
    ("If today is Wednesday, what day of the week is it in 8 days?", "med", "Thursday"),
    ("If today is Monday, what day of the week is it in 10 days?", "med", "Thursday"),
    ("Three friends split a bill of $90 equally. How much does each person pay?", "easy", "30"),
    ("If all the mangoes in a basket are ripe except two, and there are 12 mangoes, how many are unripe?", "med", "2"),
    ("Maria arrives before Tom, and Tom arrives before Sam. Who arrives last?", "easy", "Sam"),
    ("Maria arrives before Tom, and Tom arrives before Sam. Who arrives first?", "easy", "Maria"),
    ("A clock shows 3:00. How many degrees are between the hour and minute hands?", "hard", "90"),
    ("If a train travels 120 miles in 2 hours, then 180 miles in the next 3 hours, what is its average speed for the whole trip in mph?", "hard", "60"),
    ("How many multiply steps to compute 2^10 by squaring?", "hard", "4"),
    ("If it takes 5 machines 5 minutes to make 5 widgets, how long would 100 machines take to make 100 widgets?", "hard", "5"),
    ("A is taller than B. B is taller than C. Who is shortest?", "easy", "C"),
    ("A is taller than B. B is taller than C. Who is tallest?", "easy", "A"),
    ("If today is Friday, what day of the week is it in 3 days?", "easy", "Monday"),
    ("If today is Sunday, what day of the week is it in 14 days?", "easy", "Sunday"),
    ("What is the next number in the sequence 3, 6, 9, 12, 15?", "easy", "18"),
    ("What is the next number in the sequence 1, 2, 4, 8, 16?", "easy", "32"),
    ("Five friends split a bill of $100 equally. How much does each person pay?", "easy", "20"),
    ("If a train travels 100 miles in 2 hours, what is its average speed in mph?", "easy", "50"),
    ("A is older than B. C is older than A. Who is oldest?", "easy", "C"),
    ("A is older than B. C is older than A. Who is youngest?", "easy", "B"),
    ("If it takes 2 workers 4 hours to paint a fence, how many hours would 1 worker take alone?", "med", "8"),
    ("What is the missing number in the sequence 5, 10, ?, 20, 25?", "easy", "15"),
]
for t, d, g in reasoning:
    add(t, "reasoning", d, g)

print(f"Total tasks: {len(tasks)}")
assert len(tasks) >= 200, f"need >=200, got {len(tasks)}"

with open("tasks_smoke200.jsonl", "w") as f:
    for t in tasks:
        f.write(json.dumps(t) + "\n")

print(Counter(t["category"] for t in tasks))
