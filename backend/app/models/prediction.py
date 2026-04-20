from sqlalchemy import Float, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id", ondelete="CASCADE"), index=True)
    risk_score: Mapped[float] = mapped_column(Float, nullable=False)
    risk_category: Mapped[str] = mapped_column(String(16), nullable=False)
    model_version: Mapped[str] = mapped_column(String(32), nullable=False)
    feature_vector: Mapped[dict] = mapped_column(JSON, nullable=False)
    shap_values: Mapped[list] = mapped_column(JSON, nullable=False)
    base_value: Mapped[float] = mapped_column(Float, nullable=False)

    patient = relationship("Patient", back_populates="predictions")
