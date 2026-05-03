from fastapi import UploadFile
from pypdf import PdfReader
import io
import re

class FileParser:
    def parse(self, file: UploadFile) -> str:
        file.file.seek(0)

        ext = self._get_extension(file.filename)

        if ext == "txt":
            text = self._parse_text(file)
        elif ext == "md":
            text = self._parse_md(file)
        elif ext == "pdf":
            text = self._parse_pdf(file)
        elif ext == "json":
            text = self._parse_json(file)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

        return self._clean_text(text)

    def _get_extension(self, filename: str) -> str:
        return filename.lower().split(".")[-1]

    def _parse_text(self, file: UploadFile) -> str:
        content = file.file.read()

        try:
            return content.decode("utf-8")
        except UnicodeDecodeError:
            return content.decode("latin-1")

    def _parse_pdf(self, file: UploadFile) -> str:
        pdf_bytes = file.file.read()
        reader = PdfReader(io.BytesIO(pdf_bytes))

        text_parts = []

        for page in reader.pages:
            try:
                text = page.extract_text()
                if text:
                    text_parts.append(text)
                if not text:
                    print("Empty page detected")
            except Exception as e:
                print(f"Failed to parse page: {e}")

        return "\n".join(text_parts)
    
    def _parse_md(self, file: UploadFile) -> str:
        content = file.file.read().decode("utf-8", errors="ignore")

        # Remove code blocks
        content = re.sub(r"```.*?```", "", content, flags=re.DOTALL)

        # Remove inline code
        content = re.sub(r"`.*?`", "", content)

        # Remove markdown symbols
        content = re.sub(r"^[#>\-*]+", "", content, flags=re.MULTILINE)

        # Remove links but keep text [text](url) -> text
        content = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", content)

        return content.strip()

    def _parse_json(self, file: UploadFile) -> str:
        import json

        content = file.file.read().decode("utf-8", errors="ignore")
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            return ""

        def extract_text(obj):
            if isinstance(obj, dict):
                return " ".join(extract_text(v) for v in obj.values())
            elif isinstance(obj, list):
                return " ".join(extract_text(i) for i in obj)
            elif isinstance(obj, str):
                return obj
            else:
                return ""

        return extract_text(data)
    
    def _clean_text(self, text: str) -> str:
        text = text.replace("\r", " ")
        text = re.sub(r"\n\s*\n", "\n\n", text)  # collapse empty lines
        return text.strip()