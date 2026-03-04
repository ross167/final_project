"""
Collection Display Likelihood Assessor
Met and Louvre Museums

Scoring is based on statistical patterns in the Met and Louvre
collection datasets. This is a heuristic tool, not a guarantee of display.
"""

import os

MET_BASE    = 15.3
LOUVRE_BASE = 26.7


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def header():
    print()
    print("  Collection Display Likelihood Assessor")
    print("  Metropolitan Museum of Art and the Louvre")
    print()


def progress(current, total):
    filled = "#" * current
    empty  = "-" * (total - current)
    pct    = int((current / total) * 100)
    print(f"  Progress  [{filled}{empty}]  {pct}%")
    print()


STEPS = [
    {
        "id":       "acquisition",
        "label":    "Acquisition Type",
        "question": "How was the painting acquired?",
        "hint":     "Acquisition method is the strongest single predictor of display status at the Met.",
        "options": [
            ("gift",     "Gift or Bequest",  "Donated by a collector or estate"),
            ("purchase", "Purchase",          "Bought by the institution"),
            ("transfer", "Transfer",          "Moved from another collection"),
            ("other",    "Other / Unknown",   "Commission, exchange, or undocumented"),
        ],
        "met_w":    {"gift": 0.59, "purchase": 1.10, "transfer": 0.95, "other": 2.29},
        "louvre_w": {"gift": 0.88, "purchase": 1.12, "transfer": 0.95, "other": 1.05},
    },
    {
        "id":       "period",
        "label":    "Period",
        "question": "When was the painting created?",
        "hint":     "Both institutions favour historical European works in their main display galleries.",
        "options": [
            ("medieval",     "Medieval",                "Before 1400"),
            ("renaissance",  "Renaissance",             "1400-1600"),
            ("baroque",      "Baroque / Old Masters",   "1600-1750"),
            ("neoclassical", "Neoclassical / Romantic", "1750-1850"),
            ("modern",       "Modern",                  "1850-1950"),
            ("contemporary", "Contemporary",            "Post-1950"),
        ],
        "met_w":    {"medieval": 1.10, "renaissance": 1.40, "baroque": 1.35,
                     "neoclassical": 1.20, "modern": 1.00, "contemporary": 0.65},
        "louvre_w": {"medieval": 1.20, "renaissance": 1.55, "baroque": 1.45,
                     "neoclassical": 1.30, "modern": 0.60, "contemporary": 0.30},
    },
    {
        "id":       "medium",
        "label":    "Medium and Surface",
        "question": "What is the medium and surface?",
        "hint":     "Stable media on durable surfaces are more practical to display long-term.",
        "options": [
            ("oil_canvas",  "Oil on Canvas",                "Most common display format"),
            ("oil_panel",   "Oil or Tempera on Panel",      "Older and more fragile"),
            ("watercolour", "Watercolour / Works on Paper", "Light-sensitive; often rotated off display"),
            ("fresco",      "Fresco or Mural-derived",      "Rare; usually requires purpose-built display"),
            ("other_med",   "Mixed or Other",               "Pastel, gouache, encaustic, etc."),
        ],
        "met_w":    {"oil_canvas": 1.15, "oil_panel": 1.05, "watercolour": 0.70,
                     "fresco": 1.20, "other_med": 0.85},
        "louvre_w": {"oil_canvas": 1.10, "oil_panel": 1.20, "watercolour": 0.65,
                     "fresco": 1.25, "other_med": 0.80},
    },
    {
        "id":       "origin",
        "label":    "Geographic Origin",
        "question": "Where does the painting originate?",
        "hint":     "Both institutions built their core display collections around Western European works.",
        "options": [
            ("french",     "French",               "Central to the Louvre's mission"),
            ("italian",    "Italian",              "High-prestige works at both institutions"),
            ("dutch_flem", "Dutch or Flemish",     "Strong representation at both museums"),
            ("other_eur",  "Other European",       "Spanish, German, British, etc."),
            ("american",   "North American",       "Core of the Met's modern holdings"),
            ("other",      "Asian, African, Other","Specialist galleries; variable display rates"),
        ],
        "met_w":    {"french": 1.10, "italian": 1.20, "dutch_flem": 1.15,
                     "other_eur": 1.05, "american": 1.20, "other": 0.80},
        "louvre_w": {"french": 1.40, "italian": 1.30, "dutch_flem": 1.15,
                     "other_eur": 1.05, "american": 0.50, "other": 0.65},
    },
    {
        "id":       "subject",
        "label":    "Subject Matter",
        "question": "What is the primary subject of the painting?",
        "hint":     "Narrative and figurative works tend to attract more visitor engagement and curatorial attention.",
        "options": [
            ("religious",  "Religious or Mythological", "Altarpieces, biblical scenes, gods"),
            ("portrait",   "Portrait",                  "Individual or group likeness"),
            ("landscape",  "Landscape or Seascape",     "Natural or urban scenery"),
            ("genre",      "Genre / Everyday Life",     "Domestic scenes, still life"),
            ("historical", "Historical or Allegorical", "Narrative historical scenes"),
            ("abstract",   "Abstract or Decorative",    "Non-representational works"),
        ],
        "met_w":    {"religious": 1.15, "portrait": 1.20, "landscape": 1.05,
                     "genre": 1.10, "historical": 1.15, "abstract": 0.90},
        "louvre_w": {"religious": 1.30, "portrait": 1.10, "landscape": 0.95,
                     "genre": 1.05, "historical": 1.25, "abstract": 0.55},
    },
    {
        "id":       "size",
        "label":    "Physical Size",
        "question": "How large is the painting?",
        "hint":     "Gallery space is finite. The Met averages 67% more space per displayed painting than the Louvre.",
        "options": [
            ("small",      "Small",      "Under 0.5 sq m  --  miniature or cabinet painting"),
            ("medium",     "Medium",     "0.5-2 sq m  --  typical gallery painting"),
            ("large",      "Large",      "2-5 sq m  --  salon-scale"),
            ("very_large", "Very Large", "Over 5 sq m  --  monumental"),
        ],
        "met_w":    {"small": 0.90, "medium": 1.10, "large": 1.05, "very_large": 0.85},
        "louvre_w": {"small": 0.95, "medium": 1.05, "large": 1.15, "very_large": 1.10},
    },
    {
        "id":       "condition",
        "label":    "Condition",
        "question": "What is the painting's current condition?",
        "hint":     "Works in poor condition are prioritised for conservation storage rather than public display.",
        "options": [
            ("excellent", "Excellent", "Ready to display immediately"),
            ("good",      "Good",      "Minor issues; display-ready"),
            ("fair",      "Fair",      "Stable but requires monitoring"),
            ("poor",      "Poor",      "Conservation priority; storage recommended"),
        ],
        "met_w":    {"excellent": 1.20, "good": 1.05, "fair": 0.80, "poor": 0.35},
        "louvre_w": {"excellent": 1.20, "good": 1.05, "fair": 0.80, "poor": 0.35},
    },
]


def calc_score(answers, base, weight_key):
    score = base
    for step in STEPS:
        val = answers.get(step["id"])
        if val and weight_key in step:
            score *= step[weight_key].get(val, 1.0)
    return max(0.5, min(97.0, score))


def bar(pct, width=30):
    filled = round((pct / 100) * width)
    return "[" + "#" * filled + "-" * (width - filled) + "]"


def verdict(met_score, louvre_score):
    avg = (met_score + louvre_score) / 2
    if avg >= 55:
        return "  Strong display candidate"
    if avg >= 35:
        return "  Likely display candidate"
    if avg >= 20:
        return "  Borderline -- context dependent"
    return "  Storage recommended"


def ask(step, step_num, total):
    while True:
        clear()
        header()
        progress(step_num, total)

        print(f"  {step['label'].upper()}")
        print(f"  {step['question']}")
        print()
        print(f"  Note: {step['hint']}")
        print()

        options = step["options"]
        for i, (val, label, desc) in enumerate(options, 1):
            print(f"  [{i}] {label}  --  {desc}")

        print()
        print("  " + "-" * 50)
        choice = input("  Enter a number: ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1][0]

        print(f"\n  Please enter a number between 1 and {len(options)}.")
        input("  Press Enter to try again...")


def show_results(answers, met_score, louvre_score):
    clear()
    header()

    print(verdict(met_score, louvre_score))
    print()
    print("  " + "-" * 50)
    print()

    print("  Display Likelihood")
    print()
    print(f"  The Met    {bar(met_score)}  {met_score:5.1f}%")
    print()
    print(f"  Louvre     {bar(louvre_score)}  {louvre_score:5.1f}%")
    print()
    print("  " + "-" * 50)
    print()

    print("  vs. Collection Average")
    print()
    for label, score, base in [
        ("The Met", met_score,    MET_BASE),
        ("Louvre",  louvre_score, LOUVRE_BASE),
    ]:
        diff = score - base
        sign = "+" if diff >= 0 else ""
        print(f"  {label:<10} {bar(score)}  {sign}{diff:.1f}pp  (average {base}%)")

    print()
    print("  pp = percentage points difference from each museum's overall display rate.")
    print()
    print("  " + "-" * 50)
    print()

    print("  Assessment Inputs")
    print()
    for step in STEPS:
        val = answers.get(step["id"])
        opt = next((o for o in step["options"] if o[0] == val), None)
        if opt:
            print(f"  {step['label']:<24} {opt[1]}")

    print()
    print("  " + "-" * 50)
    print()
    print("  Note: Scores are heuristic estimates based on statistical patterns in the")
    print("  Met and Louvre collection datasets. They reflect population-level display")
    print("  tendencies, not institutional decisions. Curatorial judgement, loan status,")
    print("  and gallery scheduling are always additional factors.")
    print()


def main():
    while True:
        clear()
        header()
        print("  This tool estimates the likelihood of a painting being displayed")
        print("  at the Metropolitan Museum of Art or the Louvre, based on")
        print("  statistical patterns in their collection data.")
        print()
        print(f"  Met baseline display rate:    {MET_BASE}%")
        print(f"  Louvre baseline display rate: {LOUVRE_BASE}%")
        print()
        print("  " + "-" * 50)
        input("  Press Enter to begin the assessment...")

        answers = {}

        for i, step in enumerate(STEPS, 1):
            answers[step["id"]] = ask(step, i, len(STEPS))

        met_score    = calc_score(answers, MET_BASE,    "met_w")
        louvre_score = calc_score(answers, LOUVRE_BASE, "louvre_w")

        show_results(answers, met_score, louvre_score)

        again = input("  Assess another painting? (y/n): ").strip().lower()
        if again != "y":
            clear()
            print()
            print("  Collection Display Likelihood Assessor")
            print("  Session ended.")
            print()
            break


if __name__ == "__main__":
    main()
