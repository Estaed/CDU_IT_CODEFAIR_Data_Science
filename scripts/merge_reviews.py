import pandas as pd
from pathlib import Path
from common import ensure_dir


INTERIM = Path("data/generate_stars/interim")
OUT_DIR = Path("data/generate_stars/processed")
OUT = OUT_DIR / "reviews_unified.csv"


def main() -> None:
    ensure_dir(str(OUT_DIR))
    frames = []
    for name in ["tripadvisor_clean.csv", "google_clean.csv", "reddit_clean.csv"]:
        p = INTERIM / name
        if p.exists():
            frames.append(pd.read_csv(p))

    if not frames:
        pd.DataFrame(columns=["source", "place", "comment"]).to_csv(OUT, index=False)
        return

    df = pd.concat(frames, ignore_index=True)
    df.dropna(subset=["comment"], inplace=True)
    df = df[(df["comment"].str.len() > 5)]

    # dedupe on exact triplet
    df.drop_duplicates(subset=["source", "place", "comment"], inplace=True)

    # shuffle rows before saving
    df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
    df.to_csv(OUT, index=False)


if __name__ == "__main__":
    main()


