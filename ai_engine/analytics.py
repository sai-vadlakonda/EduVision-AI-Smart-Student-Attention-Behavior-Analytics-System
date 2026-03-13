import json

def save_ranking(ranking):

    with open("../ranking.json","w") as f:
        json.dump(ranking,f)


def save_emotions(emotion_counts):

    with open("../emotion_stats.json","w") as f:
        json.dump(emotion_counts,f)


def save_alerts(alerts):

    with open("../alerts.json","w") as f:
        json.dump(alerts,f)