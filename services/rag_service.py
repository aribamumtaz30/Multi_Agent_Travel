"""Lightweight RAG-style retriever for travel knowledge.
Uses local knowledge files instead of paid search APIs.
"""
import json
from pathlib import Path
class TravelRAG:
    def retrieve(self, destination):
        path=Path("data/destinations.json")
        if path.exists():
            data=json.loads(path.read_text())
            return data.get(destination.lower(), {})
        return {}
