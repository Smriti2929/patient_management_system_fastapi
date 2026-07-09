def calculate_bmi(weight: float, height: float) -> float:
    return round(weight / (height ** 2), 2)


def get_verdict(bmi: float) -> str:
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"