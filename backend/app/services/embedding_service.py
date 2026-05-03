from openai import OpenAI
from typing import List
import time
import os
from dotenv import load_dotenv

load_dotenv()


class EmbeddingService:
    def __init__(self, model: str = "text-embedding-3-small"):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model

    def embed_text(self, text: str) -> List[float]:
        text = self._clean_text(text)

        print(f"embedding.text: {text}")
        response = self.client.embeddings.create(
            model=self.model,
            input=text
        )
        return response.data[0].embedding

    def embed_batch(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        texts = [self._clean_text(t) for t in texts]

        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            embeddings = self._embed_with_retry(batch)
            all_embeddings.extend(embeddings)


        return all_embeddings

    def _embed_with_retry(self, batch: List[str], retries: int = 3) -> List[List[float]]:
        for attempt in range(retries):
            try:
                response = self.client.embeddings.create(
                    model=self.model,
                    input=batch
                )
                # print([item.embedding for item in response.data])
                return [item.embedding for item in response.data]

            except Exception as e:
                if attempt == retries - 1:
                    raise 

                wait_time = 2 ** attempt
                print(f"Embedding failed. Retrying in {wait_time}s...")
                time.sleep(wait_time)

        raise RuntimeError("Unexpected error: retry loop exited without returning or raising")

    def _clean_text(self, text: str) -> str:
        return text.replace("\n", " ").strip()