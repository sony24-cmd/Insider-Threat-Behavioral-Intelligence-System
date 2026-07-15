from sqlalchemy.orm import Session

from models.risk_score import RiskScore
from schemas.risk_score import (
    RiskScoreCreate,
    RiskScoreUpdate,
)


# ==========================================
# Create Risk Score
# ==========================================

def create_risk_score(
    db: Session,
    risk_score: RiskScoreCreate,
):

    db_risk = RiskScore(
        employee_id=risk_score.employee_id,
        risk_score=risk_score.risk_score,
        risk_level=risk_score.risk_level,
        remarks=risk_score.remarks,
    )

    db.add(db_risk)
    db.commit()
    db.refresh(db_risk)

    return db_risk


# ==========================================
# Save AI Risk Score
# ==========================================

def save_ai_risk_score(
    db: Session,
    employee_id: int,
    confidence: float,
):

    score = round(confidence, 2)

    if score >= 80:
        level = "Critical"
    elif score >= 60:
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
# Get All
# ==========================================

def get_all_risk_scores(db: Session):
    return db.query(RiskScore).all()


# ==========================================
# Get One
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
# Update
# ==========================================

def update_risk_score(
    db: Session,
    risk_id: int,
    risk_update: RiskScoreUpdate,
):

    risk = (
        db.query(RiskScore)
        .filter(RiskScore.id == risk_id)
        .first()
    )

    if not risk:
        return None

    for key, value in risk_update.model_dump(
        exclude_unset=True
    ).items():
        setattr(risk, key, value)

    db.commit()
    db.refresh(risk)

    return risk


# ==========================================
# Delete
# ==========================================

def delete_risk_score(
    db: Session,
    risk_id: int,
):

    risk = (
        db.query(RiskScore)
        .filter(RiskScore.id == risk_id)
        .first()
    )

    if not risk:
        return None

    db.delete(risk)
    db.commit()

    return risk