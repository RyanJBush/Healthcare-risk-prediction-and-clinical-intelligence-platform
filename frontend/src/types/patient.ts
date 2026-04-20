export type RiskCategory = "low" | "medium" | "high";

export type Patient = {
  id: number;
  external_id: string;
  age: number;
  sex: string;
  systolic_bp: number;
  diastolic_bp: number;
  cholesterol: number;
  bmi: number;
  hba1c: number;
};

export type PredictionSummary = {
  prediction_id: number;
  patient_id: number;
  risk_score: number;
  risk_category: RiskCategory;
  model_version: string;
};

export type FeatureContribution = {
  feature: string;
  value: number;
  contribution: number;
};

export type Explanation = {
  patient_id: number;
  prediction_id: number;
  model_version: string;
  base_value: number;
  contributions: FeatureContribution[];
};
