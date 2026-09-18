from __future__ import annotations

from typing import Any

import requests
from bs4 import BeautifulSoup


class WebScraper:
    """Public-page scraper restricted to non-login pages with simple HTTP checks."""

    def fetch(self, url: str) -> dict[str, Any]:
        try:
            response = requests.get(url, timeout=12)
            response.raise_for_status()
        except Exception:
            return {"title": "N/A", "content": "", "status": "unavailable"}

        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.get_text(strip=True) if soup.title else "N/A"
        text = " ".join(soup.stripped_strings[:400])
        return {"title": title, "content": text, "status": "ok"}
