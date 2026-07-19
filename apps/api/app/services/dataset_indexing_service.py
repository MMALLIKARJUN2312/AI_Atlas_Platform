from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.company_repository import CompanyRepository
from app.repositories.problem_repository import ProblemRepository
from app.repositories.problem_company_mapping_repository import (
    ProblemCompanyMappingRepository,
)
from app.repositories.sector_repository import SectorRepository

from app.rag.builders.company_builder import CompanyDocumentBuilder
from app.rag.builders.problem_builder import ProblemDocumentBuilder
from app.rag.builders.mapping_builder import MappingDocumentBuilder
from app.rag.builders.sector_builder import SectorDocumentBuilder

from app.rag.vector_store.indexing_service import IndexingService

logger = logging.getLogger(__name__)


class DatasetIndexingService:
    """
    Builds the AI Knowledge Base from the relational database.

    Reads all imported entities, converts them into KnowledgeDocuments,
    chunks them, embeds them, and stores them in pgvector.
    """

    def __init__(
        self,
        db: AsyncSession,
        indexing_service: IndexingService,
    ):
        self.db = db

        self.indexing_service = indexing_service

        self.company_repository = CompanyRepository(db)
        self.problem_repository = ProblemRepository(db)
        self.mapping_repository = ProblemCompanyMappingRepository(db)
        self.sector_repository = SectorRepository(db)

        self.company_builder = CompanyDocumentBuilder()
        self.problem_builder = ProblemDocumentBuilder()
        self.mapping_builder = MappingDocumentBuilder()
        self.sector_builder = SectorDocumentBuilder()

    async def index_companies(self) -> int:
        companies = await self.company_repository.find_all()

        documents = [
            self.company_builder.build(company)
            for company in companies
        ]

        await self.indexing_service.index_documents(documents)

        logger.info("Indexed %s companies", len(documents))

        return len(documents)

    async def index_problems(self) -> int:
        problems = await self.problem_repository.find_all()

        documents = [
            self.problem_builder.build(problem)
            for problem in problems
        ]

        await self.indexing_service.index_documents(documents)

        logger.info("Indexed %s problems", len(documents))

        return len(documents)

    async def index_mappings(self) -> int:
        mappings = await self.mapping_repository.find_all()

        documents = [
            self.mapping_builder.build(mapping)
            for mapping in mappings
        ]

        await self.indexing_service.index_documents(documents)

        logger.info("Indexed %s mappings", len(documents))

        return len(documents)

    async def index_sectors(self) -> int:
        sectors = await self.sector_repository.find_all()

        documents = [
            self.sector_builder.build(sector)
            for sector in sectors
        ]

        await self.indexing_service.index_documents(documents)

        logger.info("Indexed %s sectors", len(documents))

        return len(documents)

    async def index_all(self) -> dict[str, int]:
        logger.info("Starting knowledge base indexing")

        companies = await self.index_companies()
        problems = await self.index_problems()
        mappings = await self.index_mappings()
        sectors = await self.index_sectors()

        logger.info("Knowledge base indexing completed")

        return {
            "companies": companies,
            "problems": problems,
            "mappings": mappings,
            "sectors": sectors,
        }