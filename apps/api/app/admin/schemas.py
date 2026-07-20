from pydantic import BaseModel, Field


class DiscoveryRequest(BaseModel):
    sector: str = Field(min_length=1, max_length=255)
    country: str = Field(min_length=1, max_length=100)


class Evidence(BaseModel):
    source: str
    snippet: str
    url: str


class CandidateResponse(BaseModel):
    id: int
    name: str
    country: str
    category: str
    segment_tags: str
    use_cases: str
    website: str
    evidence: list[Evidence]
    confidence_score: float
    status: str

    model_config = {"from_attributes": True}


class CompanyWrite(BaseModel):
    vendor_name: str
    country: str
    ai_category: str
    segment_tags: str
    germany_presence: str = ""
    company_type: str = "NewCo"
    food_beverage_ai_use_case: str
    top_germany_food_beverage_customers: str = ""
    funding: str = "Not disclosed"
    estimated_revenue: str = "Not disclosed"
    maturity: str = "Unknown"
    top_deployment_evidence: str = ""
    website: str
