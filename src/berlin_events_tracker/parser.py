import json
from bs4 import BeautifulSoup

def parse_articles_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    articles = soup.find_all("article", class_="teaser--event")
    results = []
    for art in articles:
        # Title & detail-page link
        title_tag = art.find("h3", class_="title") \
                       .find("a", class_="js-ems-event-teaser-heading")
        title = title_tag.get_text(strip=True)
        detail_url = title_tag["href"]

        # Load the embedded JSON-LD
        ld_json = art.find("script", type="application/ld+json")
        if not ld_json:
            continue
        data = json.loads(ld_json.string)

        # Extract fields
        termin   = data.get("startDate")
        ort      = data.get("location", {}).get("name")
        # price & currency
        offers   = data.get("offers") or []
        if offers:
            preis = f"{offers[0].get('priceCurrency', '')} {offers[0].get('price')}"
            category = offers[0].get("category")
        else:
            preis = None
            category = None
            
        results.append({
            "title":    title,
            "link":     detail_url,
            "termin":   termin,
            "ort":      ort,
            "preis":    preis,
            "category": category,
        })
    return results