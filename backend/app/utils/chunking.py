import re
from typing import List


class TextChunker:
    def __init__(
        self,
        chunk_size: int = 700,
        overlap_sentences: int = 2
    ):
        self.chunk_size = chunk_size
        self.overlap_sentences = overlap_sentences

    def chunk(self, text: str) -> List[str]:
        text = self._clean_text(text)
        sentences = self._split_into_sentences(text)

        chunks = []
        current_sentences = []
        current_length = 0

        for sentence in sentences:
            sentence_length = len(sentence)

            if current_length + sentence_length > self.chunk_size:
                if current_sentences:
                    chunks.append(" ".join(current_sentences))

                    # overlap
                    current_sentences = current_sentences[-self.overlap_sentences:]
                    current_length = sum(len(s) for s in current_sentences)

            current_sentences.append(sentence)
            current_length += sentence_length

        if current_sentences:
            chunks.append(" ".join(current_sentences))

        print(f"Chunks: {len(chunks)}")
        print(chunks[0])

        return chunks

    def _clean_text(self, text: str) -> str:
        return text.replace("\n", " ").strip()

    def _split_into_sentences(self, text: str) -> List[str]:
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]