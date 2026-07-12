from sqlalchemy.orm import Session

from models.risk_score import RiskScore
from schemas.risk_score import (
    RiskScoreCreate,
    RiskScoreUpdate,
)


# ==========================================
# Create Risk Score (Manual API)
# ==========================================
def create_risk_score(
    db: Session,
    risk: RiskScoreCreate,
):
    db_risk = RiskScore(**risk.model_dump())

    db.add(db_risk)
    db.commit()
    db.refresh(db_risk)

    return db_risk


# ==========================================
# Create Risk Score (AI Prediction)
# ==========================================
def save_ai_risk_score(
    db: Session,
    employee_id: int,
    confidence: float,
):
    """
    Save AI prediction as Risk Score.
    confidence is already a percentage (0-100).
    """

    score = round(confidence, 2)

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
        remarks="Generated automatically by AI Model",
    )

    db.add(risk)
    db.commit()
    db.refresh(risk)

    return risk


# ==========================================
# Get Risk Score By ID
# ==========================================
def get_risk_score(
    db: Session,
    risk_id: int,
):
    return (
        db.query(RiskScore)
        .filter(RiskScore.id == risk_id)
        .first()
    )


# ==========================================
# Get All Risk Scores
# ==========================================
def get_all_risk_scores(
    db: Session,
):
    return db.query(RiskScore).all()


# ==========================================
# Update Risk Score
# ==========================================
def update_risk_score(
    db: Session,
    risk_id: int,
    risk: RiskScoreUpdate,
):
    db_risk = (
        db.query(RiskScore)
        .filter(RiskScore.id == risk_id)
        .first()
    )

    if not db_risk:
        return None

    update_data = risk.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_risk, key, value)

    db.commit()
    db.refresh(db_risk)

    return db_risk


# ==========================================
# Delete Risk Score
# ==========================================
def delete_risk_score(
    db: Session,
    risk_id: int,
):
    db_risk = (
        db.query(RiskScore)
        .filter(RiskScore.id == risk_id)
        .first()
    )

    if not db_risk:
        return None

    db.delete(db_risk)
    db.commit()

    return db_risk