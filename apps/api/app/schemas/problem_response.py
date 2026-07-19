from pydantic import BaseModel

class ProblemResponse(BaseModel):
    problem_id: str
    category: str
    problem_statement: str
    severity: str
    ai_use_case_solution: str
    roi_benchmark: str
    payback_months: str
    regulatory_benefit: str