
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import re

def audit_website(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        response = requests.get(
            url,
            headers={"User-Agent": "EcommerceSEOMastery/1.0"},
            timeout=15
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.get_text(strip=True) if soup.title else ""

        meta = soup.find(
            "meta",
            attrs={"name": re.compile("^description$", re.I)}
        )
        description = meta.get("content", "") if meta else ""

        h1 = soup.find_all("h1")
        h2 = soup.find_all("h2")

        images = soup.find_all("img")
        missing_alt = sum(
            1 for img in images
            if not img.get("alt", "").strip()
        )

        text = soup.get_text(" ", strip=True)
        word_count = len(text.split())

        canonical_tag = soup.find(
            "link",
            rel=lambda value: value and "canonical" in value
        )
        canonical = canonical_tag.get("href", "") if canonical_tag else ""

        checks = [
            bool(title),
            bool(description),
            30 <= len(title) <= 60,
            120 <= len(description) <= 160,
            len(h1) == 1,
            len(h2) > 0,
            missing_alt == 0,
            bool(canonical),
            word_count >= 300
        ]

        score = round(sum(checks) / len(checks) * 100)

        recommendations = []

        if not title:
            recommendations.append("Add an SEO title.")
        if not description:
            recommendations.append("Add a meta description.")
        if len(h1) != 1:
            recommendations.append("Review the main H1 heading.")
        if missing_alt:
            recommendations.append("Add ALT text to images.")
        if not canonical:
            recommendations.append("Check the canonical URL.")
        if word_count < 300:
            recommendations.append("Add useful original content.")

        if not recommendations:
            recommendations.append("Basic SEO checks look good.")

        return {
            "url": response.url,
            "title": title,
            "description": description,
            "h1": len(h1),
            "h2": len(h2),
            "missing_alt": missing_alt,
            "word_count": word_count,
            "canonical": canonical,
            "score": score,
            "recommendations": recommendations
        }

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def analyze_product(title, description, keyword):

    score = 0
    suggestions = []

    if 30 <= len(title) <= 60:
        score += 30
    else:
        suggestions.append("Improve product title length.")

    if 120 <= len(description) <= 160:
        score += 30
    else:
        suggestions.append("Improve meta description length.")

    if keyword.lower() in title.lower():
        score += 20
    else:
        suggestions.append("Include the target keyword in the title.")

    if keyword.lower() in description.lower():
        score += 20
    else:
        suggestions.append("Include the keyword in the description.")

    return score, suggestions


def keyword_ideas(keyword):

    templates = [
        "best {}",
        "{} online",
        "buy {} online",
        "affordable {}",
        "premium {}",
        "{} price",
        "{} reviews",
        "top rated {}",
        "{} for beginners",
        "{} offers"
    ]

    return [template.format(keyword) for template in templates]
