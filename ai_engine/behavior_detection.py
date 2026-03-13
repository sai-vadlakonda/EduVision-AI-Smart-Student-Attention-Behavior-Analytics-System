def detect_sleeping(head_direction, attention_score):
    
    if head_direction == "Down" and attention_score < 0.3:
        return True
    
    return False


def detect_copying(head_direction, students_detected):

    if head_direction in ["Left", "Right"] and students_detected > 1:
        return True
    
    return False