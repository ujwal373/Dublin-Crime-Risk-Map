"""
Severity weights for different crime categories.
Edit these values to adjust risk scoring.
"""

SEVERITY_WEIGHTS = {
    # Highest severity - 5
    'homicide': 5,
    'murder': 5,
    'manslaughter': 5,
    'killed': 5,

    # High severity - 4
    'assault': 4,
    'robbery': 4,
    'weapons': 4,
    'firearm': 4,
    'rape': 4,
    'sexual': 4,
    'kidnap': 4,

    # Medium-high severity - 3
    'burglary': 3,
    'aggravated': 3,
    'arson': 3,

    # Medium severity - 2
    'theft': 2,
    'fraud': 2,
    'deception': 2,
    'damage': 2,
    'drugs': 2,

    # Low severity - 1
    'public order': 1,
    'minor': 1,
    'neglect': 1,
    'breach': 1,
}

DEFAULT_WEIGHT = 2

def get_offence_weight(offence_text):
    """
    Return severity weight for an offence based on keyword matching.

    Args:
        offence_text (str): The offence description

    Returns:
        int: Severity weight (1-5)
    """
    if not offence_text:
        return DEFAULT_WEIGHT

    offence_lower = offence_text.lower()

    for keyword, weight in SEVERITY_WEIGHTS.items():
        if keyword in offence_lower:
            return weight

    return DEFAULT_WEIGHT
