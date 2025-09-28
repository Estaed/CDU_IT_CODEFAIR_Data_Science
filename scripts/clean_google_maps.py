import pandas as pd
from pathlib import Path
from common import normalize_place, clean_text, ensure_dir


RAW_DIR = Path("/data/raw_data/googlemaps")
OUT_DIR = Path("data/interim")
OUT = OUT_DIR / "google_clean.csv"


def load_concat() -> pd.DataFrame:
    frames = []
    for csv in sorted(RAW_DIR.glob("*.csv")):
        df = pd.read_csv(csv)
        # Expected columns from samples: nama_tempat,user,review,rating OR similar
        df = df.rename(columns={
            "nama_tempat": "place",
            "review": "comment",
        })
        frames.append(df)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=["place", "comment"]) 


def main() -> None:
    ensure_dir(str(OUT_DIR))
    df = load_concat()
    if df.empty:
        pd.DataFrame(columns=["source", "place", "comment"]).to_csv(OUT, index=False)
        return

    df["place"] = df["place"].map(normalize_place)
    df["comment"] = df["comment"].map(clean_text)

    keep = df[["place", "comment"]].copy()
    keep.insert(0, "source", "GoogleMaps")
    keep = keep[(keep["comment"].str.len() > 5) & keep["comment"].notna()]
    keep.drop_duplicates(subset=["source", "place", "comment"], inplace=True)
    keep.to_csv(OUT, index=False)


if __name__ == "__main__":
    main()


