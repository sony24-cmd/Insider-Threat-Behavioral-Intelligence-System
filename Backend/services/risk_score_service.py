from sqlalchemy.orm import Session

from models.risk_score import RiskScore
from schemas.risk_score import (
    RiskScoreCreate,
    RiskScoreUpdate,
)


def create_risk_score(db: Session, risk: RiskScoreCreate):
    db_risk = RiskScore(**risk.model_dump())
    db.add(db_risk)
    db.commit()
    db.refresh(db_risk)
    return db_risk


def get_risk_score(db: Session, risk_id: int):
    return db.query(RiskScore).filter(RiskScore.id == risk_id).first()


def get_all_risk_scores(db: Session):
    return db.query(RiskScore).all()


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