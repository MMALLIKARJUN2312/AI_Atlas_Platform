from __future__ import annotations

import logging
from urllib.parse import urlparse

from app.ai.schemas.grounded_llm_response import GroundedLLMResponse
from app.ai.services.llm_service import LLMService

logger = logging.getLogger(__name__)


class DiscoveryVerifier:
    """
    Second-pass verification deciding whether a freshly-discovered company is
    trustworthy enough to write straight to the directory with no human in
    the loop.

    The score is four separately-checkable signals, not one opaque number, so
    a reviewer can see exactly why a candidate did or didn't clear the
    auto-approve bar:

      1. Evidence breadth (max 0.35)   - how many DISTINCT grounded sources
         from the original discovery search mention this company. One source
         could be a fluke; three independent ones rarely are.
      2. Field completeness (max 0.15) - how many of the extracted fields
         (category, use cases, segment tags, website) actually came back
         non-empty from the extraction step.
      3. Website plausibility (max 0.10) - the extracted website resembles a
         real, single domain rather than blank or malformed text.
      4. Independent corroboration (max 0.40) - a SECOND, separate grounded
         web search, issued only for this verification step, that itself
         mentions the company. This is deliberately the largest signal,
         because it is the only one built from evidence outside the original
         discovery search - a hallucinated or coincidental first search can't
         carry a candidate across the line on its own.

    Signals 1-3 cap at 0.60, below the 0.90 auto-approve threshold. That's
    structural, not tuned: no candidate can be auto-stored unless the
    independent corroboration search in step 4 actually runs and actually
    confirms the company - however convincing the original search looked.

    If the corroboration search is unavailable (e.g. the provider's grounding
    quota is exhausted), the candidate simply falls back to the existing
    human-review queue rather than being blocked or, worse, auto-approved on
    unverified evidence.
    """

    def __init__(self, llm: LLMService):
        self.llm = llm

    def score(self, *, name: str, evidence: list[dict], extracted: dict, website: str) -> tuple[float, bool]:
        breadth = self._evidence_breadth_score(evidence)
        completeness = self._completeness_score(extracted, website)
        website_score = self._website_score(website)
        corroboration, verified = self._independent_corroboration(name, website)

        confidence = round(min(breadth + completeness + website_score + corroboration, 1.0), 4)
        return confidence, verified

    @staticmethod
    def _evidence_breadth_score(evidence: list[dict]) -> float:
        distinct_sources = len({item.get("url") for item in evidence if item.get("url")})
        if distinct_sources >= 3:
            return 0.35
        if distinct_sources == 2:
            return 0.25
        if distinct_sources == 1:
            return 0.15
        return 0.0

    @staticmethod
    def _completeness_score(extracted: dict, website: str) -> float:
        fields = [extracted.get("category"), extracted.get("use_cases"), extracted.get("segment_tags"), website]
        present = sum(1 for field in fields if str(field or "").strip())
        return round(0.15 * (present / len(fields)), 4)

    @staticmethod
    def _website_score(website: str) -> float:
        website = (website or "").strip()
        if not website:
            return 0.0
        domain = urlparse(website if website.startswith("http") else f"https://{website}").netloc
        return 0.10 if "." in domain and " " not in domain else 0.0

    def _independent_corroboration(self, name: str, website: str) -> tuple[float, bool]:
        query = (
            f'Confirm whether "{name}" is a real, currently operating company. '
            "Briefly state what it does and its official website if known."
        )
        try:
            grounded = self.llm.search(query)
        except Exception as exc:
            logger.info("Independent verification search unavailable for %r: %s", name, exc)
            return 0.0, False

        if not grounded.text or name.casefold() not in grounded.text.casefold():
            return 0.0, False

        domain_matched = self._shares_domain(website, grounded)
        return (0.40 if domain_matched else 0.20), True

    @staticmethod
    def _shares_domain(website: str, grounded: GroundedLLMResponse) -> bool:
        website = (website or "").strip()
        if not website:
            return False
        target = urlparse(website if website.startswith("http") else f"https://{website}").netloc.removeprefix("www.")
        if not target:
            return False
        for chunk in grounded.chunks:
            source_domain = urlparse(chunk.uri).netloc.removeprefix("www.")
            if source_domain and source_domain == target:
                return True
        return False
