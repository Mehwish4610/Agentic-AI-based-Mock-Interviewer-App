# utils/badges.py

def assign_badges(analysis):
    badges = []

    if len(analysis['skills']) >= 5:
        badges.append("Skill Pro")

    if analysis['experience_years'] >= 2:
        badges.append("Experienced Candidate")

    if "Master's" in analysis['education']:
        badges.append("Advanced Degree Holder")

    if not badges:
        badges.append("Rising Star")

    return badges
