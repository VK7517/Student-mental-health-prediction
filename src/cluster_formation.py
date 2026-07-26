# Depression Level
def depression_level(score):
    if score <= 9:
        return "Normal"
    elif score <= 13:
        return "Mild"
    elif score <= 20:
        return "Moderate"
    else :
        return "Severe/Extremely Severe"

# Anxiety Level
def anxiety_level(score):
    if score <= 7:
        return "Normal"
    elif score <= 9:
        return "Mild"
    elif score <= 14:
        return "Moderate"
    else :
        return "Severe/Extremely Severe"


# Stress Level
def stress_level(score):
    if score <= 14:
        return "Normal"
    elif score <= 18:
        return "Mild"
    elif score <= 25:
        return "Moderate"
    else :
        return "Severe/Extremely Severe"


# BRS Level
def brs_level(score):
    if score == 0:
        return "Balanced wellbeing"
    elif score < 3.0:
        return "Low"
    elif score <= 4.3:
        return "Average"
    else:
        return "High"


# Cluster Logic
def assign_cluster(row):
    
    ghq = row["GHQ"]
    
    dep = row["Depression_Level"]
    anx = row["Anxiety_Level"]
    stress = row["Stress_Level"]
    
    brs = row["BRS_Level"]
    
    # Cluster A
    if ghq < 12:
        return "A"
    
    
    # Count Moderate/Severe Domains
    
    moderate_or_severe = [
        dep in ["Moderate", "Severe/Extremely Severe"],
        anx in ["Moderate", "Severe/Extremely Severe"],
        stress in ["Moderate", "Severe/Extremely Severe"]
    ]
    
    count_mod = sum(moderate_or_severe)
    

    # Check Severe Domains
    
    severe_present = (
        dep in ["Severe/Extremely Severe"] or
        anx in ["Severe/Extremely Severe"] or
        stress in ["Severe/Extremely Severe"]
    )
    

    # Cluster E
    
    if severe_present and brs == "High":
        return "E"
    
    # Cluster F
    
    if severe_present and brs == "Low":
        return "F"

    # Cluster G
    if (
        ghq >= 12 and
        dep in ["Normal", "Mild"] and
        anx in ["Normal", "Mild"] and
        stress in ["Normal", "Mild"] and
        brs == "Low"
    ):
        return "G"


    # Cluster B
    
    if (
        12 <= ghq and
        dep in ["Normal", "Mild"] and
        anx in ["Normal", "Mild"] and
        stress in ["Normal", "Mild"] and
        brs in ["Average", "High"]
    ):
        return "B"
    
    # Cluster H

    if (
        ghq >= 12 and
        count_mod == 1 and
        not severe_present and
        brs == "Low"
    ):
        return "H"
        
    # Cluster C 
    
    if count_mod == 1 and brs in ["Average", "High"]:
        return "C"
    
    # Cluster D    
    
    if count_mod >= 2 and brs in ["Low", "Average"]:
        return "D"
    
    # Default
    return "Unclassified"