def calculate_attention(head_direction, emotion, phone_detected):

    score = 0.0

    # -------------------------
    # Head direction importance
    # -------------------------
    if head_direction == "Forward":
        score += 0.5

    elif head_direction in ["Left", "Right"]:
        score += 0.25

    elif head_direction == "Down":
        score += 0.1

    else:
        score += 0.2


    # -------------------------
    # Emotion impact
    # -------------------------
    if emotion in ["happy", "neutral"]:
        score += 0.3

    elif emotion in ["sad", "angry"]:
        score += 0.1

    elif emotion == "surprise":
        score += 0.2

    else:
        score += 0.15


    # -------------------------
    # Phone penalty
    # -------------------------
    if phone_detected:
        score -= 0.4
    else:
        score += 0.2


    # Clamp score between 0 and 1
    score = max(0, min(score, 1))

    return round(score, 2)


def classify_attention(score, phone_detected):

    if phone_detected:
        return "Using Phone"

    if score >= 0.75:
        return "Highly Attentive"

    elif score >= 0.5:
        return "Moderately Attentive"

    elif score >= 0.3:
        return "Distracted"

    else:
        return "Not Paying Attention"


# -------------------------
# Productivity score
# -------------------------

def classroom_productivity(avg_attention, phone_users, total_students):

    if total_students == 0:
        return 0

    phone_penalty = phone_users * 0.05

    productivity = avg_attention - phone_penalty

    productivity = max(0, min(productivity, 1))

    return round(productivity, 2)