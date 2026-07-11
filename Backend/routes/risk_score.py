from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas.risk_score import (
    RiskScoreCreate,
    RiskScoreResponse,
    RiskScoreUpdate,
)
from services import risk_score_service

router = APIRouter(
    prefix="/risk-scores",
    tags=["Risk Scores"],
)


@router.post("/", response_model=RiskScoreResponse)
def create_risk_score(
    risk: RiskScoreCreate,
    db: Session = Depends(get_db),
):
    return risk_score_service.create_risk_score(db, risk)


@router.get("/", response_model=list[RiskScoreResponse])
def get_all_risk_scores(
    db: Session = Depends(get_db),
):
    return risk_score_service.get_all_risk_scores(db)


@router.get("/{risk_id}", response_model=RiskScoreResponse)
def get_risk_score(
    risk_id: int,
    db: Session = Depends(get_db),
):
    risk = risk_score_service.get_risk_score(db, risk_id)

    if risk is None:
        raise HTTPException(
            status_code=404,
            detail="Risk Score not found",
        )

    return risk


@router.put("/{risk_id}", response_model=RiskScoreResponse)
def update_risk_score(
    risk_id: int,
    risk: RiskScoreUpdate,
    db: Session = Depends(get_db),
):
    updated = risk_score_service.update_risk_score(
        db,
        risk_id,
        risk,
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Risk Score not found",
        )

    return updated


@router.delete("/{risk_id}")
def delete_risk_score(
    risk_id: int,
    db: Session = Depends(get_db),
):
    deleted = risk_score_service.delete_risk_score(
        db,
        risk_id,
    )

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Risk Score not found",
        )

    return {
        "message": "Risk Score deleted successfully"
    }