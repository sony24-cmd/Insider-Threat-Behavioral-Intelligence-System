from sqlalchemy.orm import Session

from models.risk_score import RiskScore


def save_risk_score(
    db: Session,
    employee_id: int,
    confidence: float,
):
    """
    Save AI-generated risk score.
    """

    score = round(confidence * 100, 2)

    if score >= 70:
        level = "High"
    elif score >= 40:
        level = "Medium"
    else:
        level = "Low"

    risk = RiskScore(
        employee_id=employee_id,
        risk_score=score,
        risk_level=level,
        remarks="Generated automatically by AI",
    )

    db.add(risk)
    db.commit()
    db.refresh(risk)

    return risk