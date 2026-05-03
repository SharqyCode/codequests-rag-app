from openai import OpenAI
from typing import List, Dict
import os
from dotenv import load_dotenv
from app.utils.logger import setup_logger

load_dotenv()


logger = setup_logger("ai_service")


class AIService:

    def __init__(self, model="gpt-4.1-mini"):
        self.client = OpenAI()
        self.model = model

    def answer(self, query, retrieved_chunks):
        logger.info(f"AI answering query: {query[:100]}")

        if not retrieved_chunks:
            logger.warning("No chunks provided to AI")
            return {
                "answer": "I don't know.",
                "sources": [],
                "confidence": 0.0
            }

        try:
            context = self._build_context(retrieved_chunks)
            prompt = self._build_prompt(query, context)

            logger.info(f"Prompt length: {len(prompt)} chars")

            answer = self._call_llm(prompt)

            logger.info("AI response generated successfully")

            return {
                "answer": answer,
                "sources": self._extract_sources(retrieved_chunks),
                "confidence": self._estimate_confidence(retrieved_chunks)
            }

        except Exception as e:
            logger.error(f"AI generation failed: {str(e)}", exc_info=True)

            return {
                "answer": "Something went wrong while generating the answer.",
                "sources": [],
                "confidence": 0.0
            }