from pydantic import BaseModel, ConfigDict

class CompanySummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    vendor_name: str
    country: str
    ai_category: str
    company_type: str
    maturity: str
    website: str


class CompanyDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    vendor_name: str
    country: str
    ai_category: str
    segment_tags: str
    germany_presence: str
    company_type: str
    food_beverage_ai_use_case: str
    top_germany_food_beverage_customers: str
    funding: str
    estimated_revenue: str
    maturity: str
    top_deployment_evidence: str
    website: str