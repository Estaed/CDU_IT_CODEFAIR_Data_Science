import pandas as pd
from pathlib import Path
from common import normalize_place, clean_text, ensure_dir


RAW = Path("data/raw_data/australian_dark_sky_reviews_final_clean_FIXED2.csv")
OUT_DIR = Path("data/generate_stars/interim")
OUT = OUT_DIR / "tripadvisor_clean.csv"


def main() -> None:
    ensure_dir(str(OUT_DIR))
    df = pd.read_csv(RAW)

    # Expected columns from sample: place_name, text, rating, date_iso, ...
    df = df.rename(columns={
        "place_name": "place",
        "text": "comment",
    })

    df["place"] = df["place"].map(normalize_place)
    df["comment"] = df["comment"].map(clean_text)

    keep = df[["place", "comment"]].copy()
    keep.insert(0, "source", "TripAdvisor")
    keep = keep[(keep["comment"].str.len() > 5) & keep["comment"].notna()]
    keep.drop_duplicates(subset=["source", "place", "comment"], inplace=True)
    keep.to_csv(OUT, index=False)


if __name__ == "__main__":
    main()


