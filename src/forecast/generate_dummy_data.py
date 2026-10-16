"""Generate realistic historical entrance exam and admission data for NIT Trichy.

Data models:
- National JEE Main applicant trends (2016-2024)
- NIT Trichy branch-wise seat matrix, JoSAA choices/applicants, cutoff ranks,
  seats filled, acceptance rates, and competition ratios.
"""

from pathlib import Path
from hashlib import sha256
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "exam"

NATIONAL_JEE_DATA = {
    2016: 1194932,
    2017: 1186454,
    2018: 1135084,
    2019: 1147125,
    2020: 1023000,
    2021: 939008,
    2022: 1026799,
    2023: 1162398,
    2024: 1415110,
}

COURSES_SPEC = {
    "CSE": {
        "name": "Computer Science & Engineering",
        "dept": "Computer Science",
        "intake_base": 92,
        "intake_2024": 119,
        "pref_share_2016": 0.082,  # 8.2% of national pool
        "pref_share_2024": 0.140,  # 14.0%
        "open_rank_2016": 950,
        "open_rank_2024": 620,
        "close_rank_2016": 6100,
        "close_rank_2024": 4150,
    },
    "ECE": {
        "name": "Electronics & Communication Engineering",
        "dept": "Electronics & Communication",
        "intake_base": 92,
        "intake_2024": 119,
        "pref_share_2016": 0.068,
        "pref_share_2024": 0.098,
        "open_rank_2016": 2100,
        "open_rank_2024": 1850,
        "close_rank_2016": 10200,
        "close_rank_2024": 7850,
    },
    "EEE": {
        "name": "Electrical & Electronics Engineering",
        "dept": "Electrical & Electronics",
        "intake_base": 92,
        "intake_2024": 115,
        "pref_share_2016": 0.052,
        "pref_share_2024": 0.065,
        "open_rank_2016": 4200,
        "open_rank_2024": 3900,
        "close_rank_2016": 16500,
        "close_rank_2024": 13200,
    },
    "MECH": {
        "name": "Mechanical Engineering",
        "dept": "Mechanical Engineering",
        "intake_base": 105,
        "intake_2024": 120,
        "pref_share_2016": 0.065,
        "pref_share_2024": 0.048,
        "open_rank_2016": 5100,
        "open_rank_2024": 6800,
        "close_rank_2016": 18200,
        "close_rank_2024": 21500,
    },
    "CIVIL": {
        "name": "Civil Engineering",
        "dept": "Civil Engineering",
        "intake_base": 100,
        "intake_2024": 118,
        "pref_share_2016": 0.045,
        "pref_share_2024": 0.032,
        "open_rank_2016": 9200,
        "open_rank_2024": 12500,
        "close_rank_2016": 27500,
        "close_rank_2024": 34500,
    },
    "CHEM": {
        "name": "Chemical Engineering",
        "dept": "Chemical Engineering",
        "intake_base": 85,
        "intake_2024": 105,
        "pref_share_2016": 0.038,
        "pref_share_2024": 0.031,
        "open_rank_2016": 8500,
        "open_rank_2024": 11000,
        "close_rank_2016": 26000,
        "close_rank_2024": 31200,
    },
    "ICE": {
        "name": "Instrumentation & Control Engineering",
        "dept": "Instrumentation & Control",
        "intake_base": 85,
        "intake_2024": 104,
        "pref_share_2016": 0.032,
        "pref_share_2024": 0.035,
        "open_rank_2016": 7900,
        "open_rank_2024": 8800,
        "close_rank_2016": 24200,
        "close_rank_2024": 25600,
    },
    "PROD": {
        "name": "Production Engineering",
        "dept": "Production Engineering",
        "intake_base": 80,
        "intake_2024": 102,
        "pref_share_2016": 0.028,
        "pref_share_2024": 0.024,
        "open_rank_2016": 12000,
        "open_rank_2024": 14500,
        "close_rank_2016": 32000,
        "close_rank_2024": 38900,
    },
    "MME": {
        "name": "Metallurgical & Materials Engineering",
        "dept": "Metallurgical & Materials",
        "intake_base": 60,
        "intake_2024": 92,
        "pref_share_2016": 0.024,
        "pref_share_2024": 0.020,
        "open_rank_2016": 13500,
        "open_rank_2024": 16200,
        "close_rank_2016": 36000,
        "close_rank_2024": 44500,
    },
}


def generate_historical_dataset() -> pd.DataFrame:
    years = sorted(NATIONAL_JEE_DATA.keys())
    min_year, max_year = years[0], years[-1]
    rows = []

    for year in years:
        total_jee = NATIONAL_JEE_DATA[year]
        factor = (year - min_year) / (max_year - min_year)

        for course_id, meta in COURSES_SPEC.items():
            # Linear/eased interpolation for seat intake:
            intake = int(round(meta["intake_base"] + factor * (meta["intake_2024"] - meta["intake_base"])))
            
            # Preference share with minor realistic jitter
            pref_share = meta["pref_share_2016"] + factor * (meta["pref_share_2024"] - meta["pref_share_2016"])
            # Small random-like deterministic wobble based on year and course
            seed = int.from_bytes(sha256(f"{course_id}_{year}".encode()).digest()[:4], "big")
            wobble = ((seed % 100) - 50) / 10000.0
            pref_share = max(0.01, pref_share + wobble)

            # Total students expressing preference for NIT Trichy course in JoSAA
            course_applicants = int(round(total_jee * pref_share))

            # Opening and Closing ranks
            open_rank = int(round(meta["open_rank_2016"] + factor * (meta["open_rank_2024"] - meta["open_rank_2016"])))
            close_rank = int(round(meta["close_rank_2016"] + factor * (meta["close_rank_2024"] - meta["close_rank_2016"])))

            # Seats filled at NIT Trichy is typically 100% (or slightly below due to round 6 drops)
            seats_filled = intake if year != 2020 else intake - 1

            # Key user metrics:
            # Acceptance rate (% of applicants getting the seat)
            acceptance_rate_pct = round((seats_filled / course_applicants) * 100, 4)
            # Applicants per seat
            applicants_per_seat = round(course_applicants / intake, 1)

            rows.append({
                "year": year,
                "institute": "National Institute of Technology, Tiruchirappalli (NIT Trichy)",
                "course_id": course_id,
                "course_name": meta["name"],
                "department": meta["dept"],
                "national_exam_applicants": total_jee,
                "course_applicants": course_applicants,
                "preference_share_pct": round(pref_share * 100, 3),
                "sanctioned_intake": intake,
                "seats_filled": seats_filled,
                "fill_rate_pct": round((seats_filled / intake) * 100, 1),
                "opening_rank": open_rank,
                "closing_rank": close_rank,
                "acceptance_rate_pct": acceptance_rate_pct,
                "applicants_per_seat": applicants_per_seat,
            })

    df = pd.DataFrame(rows)
    return df


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    df = generate_historical_dataset()
    csv_path = DATA_DIR / "entrance_exam_history.csv"
    df.to_csv(csv_path, index=False)
    print(f"Generated {len(df)} records for {len(COURSES_SPEC)} courses across {len(NATIONAL_JEE_DATA)} years.")
    print(f"Saved to: {csv_path}")


if __name__ == "__main__":
    main()
