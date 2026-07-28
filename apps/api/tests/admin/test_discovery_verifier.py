from app.admin.discovery_verifier import DiscoveryVerifier
from app.ai.schemas.grounded_llm_response import GroundedLLMResponse, GroundingChunk


class StubLLM:
    """Stands in for LLMService.search for the verifier's corroboration step."""

    def __init__(self, response: GroundedLLMResponse | None = None, error: Exception | None = None):
        self._response = response
        self._error = error
        self.queries: list[str] = []

    def search(self, query: str) -> GroundedLLMResponse:
        self.queries.append(query)
        if self._error:
            raise self._error
        return self._response


def _extracted(**overrides):
    base = {"category": "Sorting AI", "use_cases": "Optical sorting", "segment_tags": "2"}
    base.update(overrides)
    return base


def test_evidence_breadth_scores_by_distinct_source_count():
    verifier = DiscoveryVerifier(StubLLM(GroundedLLMResponse(text="", model="fake")))
    assert verifier._evidence_breadth_score([]) == 0.0
    assert verifier._evidence_breadth_score([{"url": "https://a.com"}]) == 0.15
    assert verifier._evidence_breadth_score([{"url": "https://a.com"}, {"url": "https://b.com"}]) == 0.25
    assert verifier._evidence_breadth_score(
        [{"url": "https://a.com"}, {"url": "https://b.com"}, {"url": "https://c.com"}]
    ) == 0.35
    # Duplicate URLs across evidence items don't count twice.
    assert verifier._evidence_breadth_score([{"url": "https://a.com"}, {"url": "https://a.com"}]) == 0.15


def test_completeness_score_scales_with_present_fields():
    verifier = DiscoveryVerifier(StubLLM())
    assert verifier._completeness_score(_extracted(), "https://acme.ai") == 0.15
    assert verifier._completeness_score(_extracted(category=""), "https://acme.ai") == round(0.15 * 3 / 4, 4)
    assert verifier._completeness_score({}, "") == 0.0


def test_website_score_requires_a_plausible_domain():
    verifier = DiscoveryVerifier(StubLLM())
    assert verifier._website_score("https://acme.ai") == 0.10
    assert verifier._website_score("acme.ai") == 0.10
    assert verifier._website_score("") == 0.0
    assert verifier._website_score("not a url") == 0.0


def test_corroboration_returns_zero_when_search_unavailable():
    verifier = DiscoveryVerifier(StubLLM(error=Exception("429 RESOURCE_EXHAUSTED")))
    score, verified = verifier._independent_corroboration("Acme AI", "https://acme.ai")
    assert score == 0.0
    assert verified is False


def test_corroboration_returns_zero_when_name_not_mentioned():
    verifier = DiscoveryVerifier(StubLLM(GroundedLLMResponse(text="Nothing relevant here.", model="fake")))
    score, verified = verifier._independent_corroboration("Acme AI", "https://acme.ai")
    assert score == 0.0
    assert verified is False


def test_corroboration_gives_partial_credit_without_domain_match():
    llm = StubLLM(GroundedLLMResponse(
        text="Acme AI is a real robotics company.",
        model="fake",
        chunks=[GroundingChunk(uri="https://unrelated-directory.example/acme", title="Listing")],
    ))
    verifier = DiscoveryVerifier(llm)
    score, verified = verifier._independent_corroboration("Acme AI", "https://acme.ai")
    assert score == 0.20
    assert verified is True


def test_corroboration_gives_full_credit_with_matching_domain():
    llm = StubLLM(GroundedLLMResponse(
        text="Acme AI is a real robotics company, official site acme.ai.",
        model="fake",
        chunks=[GroundingChunk(uri="https://www.acme.ai/about", title="Acme AI - About")],
    ))
    verifier = DiscoveryVerifier(llm)
    score, verified = verifier._independent_corroboration("Acme AI", "https://acme.ai")
    assert score == 0.40
    assert verified is True


def test_base_signals_alone_cannot_reach_auto_approve_threshold():
    """
    Structural guarantee: without a successful, corroborating independent
    search, a candidate cannot cross the 0.90 auto-approve threshold no
    matter how strong evidence breadth, completeness, and website
    plausibility are.
    """
    verifier = DiscoveryVerifier(StubLLM(error=Exception("quota exceeded")))
    confidence, verified = verifier.score(
        name="Acme AI",
        evidence=[{"url": "https://a.com"}, {"url": "https://b.com"}, {"url": "https://c.com"}],
        extracted=_extracted(),
        website="https://acme.ai",
    )
    assert verified is False
    assert confidence == 0.60
    assert confidence < 0.90


def test_full_score_with_domain_matched_corroboration_reaches_maximum():
    llm = StubLLM(GroundedLLMResponse(
        text="Acme AI is a real robotics company, official site acme.ai.",
        model="fake",
        chunks=[GroundingChunk(uri="https://acme.ai", title="Acme AI")],
    ))
    verifier = DiscoveryVerifier(llm)
    confidence, verified = verifier.score(
        name="Acme AI",
        evidence=[{"url": "https://a.com"}, {"url": "https://b.com"}, {"url": "https://c.com"}],
        extracted=_extracted(),
        website="https://acme.ai",
    )
    assert verified is True
    assert confidence == 1.0
