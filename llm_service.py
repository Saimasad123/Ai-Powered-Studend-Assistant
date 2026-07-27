from __future__ import annotations

import hashlib
import logging

from groq import Groq

from app.core.config import settings


logger = logging.getLogger(__name__)


# =========================================================
# DETERMINISTIC EMBEDDING
# =========================================================

def _deterministic_embedding(
    text: str,
    dimensions: int = 1536
) -> list[float]:
    """
    Development-only deterministic embedding.

    This allows document ingestion and local lexical
    retrieval to work without requiring an embedding API.
    """

    values: list[float] = []

    seed = text.encode("utf-8")
    counter = 0

    while len(values) < dimensions:

        digest = hashlib.sha256(
            seed + counter.to_bytes(4, "big")
        ).digest()

        values.extend(
            (byte / 255.0) * 2.0 - 1.0
            for byte in digest
        )

        counter += 1

    return values[:dimensions]


# =========================================================
# LLM SERVICE
# =========================================================

class LLMService:

    def __init__(self):

        # Use Groq model from backend/.env
        self.model = settings.GROQ_MODEL

        # Create Groq client if API key exists
        self.client = (
            Groq(
                api_key=settings.GROQ_API_KEY
            )
            if settings.GROQ_API_KEY
            else None
        )


    # =====================================================
    # CHECK CONFIGURATION
    # =====================================================

    @property
    def configured(self) -> bool:

        return self.client is not None


    # =====================================================
    # CREATE EMBEDDING
    # =====================================================

    def create_embedding(
        self,
        text: str
    ) -> list[float]:

        """
        Groq does not provide embeddings through
        the standard Groq chat client.

        We use deterministic embeddings for now.
        """

        return _deterministic_embedding(text)


    # =====================================================
    # CHAT / AI GENERATION
    # =====================================================

    def chat(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.2
    ) -> str:

        # Check API key
        if not self.client:

            raise RuntimeError(
                "AI provider is not configured. "
                "Add GROQ_API_KEY to backend/.env."
            )


        try:

            logger.info(
                "Sending AI request to Groq | model=%s",
                self.model
            )


            # Send request to Groq
            response = (
                self.client
                .chat
                .completions
                .create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=1600,
                )
            )


            # Get AI response
            content = (
                response
                .choices[0]
                .message
                .content
            )


            # Make sure response is not empty
            if not content:

                raise RuntimeError(
                    "The Groq AI provider returned "
                    "an empty response."
                )


            logger.info(
                "Groq AI response received successfully"
            )


            return content.strip()


        except Exception as exc:

            logger.exception(
                "Groq chat request failed"
            )

            raise RuntimeError(
                f"Groq API request failed: {exc}"
            ) from exc