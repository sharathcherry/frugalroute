"""
FrugalRoute comprehensive smoke test.

Runs 200+ diverse prompts against the LIVE production pipeline (POST /api/route
on localhost:8000, on the MI300X box itself), spanning every category the
router recognizes (math easy/hard, classification, qa, extraction,
summarization, reasoning, coding, open-ended). Periodically cycles the active
REMOTE model via /api/models/remote/select so multiple of the 12 real
Fireworks models actually get exercised when the confidence gate escalates,
not just whatever the default happens to be.

Logs full per-call detail to smoke_results.jsonl and prints a live progress
line every 10 calls. Designed to run detached (nohup) since 200+ real model
calls will take a while.
"""
import json
import time
import urllib.request
import urllib.error

BASE = "http://127.0.0.1:8000"

REMOTE_MODELS = [
    "accounts/fireworks/models/gpt-oss-120b",
    "accounts/fireworks/models/gpt-oss-20b",
    "accounts/fireworks/models/glm-5p1",
    "accounts/fireworks/models/glm-5p2",
    "accounts/fireworks/models/deepseek-v4-pro",
    "accounts/fireworks/models/deepseek-v4-flash",
    "accounts/fireworks/models/kimi-k2p6",
    "accounts/fireworks/models/kimi-k2p7-code",
    "accounts/fireworks/models/minimax-m2p7",
    "accounts/fireworks/models/minimax-m3",
    "accounts/fireworks/models/qwen3p7-plus",
    "accounts/fireworks/models/nemotron-3-ultra-nvfp4",
]

MATH_EASY = [
    "What is 145 + 278?", "What is 932 - 417?", "What is 23 * 17?",
    "What is 144 / 12?", "What is the square of 13?", "What is 15% of 240?",
    "Round 3.14159 to two decimal places.", "What is 7 factorial?",
    "Convert 5 miles to kilometers.", "What is the average of 4, 8, 15, 16, 23?",
    "What is 2 to the power of 8?", "Simplify the fraction 24/36.",
    "What is the least common multiple of 4 and 6?",
    "What is the greatest common divisor of 18 and 24?",
    "Convert 98.6 Fahrenheit to Celsius.", "What is 1000 divided by 8?",
    "What is 9 squared minus 4 squared?", "How many minutes are in 3.5 hours?",
    "What is 50% of 50% of 400?", "Solve for x: 2x + 5 = 17.",
]

MATH_HARD = [
    "How many multiply steps to compute 2^10 by squaring?",
    "Prove that the square root of 2 is irrational.",
    "Derive the quadratic formula from ax^2 + bx + c = 0 by completing the square.",
    "Explain why the sum of the first n odd numbers equals n squared, with a proof.",
    "Prove by induction that 1 + 2 + ... + n = n(n+1)/2.",
    "How many comparisons does binary search need in the worst case on 1000 sorted items? Explain the derivation.",
    "Prove that there are infinitely many prime numbers.",
    "Explain step by step why 0.999... repeating equals exactly 1.",
    "Derive the formula for the sum of a geometric series step by step.",
    "Prove the Pythagorean theorem using similar triangles.",
    "Explain step by step how the Euclidean algorithm finds the GCD of 1071 and 462.",
    "Derive Bayes' theorem from the definition of conditional probability, step by step.",
    "Prove that the product of any two consecutive integers is even.",
    "Explain, step by step, why matrix multiplication is not commutative in general, with an example.",
    "Derive the derivative of x^n using first principles.",
    "Prove that an angle inscribed in a semicircle is always a right angle.",
    "Explain step by step how RSA encryption uses modular exponentiation.",
    "Derive the formula for compound interest from first principles.",
    "Prove that the sum of the interior angles of any triangle is 180 degrees.",
    "Explain step by step why the halting problem is undecidable, using diagonalization.",
]

CLASSIFICATION = [
    "Classify the sentiment: 'This product completely exceeded my expectations!'",
    "Classify the sentiment: 'Absolutely terrible service, I want a refund.'",
    "Classify the sentiment: 'It was okay, nothing special.'",
    "Is this email spam? 'CONGRATULATIONS!!! You won $1,000,000, click here now!!!'",
    "Is this email spam? 'Hi team, attaching the Q3 report for review before Friday.'",
    "Classify this text by topic: 'The Federal Reserve raised interest rates by 0.25%.'",
    "Classify this text by topic: 'The striker scored a hat-trick in the final minutes.'",
    "Classify this text by topic: 'Researchers discovered a new exoplanet orbiting a red dwarf.'",
    "Classify the sentiment: 'I'm not sure how I feel about this update.'",
    "Classify this review as positive, negative, or neutral: 'Good value but the battery life is disappointing.'",
    "Is this a question or a statement: 'Could you send me the invoice by tomorrow?'",
    "Classify this news headline by topic: 'Central bank signals rate cuts amid slowing inflation.'",
    "Classify the sentiment: 'Worst purchase I have ever made.'",
    "Classify this text: 'Mitochondria are the powerhouse of the cell.' — is this biology, chemistry, or physics?",
    "Classify the intent: 'Can you cancel my subscription?' — is this a complaint, a request, or feedback?",
    "Classify the sentiment of this tweet: 'Just landed and my luggage is already lost. Great start.'",
    "Classify this support ticket priority as low, medium, or high: 'The entire production database is down.'",
    "Classify this support ticket priority: 'Minor typo on the about page.'",
    "Classify the language of this text: 'Bonjour, comment allez-vous aujourd'hui?'",
    "Classify this as fact or opinion: 'Water boils at 100 degrees Celsius at sea level.'",
]

QA = [
    "What is the capital of Australia?", "Who wrote the play Hamlet?",
    "What is the chemical symbol for gold?", "What year did World War II end?",
    "What is the tallest mountain in the world?", "Who painted the Mona Lisa?",
    "What is the largest planet in our solar system?",
    "What is the boiling point of water at sea level in Celsius?",
    "Who was the first President of the United States?",
    "What is the speed of light in a vacuum?",
    "What is the current share price of AMD?",
    "What is the current price of Bitcoin?",
    "What's the weather like in Tokyo right now?",
    "Who is the current CEO of Microsoft?",
    "What is the population of Japan?",
    "What is the currency used in Switzerland?",
    "What is the freezing point of water in Fahrenheit?",
    "How many continents are there on Earth?",
    "What is the longest river in the world?",
    "What is the smallest country in the world by area?",
    "What language has the most native speakers worldwide?",
    "What is the main function of red blood cells?",
    "What gas do plants absorb during photosynthesis?",
    "Who developed the theory of general relativity?",
    "What is the name of the galaxy that contains our solar system?",
    "What is the hardest natural substance on Earth?",
    "What is the national animal of Canada?",
    "What is the SI unit of electric current?",
    "What is the largest ocean on Earth?",
    "What does CPU stand for?",
]

EXTRACTION = [
    "Extract all email addresses from: 'Contact john@example.com or sales@company.org for details.'",
    "Extract all dates from: 'The meeting is on March 3rd, followed by a review on April 12, 2027.'",
    "Extract all names from: 'Alice met Bob and Carol at the conference in Berlin.'",
    "Extract all phone numbers from: 'Call us at (555) 123-4567 or (555) 987-6543.'",
    "List all the fruits mentioned: 'She bought apples, bananas, and a bag of oranges, plus some bread.'",
    "Extract the total amount due from this invoice text: 'Subtotal: $120.00, Tax: $9.60, Total: $129.60.'",
    "Extract all URLs from: 'Visit https://example.com or http://test.org for more info.'",
    "Extract the company names mentioned: 'Google and Microsoft both announced new AI products this week, alongside a smaller startup called Cohere.'",
    "Pull out the numeric quantities from: 'We shipped 42 units on Monday and 108 units on Tuesday.'",
    "Extract the job title and company from: 'Jane Doe, Senior Engineer at Acme Corp, joined in 2021.'",
    "Extract all hashtags from: 'Loving the new update! #tech #innovation #ai'",
    "Extract the location mentioned in: 'The conference will be held in Berlin, Germany next spring.'",
    "Extract all currency amounts from: 'The item costs $49.99 plus a $5.00 shipping fee.'",
    "Extract the main verb in this sentence: 'The cat quickly jumped over the fence.'",
    "List the ingredients mentioned: 'Mix flour, sugar, eggs, and a pinch of salt.'",
    "Extract the deadline mentioned: 'Please submit your report by end of day Friday, June 5th.'",
    "Extract all product names from: 'We compared the iPhone 15, Galaxy S24, and Pixel 8 side by side.'",
    "Extract the sender and recipient from: 'From: alice@corp.com To: bob@corp.com Subject: Meeting notes'",
    "Extract percentages mentioned in: 'Revenue grew 12% while costs increased by only 3%.'",
    "Extract all country names from: 'The trip covered France, Italy, and Spain over two weeks.'",
]

SUMMARIZATION = [
    "Summarize in one sentence: 'The company reported record quarterly revenue driven by strong cloud services growth, though profit margins narrowed due to increased infrastructure spending and rising competition in the AI sector.'",
    "Summarize in one sentence: 'Scientists have discovered a new species of frog in the Amazon rainforest that can change the texture of its skin, a trait never before observed in amphibians, potentially aiding future biomimetic material research.'",
    "Summarize this in two sentences: 'The city council voted to approve a new public transit expansion plan that will add 15 miles of light rail track over the next five years, funded partly by a new local sales tax and partly by federal infrastructure grants.'",
    "Summarize: 'After months of negotiation, the two companies finalized a merger agreement valued at $4.2 billion, combining their cloud computing divisions to better compete against larger industry players.'",
    "Give a one-line summary: 'Researchers found that a Mediterranean diet rich in olive oil, vegetables, and fish was associated with a 20% reduction in cardiovascular disease risk over a ten-year study period.'",
    "Summarize this paragraph: 'The novel follows a young detective in 1920s Paris who uncovers a conspiracy involving forged art while grappling with her own troubled past and a rival investigator who may not be who he claims to be.'",
    "Summarize in one sentence: 'The startup raised $50 million in Series B funding to expand its AI-powered logistics platform into new markets across Southeast Asia.'",
    "Summarize: 'Heavy rainfall over the past week caused widespread flooding across three provinces, displacing thousands of residents and prompting the government to declare a state of emergency and deploy military resources for relief efforts.'",
    "Summarize in one sentence: 'The study analyzed data from over 10,000 participants across 15 countries and found a strong correlation between sleep quality and long-term cognitive health outcomes.'",
    "Summarize: 'The new smartphone features a significantly improved camera system, a faster processor, and a larger battery, but critics note the price increase makes it less competitive against rival flagship devices.'",
    "Summarize in one sentence: 'The airline announced it would ground its entire fleet of a specific aircraft model after a mid-air incident, pending a full safety investigation by regulators, disrupting thousands of flights worldwide.'",
    "Summarize: 'A decade-long archaeological excavation uncovered an ancient trading settlement, revealing artifacts from three distinct civilizations and suggesting far more extensive trade networks than previously believed.'",
    "Summarize in one sentence: 'The central bank held interest rates steady for the third consecutive meeting, citing mixed signals from labor market data and persistent but slowing inflation.'",
    "Summarize: 'The university launched a new scholarship program aimed at first-generation college students, covering full tuition and housing costs for up to 200 students per year, funded by a private donor.'",
    "Summarize in one sentence: 'The film, shot entirely on location over 18 months, received critical acclaim for its cinematography but mixed reviews for its unconventional non-linear narrative structure.'",
    "Summarize: 'Engineers completed the final testing phase of the new bridge design, which uses a novel composite material expected to double the structure's lifespan while reducing maintenance costs significantly.'",
    "Summarize in one sentence: 'The video game studio delayed the release of its highly anticipated title by six months to add additional polish and address feedback from an earlier public beta test.'",
    "Summarize: 'A joint research team from three universities published findings showing that a common soil bacterium could be engineered to break down certain plastics far faster than natural decomposition processes.'",
    "Summarize in one sentence: 'The city's water utility completed an infrastructure upgrade that is expected to reduce leakage losses by 30 percent and lower the risk of contamination during heavy rainfall events.'",
]

REASONING = [
    "Why does increasing temperature speed up a chemical reaction? Explain step by step.",
    "Explain step by step why the sky appears blue.",
    "Deduce who is oldest: Ann is older than Bob, Bob is older than Cy.",
    "If all roses are flowers and some flowers fade quickly, can we conclude some roses fade quickly? Explain your reasoning.",
    "Explain why ice floats on water instead of sinking.",
    "A train leaves station A at 60 mph heading toward station B, 300 miles away. How long until it arrives? Explain your reasoning.",
    "Why do we see lightning before we hear thunder? Explain step by step.",
    "If it's true that no cats are dogs, and all poodles are dogs, can a poodle be a cat? Explain.",
    "Explain why a full moon appears larger near the horizon than overhead.",
    "Three friends split a bill of $90 equally, then one of them realizes they forgot to include a $15 tip. How much does each person now owe? Explain the steps.",
    "Why does a metal spoon feel colder than a wooden spoon at the same room temperature? Explain step by step.",
    "If today is Wednesday, what day of the week will it be in 100 days? Explain your reasoning.",
    "Explain step by step why vaccines work by training the immune system.",
    "A farmer has 17 sheep, all but 9 die. How many are left? Explain the trick in this question.",
    "Why does bread rise when you add yeast? Explain the underlying process step by step.",
    "If a bat and a ball cost $1.10 together, and the bat costs $1.00 more than the ball, how much does the ball cost? Explain step by step.",
    "Explain why mixing hot and cold water eventually reaches a uniform temperature.",
    "Deduce the next number in the sequence 2, 6, 12, 20, 30 and explain the pattern.",
    "Why is it colder at high altitudes even though they are closer to the sun? Explain step by step.",
    "Explain why compound interest grows faster than simple interest over time, with reasoning.",
    "If all the mangoes in a basket are ripe except two, and there are 12 mangoes, how many are unripe? Explain step by step.",
    "Explain step by step why mixing baking soda and vinegar produces bubbles.",
    "A clock shows 3:15. What is the angle between the hour and minute hands? Explain the calculation.",
    "Why do objects of different masses fall at the same rate in a vacuum? Explain step by step.",
    "Deduce who arrives first: if Maria arrives before Tom, and Tom arrives before Sam, who is last?",
    "Explain step by step why salt lowers the freezing point of water.",
    "If a train travels 120 miles in 2 hours, then 180 miles in the next 3 hours, what is its average speed for the whole trip? Explain.",
    "Explain why the seasons change on Earth, step by step.",
    "Deduce: All A are B. All B are C. Is it true that all A are C? Explain your reasoning.",
    "Why does a helium balloon rise while a similar balloon filled with air does not? Explain step by step.",
]

CODING = [
    "Write a Python function to check if a number is prime.",
    "Write a Python function that reverses a string without using slicing.",
    "Write a function to find the factorial of a number recursively.",
    "Write a Python function to check if a string is a palindrome.",
    "Write code to find the maximum value in a list without using the built-in max function.",
    "Write a Python function that returns the Fibonacci sequence up to n terms.",
    "Write a function to remove duplicates from a list while preserving order.",
    "Write a Python function to merge two sorted lists into one sorted list.",
    "Write a function that counts the number of vowels in a string.",
    "Write a Python function to flatten a nested list.",
    "Write code to swap two variables without using a temporary variable.",
    "Write a function that checks whether two strings are anagrams of each other.",
    "Write a Python function to find the second largest number in a list.",
    "Write a function that implements bubble sort.",
    "Write a Python function to count the frequency of each word in a sentence.",
    "Write code to find the intersection of two lists.",
    "Write a Python function that returns True if a year is a leap year.",
    "Write a function to compute the sum of digits of a number.",
    "Write a Python function that implements binary search on a sorted list.",
    "Write code to generate all permutations of a short string.",
]

OPEN_ENDED = [
    "What's a good icebreaker question for a team meeting?",
    "Give me three tips for staying focused while working from home.",
    "Suggest a name for a coffee shop that specializes in cold brew.",
    "What's a healthy breakfast I can make in under 10 minutes?",
    "Give me a short motivational quote about persistence.",
    "Suggest three books for someone who enjoyed 'Dune'.",
    "What are some good conversation starters for a first date?",
    "Give me a simple explanation of what a firewall does in networking.",
    "Suggest a weekend itinerary for a first-time visitor to Kyoto.",
    "What's the difference between a virus and bacteria, in simple terms?",
    "Give me three ideas for a birthday gift for someone who loves hiking.",
    "Explain what a black hole is to a curious 10-year-old.",
    "What's a good way to start learning a new language as an adult?",
    "Suggest a title for a blog post about remote work productivity.",
    "What's the difference between weather and climate?",
    "Give me two tips for giving constructive feedback to a coworker.",
    "Suggest a fun team-building activity for a remote team.",
    "What's a simple way to explain compound interest to a teenager?",
    "Give me three questions to ask in a job interview as the candidate.",
    "Suggest a playlist theme for a long road trip.",
    "What's a good way to organize a cluttered home office?",
]

PROMPTS = []
for lst, tag in [
    (MATH_EASY, "math_easy"), (MATH_HARD, "math_hard"),
    (CLASSIFICATION, "classification"), (QA, "qa"),
    (EXTRACTION, "extraction"), (SUMMARIZATION, "summarization"),
    (REASONING, "reasoning"), (CODING, "coding"), (OPEN_ENDED, "open_ended"),
]:
    for p in lst:
        PROMPTS.append((p, tag))

print(f"Total prompts: {len(PROMPTS)}")
assert len(PROMPTS) >= 200, f"Need >= 200 prompts, got {len(PROMPTS)}"


def post_json(path, body, timeout=90):
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        BASE + path, data=data,
        headers={"Content-Type": "application/json"}, method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def select_remote(model_id):
    try:
        post_json("/api/models/remote/select", {"model": model_id}, timeout=15)
        return True
    except Exception as e:
        print(f"  [WARN] could not switch remote model to {model_id}: {e}")
        return False


def main():
    results = []
    t_start = time.time()

    model_idx = 0
    switch_every = max(1, len(PROMPTS) // len(REMOTE_MODELS))

    with open("smoke_results.jsonl", "w") as out:
        for i, (task, tag) in enumerate(PROMPTS):
            if i % switch_every == 0:
                model = REMOTE_MODELS[model_idx % len(REMOTE_MODELS)]
                select_remote(model)
                model_idx += 1

            t0 = time.time()
            record = {"i": i, "task": task, "expected_tag": tag}
            try:
                resp = post_json("/api/route", {"task": task})
                record.update({
                    "ok": True,
                    "category": resp.get("category"),
                    "source": resp.get("source"),
                    "confidence": resp.get("confidence"),
                    "remote_tokens": resp.get("remote_tokens"),
                    "latency_ms": resp.get("latency_ms"),
                    "answer_preview": (resp.get("answer") or "")[:150],
                })
            except urllib.error.HTTPError as e:
                record.update({"ok": False, "error": f"HTTP_{e.code}: {e.read().decode(errors='replace')[:200]}"})
            except Exception as e:
                record.update({"ok": False, "error": str(e)[:200]})
            record["wall_ms"] = round((time.time() - t0) * 1000)

            out.write(json.dumps(record) + "\n")
            out.flush()
            results.append(record)

            if (i + 1) % 10 == 0:
                elapsed = time.time() - t_start
                ok = sum(1 for r in results if r.get("ok"))
                local = sum(1 for r in results if r.get("source") == "local")
                remote = sum(1 for r in results if r.get("source") == "remote")
                print(f"...{i+1}/{len(PROMPTS)}  ok={ok} local={local} remote={remote}  elapsed={elapsed:.0f}s")

    t_total = time.time() - t_start
    print(f"\n=== DONE in {t_total:.0f}s ===")
    print(f"Total: {len(results)}")
    print(f"OK: {sum(1 for r in results if r.get('ok'))}")
    print(f"Errors: {sum(1 for r in results if not r.get('ok'))}")
    print(f"Local: {sum(1 for r in results if r.get('source') == 'local')}")
    print(f"Remote: {sum(1 for r in results if r.get('source') == 'remote')}")
    json.dump(results, open("smoke_results_full.json", "w"))


if __name__ == "__main__":
    main()
