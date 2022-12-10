import os
from datetime import datetime
from typing import Dict, List

from slack_bolt import App
from slack_sdk.errors import SlackApiError
import requests
import re
import humanfriendly

BY_TIME_PAT = re.compile(r"scoreboard by time\s*(\d+)?", flags=re.IGNORECASE)

CHANNEL_ID = "C01G7DC9BJM" # advent-of-cocde
# CHANNEL_ID = "C04D6FAKWDQ"  # app-testing

EMOJIS = {
    0: ":first_place_medal:",
    1: ":second_place_medal:",
    2: ":third_place_medal:",
    "Stephen Mullins": ":samus_run:",
}

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)


def fetch_scores():
    res = requests.get('https://adventofcode.com/2022/leaderboard/private/view/134020.json', cookies={
        "session": os.environ.get("AOC_SESSION")})

    for member in res.json()["members"].values():
        yield {
            "name": member["name"],
            "score": member["local_score"],
            "stars": member["stars"],
            "completion_day_level": member["completion_day_level"]
        }


def format_line(index, score):
    place = EMOJIS.get(index, "       ")
    emoji = EMOJIS.get(score["name"], "")
    return f"{place} {score['score']} ({score['stars']}:star:) {score['name']} {emoji}"


def get_latest_day(scores):
    return str(max([int(k) for score in scores for k in score["completion_day_level"].keys()]))


def puzzle_by_time(scores, day):
    for score in scores:
        if day in score["completion_day_level"]:
            yield {
                "name": score["name"],
                "part_1_ts": score["completion_day_level"][day]['1']["get_star_ts"],
                "part_2_ts": score["completion_day_level"][day].get("2", {}).get("get_star_ts", 0)
            }


def format_time_line(index, score, day):
    def time_taken(ts):
        if not ts:
            return ""
        # 5 because midnight EST to UTC
        text = humanfriendly.format_timespan(datetime.utcfromtimestamp(ts) - datetime(2022, 12, day, 5))
        return text.replace(" hours", "h").replace(" minutes", "m").replace(" seconds", "s")

    place = EMOJIS.get(index, "       ")
    emoji = EMOJIS.get(score["name"], "")
    part_1 = time_taken(score["part_1_ts"])
    part_2 = time_taken(score["part_2_ts"])
    return f"{place} {score['name']}: {part_1} | {part_2} | {emoji}"


def by_time(scores: List[Dict], day=None) -> str:
    day = day or get_latest_day(scores)
    sorted_scores = sorted(puzzle_by_time(scores, day), key=lambda x: x["part_1_ts"])
    return "\n".join([format_time_line(index, score, int(day))
                      for index, score in enumerate(sorted_scores)])


def by_score(scores: List[Dict]) -> str:
    return "\n".join([format_line(index, score)
                      for index, score in enumerate(scores) if score["score"] > 0])


def command(text, scores):
    m = BY_TIME_PAT.match(text)
    if m:
        return lambda: by_time(scores, m.group(1))
    return lambda: by_score(scores)


@app.event("message")
def foo(client, event, logger):
    text = event.get('text', '')
    if not text.startswith("scoreboard"):
        print("skipping message")
        return

    try:
        scores = sorted(fetch_scores(), key=lambda x: x["score"], reverse=True)
        text_func = command(text, scores)

        today = datetime.today().day
        result = client.chat_postMessage(
            channel=CHANNEL_ID,
            text="make the warning go away",
            blocks=[
                {"type": "section",
                 "text": {"type": "plain_text", "text": "AOC 2022 scores!:calendar: :christmas_tree:"}},
                {"type": "section", "text": {"type": "plain_text", "text": text_func()}},
                {"type": "section", "text": {"type": "plain_text", "text": f"Only {25 - today} days left!"}},
            ]
        )
        # Print result, which includes information about the message (like TS)
        print(result)

    except SlackApiError as e:
        print(f"Error: {e}")


# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
