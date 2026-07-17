import logging 

from sqlalchemy.ext.asyncio import AsyncSession

from app.ingestion.constants import (COMPANIES_CSV, PROBLEMS_CSV, MAPPINGS_CSV, SECTORS_CSV)
from app.ingestion.readers import read_csv
from app.ingestion.validators import validate_dataframe

from app.models.company import Company
from app.models.problem import Problem
from app.models.problem_company_mapping import ProblemCompanyMapping
from app.models.sector import Sector

from app.repositories.company_repository import CompanyRepository
from app.repositories.problem_repository import ProblemRepository
from app.repositories.problem_company_mapping_repository import ProblemCompanyMappingRepository
from app.repositories.sector_repository import SectorRepository

logger = logging.getLogger(__name__)

class DatasetImportService:
    def __init__(self, db : AsyncSession):
        self.db = db 
        
        self.company_repository = CompanyRepository(db)
        self.problem_repository = ProblemRepository(db)
        self.mapping_repository = ProblemCompanyMappingRepository(db)
        self.sector_repository = SectorRepository(db)
    
    async def import_companies(self) -> int:
        logger.info("Importing germany companies dataset")
        
        dataframe = read_csv(COMPANIES_CSV)
        
        validate_dataframe(dataframe, [
            "#", "Vendor Name", "Country", "AI Category", "Seg Tags", "Germany Presence", "Company Type", "F&B AI Use Case",
            "Top Germany F&B Customers", "Funding", "Est. Revenue", "Maturity", "Top Deployment Evidence", "Website"
        ])
        
        companies : list[Company] = []
        
        for _, row in dataframe.iterrows():
            companies.append(
                Company(
                    vendor_name=row["Vendor Name"],
                    country=row["Country"],
                    ai_category=row["AI Category"],
                    segment_tags=row["Seg Tags"],
                    germany_presence=row["Germany Presence"],
                    company_type=row["Company Type"],
                    food_beverage_ai_use_case=row["F&B AI Use Case"],
                    top_germany_food_beverage_customers=row["Top Germany F&B Customers"],
                    funding=row["Funding"],
                    estimated_revenue=row["Est. Revenue"],
                    maturity=row["Maturity"],
                    top_deployment_evidence=row["Top Deployment Evidence"],
                    website=row["Website"]
                )
            )
            
        result = await self.company_repository.bulk_insert_dataset(companies)
        
        logger.info("Imported %s germany companies", len(companies))
        
        return result
    
    async def import_problems(self) -> int:
        logger.info("Importing germany problems dataset")
        
        dataframe = read_csv(PROBLEMS_CSV)
        
        validate_dataframe(dataframe, [
            "Prob ID", "Category", "Problem Statement", "Seg Tags", "VC Stage", "Severity", "AI Use Case Solution",
            "Affected Germany Companies", "Financial Impact (€)", "Regulatory Trigger", "Problem Type"
        ])
    
        problems : list[Problem] = []
        
        for _, row in dataframe.iterrows():
            problems.append(
                Problem(
                    problem_id=row["Prob ID"],
                    category=row["Category"],
                    problem_statement=row["Problem Statement"],
                    segment_tags=row["Seg Tags"],
                    vc_stage=row["VC Stage"],
                    severity=row["Severity"],
                    ai_use_case_solution=row["AI Use Case Solution"],
                    affected_germany_companies=row["Affected Germany Companies"],
                    financial_impact=row["Financial Impact (€)"],
                    regulatory_trigger=row["Regulatory Trigger"],
                    problem_type=row["Problem Type"]
                ))        
        
        result = await self.problem_repository.bulk_insert_dataset(problems)
        
        logger.info("Imported %s germany problems", len(problems))
        
        return result
    
    async def import_mappings(self) -> int:
        logger.info("Importing problem company mappings dataset")
        
        dataframe =read_csv(MAPPINGS_CSV)
        
        validate_dataframe(dataframe, [
             "#", "Problem Statement", "Seg Tags", "VC Stage", "AI Solution 1", "AI Solution 2", "AI Solution 3",
             "Germany Vendors (ranked)", "ROI Benchmark", "Payback (months)", "Regulatory Benefit"     
        ])
        
        mappings : list[ProblemCompanyMapping] = []
        
        for _, row in dataframe.iterrows():
            mappings.append(
                ProblemCompanyMapping(
                    sequence_number=int(row["#"]),
                    problem_statement=row["Problem Statement"],
                    segment_tags=row["Seg Tags"],
                    vc_stage=row["VC Stage"],
                    ai_solution_1=row["AI Solution 1"],
                    ai_solution_2=row["AI Solution 2"],
                    ai_solution_3=row["AI Solution 3"],
                    germany_vendors=row["Germany Vendors (ranked)"],
                    roi_benchmark=row["ROI Benchmark"],
                    payback_months=row["Payback (months)"],
                    regulatory_benefit=row["Regulatory Benefit"]
                )
            )

        result = await self.mapping_repository.bulk_insert_dataset(mappings)
        
        logger.info("Imported %s problem company mappings", len(mappings))
        
        return result
        
    async def import_sectors(self) -> int:
        logger.info("Importing sector reference dataset")
        
        dataframe = read_csv(SECTORS_CSV)
        
        validate_dataframe(dataframe, [
            "Seg No.", "Segment Name", "Definition", "Key Germany Companies", "AI Adoption", "DE Market Size",
            "Regulatory Complexity", "Platform Priority", "Primary AI Entry Point"
        ])
        
        sectors : list[Sector] = []
        
        for _, row in dataframe.iterrows():
            sectors.append(
                Sector(
                    segment_number=int(row["Seg No."]),
                    segment_name=row["Segment Name"],
                    definition=row["Definition"],
                    key_germany_companies=row["Key Germany Companies"],
                    ai_adoption=row["AI Adoption"],
                    de_market_size=row["DE Market Size"],
                    regulatory_complexity=row["Regulatory Complexity"],
                    platform_priority=row["Platform Priority"],
                    primary_ai_entry_point=row["Primary AI Entry Point"]
                ))
            
        result = await self.sector_repository.bulk_insert_dataset(sectors)
        
        logger.info("Imported %s sectors", len(sectors))
        
        return result
        
    async def import_all(self) -> dict:
        logger.info("Starting dataset import")
        
        try:            
            companies = await self.import_companies()
            problems = await self.import_problems()
            mappings = await self.import_mappings()
            sectors = await self.import_sectors()
            
            await self.db.commit()
            
            logger.info("Dataset import completed successfully")
        
            return {
                "companies" : companies,
                "problems" : problems,
                "mappings" : mappings,
                "sectors" : sectors
            }
        except Exception:
            logger.exception("Dataset import failed. Rolling back transaction.")
            
            await self.db.rollback()
            raise