from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class OCRResult:
    text: str
    page_count: int | None
    language: str | None
    confidence: float | None
    provider: str


class OCRProvider(Protocol):
    """Switchable OCR boundary. No OCR engine is bundled or claimed as active."""
    def extract(self, document: bytes, mime_type: str) -> OCRResult: ...


class EmbeddingProvider(Protocol):
    """Configurable multilingual embedding boundary (e5, BGE-M3, or later)."""
    def embed(self, texts: list[str]) -> list[list[float]]: ...


class RerankerProvider(Protocol):
    """Configurable cross-encoder boundary; must be backed by a chosen model."""
    def rank(self, query: str, candidates: list[str]) -> list[float]: ...


class LLMProvider(Protocol):
    """Generation boundary. Registry/version facts must never come from this."""
    def complete(self, prompt: str, context: str) -> str: ...


class RegistryProvider(Protocol):
    """Only an authoritative, dated registry adapter can verify standards."""
    def lookup(self, standard_number: str, snapshot_date: str) -> dict | None: ...


class DemoOCRProvider:
    def extract(self, document: bytes, mime_type: str) -> OCRResult:
        raise RuntimeError("OCR provider is not configured; no text has been extracted.")


class UnconfiguredRegistryProvider:
    def lookup(self, standard_number: str, snapshot_date: str) -> dict | None:
        return None
