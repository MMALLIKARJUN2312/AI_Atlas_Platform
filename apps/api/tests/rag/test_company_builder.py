from datetime import datetime, UTC

from app.database.models.company import Company
from app.rag.builders.company_builder import CompanyDocumentBuilder


def test_company_document_builder():
    company = Company(
        id=1,
        vendor_name="Krones",
        country="Germany",
        ai_category="Computer Vision",
        segment_tags="Packaging",
        germany_presence="Yes",
        company_type="Enterprise",
        food_beverage_ai_use_case="Quality Inspection",
        top_germany_food_beverage_customers="Nestlé",
        funding="Public",
        estimated_revenue="€5B",
        maturity="5",
        top_deployment_evidence="Case Study",
        website="https://krones.com",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    builder = CompanyDocumentBuilder()

    document = builder.build(company)

    assert document.document_id == "company:1"
    assert document.document_type == "company"
    assert document.title == "Krones"
    assert "Quality Inspection" in document.content
    assert document.metadata["country"] == "Germany"
    assert document.metadata["website"] == "https://krones.com"