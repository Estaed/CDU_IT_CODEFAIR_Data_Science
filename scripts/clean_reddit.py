import pandas as pd
from pathlib import Path
from common import normalize_place, clean_text, ensure_dir


RAW_DIR = Path("/data/raw_data/Reddit_comment")
OUT_DIR = Path("data/interim")
OUT = OUT_DIR / "reddit_clean.csv"


def infer_place_from_filename(path: Path) -> str:
    name = path.stem.replace("_", " ")
    return normalize_place(name)


def load_concat() -> pd.DataFrame:
    frames = []
    for csv in sorted(RAW_DIR.glob("*.csv")):
        df = pd.read_csv(csv)
        # Expected columns: subreddit, comment_body, ...
        if "comment_body" in df.columns:
            comment_col = "comment_body"
        elif "comment" in df.columns:
            comment_col = "comment"
        else:
            continue

        place = infer_place_from_filename(csv)
        sub = df["subreddit"].astype(str) if "subreddit" in df.columns else "reddit"

        out = pd.DataFrame({
            "source": sub.apply(lambda s: f"Reddit/{s}"),
            "place": place,
            "comment": df[comment_col].astype(str),
        })
        frames.append(out)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=["source", "place", "comment"]) 


def main() -> None:
    ensure_dir(str(OUT_DIR))
    df = load_concat()
    if df.empty:
        pd.DataFrame(columns=["source", "place", "comment"]).to_csv(OUT, index=False)
        return

    df["place"] = df["place"].map(normalize_place)
    df["comment"] = df["comment"].map(clean_text)

    keep = df[(df["comment"].str.len() > 5) & df["comment"].notna()].copy()
    keep.drop_duplicates(subset=["source", "place", "comment"], inplace=True)
    keep.to_csv(OUT, index=False)


if __name__ == "__main__":
    main()


