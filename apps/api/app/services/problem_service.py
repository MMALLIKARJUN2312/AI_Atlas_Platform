from app.repositories.company_repository import CompanyRepository
from app.repositories.problem_company_mapping_repository import (
    ProblemCompanyMappingRepository,
)
from app.repositories.problem_repository import ProblemRepository
from app.schemas.problem_response import ProblemResponse


class ProblemService:
    def __init__(self, company_repository: CompanyRepository, mapping_repository: ProblemCompanyMappingRepository, problem_repository: ProblemRepository):
        self.company_repository = company_repository
        self.mapping_repository = mapping_repository
        self.problem_repository = problem_repository

    async def get_company_problems(self, company_id: int) -> list[ProblemResponse]:

        company = await self.company_repository.find_by_id(company_id)

        if company is None:
            return []

        vendor_name = company.vendor_name

        for suffix in [" SE & Co KG", " GmbH", " AG", " SE", " Inc.", " Ltd."]:
            vendor_name = vendor_name.replace(suffix, "")

        mappings = await self.mapping_repository.find_by_vendor_name(
            vendor_name.strip()
        )

        response: list[ProblemResponse] = []

        for mapping in mappings:
            problem = await self.problem_repository.find_by_problem_statement(
                mapping.problem_statement
            )

            if problem is None:
                continue

            response.append(
                ProblemResponse(
                    problem_id=problem.problem_id,
                    category=problem.category,
                    problem_statement=problem.problem_statement,
                    severity=problem.severity,
                    ai_use_case_solution=problem.ai_use_case_solution,
                    roi_benchmark=mapping.roi_benchmark,
                    payback_months=mapping.payback_months,
                    regulatory_benefit=mapping.regulatory_benefit,
                )
            )

        return response