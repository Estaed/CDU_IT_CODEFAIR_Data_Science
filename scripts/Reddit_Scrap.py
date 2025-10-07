# pip install praw
import praw
import re
import csv

reddit = praw.Reddit(
    client_id="djmHiO6PUKAhQXBZPtKuRw",
    client_secret="1UhWTOnY9xpyoFkM6wlWpSMYPBnZ1w",
    user_agent="IT code fair"
)

# -----------------------------
# Place names & common search terms
# -----------------------------
# places = {
#     "Uluru": r"Uluru|Ayers Rock|Kata Tjuta",
#     "Alice_Springs_Desert_Park": r"Alice Springs Desert Park|Alice Springs park|Alice Springs",
#     "Devils_Marbles": r"Devils Marbles|Karlu Karlu|Karlu",
#     "Kakadu_Gunlom_Falls": r"Kakadu|Gunlom Falls|Gunlom",
#     "West_MacDonnell_Ormiston": r"West MacDonnell|Ormiston Gorge|West Macs|Ormiston",
#     "Nitmiluk_Katherine_Gorge": r"Nitmiluk|Katherine Gorge|Katherine"
# }

places = {
    "Nitmiluk_Katherine_Gorge": r"Nitmiluk|Katherine Gorge|Katherine"
}

# -----------------------------
# Export comments for each place
# -----------------------------
for place, regex in places.items():
    pattern = re.compile(rf"\b({regex})\b", re.IGNORECASE)
    filename = place + ".csv"

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["submission_id", "comment_id", "subreddit", "author", "created_utc", "comment_body"])

        # search submissions using just one of the main common terms (to reduce noise)
        main_term = regex.split("|")[0]  # e.g. "Uluru"
        for submission in reddit.subreddit("all").search(main_term, limit=100):
            submission.comments.replace_more(limit=0)
            for comment in submission.comments.list():
                if pattern.search(comment.body):
                    writer.writerow([
                        submission.id,
                        comment.id,
                        str(submission.subreddit),
                        str(comment.author),
                        comment.created_utc,
                        comment.body.replace("\n", " ")[:5000]
                    ])
    print(f"✅ Exported comments mentioning {place} → {filename}")