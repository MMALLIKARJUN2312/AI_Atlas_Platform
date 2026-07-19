from pydantic import BaseModel, ConfigDict

class SectorResponse(BaseModel):
    id: int
    segment_number: int
    segment_name: str
    definition: str
    key_germany_companies: str
    ai_adoption: str
    de_market_size: str
    regulatory_complexity: str
    platform_priority: str
    primary_ai_entry_point: str

    model_config = ConfigDict(from_attributes=True)