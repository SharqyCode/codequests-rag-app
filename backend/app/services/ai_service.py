from openai import OpenAI
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self, model: str = "gpt-4.1-nano"):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model

    def answer(self, query: str, retrieved_chunks: List[Dict]) -> Dict:
        if not retrieved_chunks:
            return {
                "answer": "I don't know.",
                "sources": [],
                "confidence": 0.0
            }

        context = self._build_context(retrieved_chunks)
        prompt = self._build_prompt(query, context)

        answer = self._call_llm(prompt)

        return {
            "answer": answer,
            "sources": self._extract_sources(retrieved_chunks),
            "confidence": self._estimate_confidence(retrieved_chunks)
        }

    def _build_context(self, chunks: List[Dict]) -> str:
        context_parts = []

        for i, chunk in enumerate(chunks):
            context_parts.append(
                f"[Source {i+1}] ({chunk['source']}):\n{chunk['text']}"
            )

        return "\n\n".join(context_parts)

    def _build_prompt(self, query: str, context: str) -> str:
        return f"""
You are a helpful AI assistant.

Answer the question using ONLY the provided context.
If the answer is not in the context, say "I don't know."

Be concise and clear.

Context:
{context}

Question:
{query}
"""

    def _call_llm(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        return response.choices[0].message.content

    def _extract_sources(self, chunks: List[Dict]) -> List[Dict]:
        return [
            {
                "source": c["source"],
                "document_id": c["document_id"]
            }
            for c in chunks
        ]

    def _estimate_confidence(self, chunks: List[Dict]) -> float:
        if not chunks:
            return 0.0

        avg_score = sum(c["score"] for c in chunks) / len(chunks)
        return max(0.0, min(1.0, 1 - avg_score))