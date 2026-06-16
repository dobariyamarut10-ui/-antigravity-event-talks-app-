import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, render_template

app = Flask(__name__)

FEED_URL = "https://docs.cloud.google.com/feeds/bigquery-release-notes.xml"
NAMESPACE = {"atom": "http://www.w3.org/2005/Atom"}

def parse_release_notes():
    try:
        response = requests.get(FEED_URL, timeout=15)
        response.raise_for_status()
    except Exception as e:
        # Return empty list or fallback error structure if feed fetching fails
        print(f"Error fetching feed: {e}")
        return None

    try:
        root = ET.fromstring(response.content)
        entries = []
        
        # Parse each entry in the Atom feed
        for entry_node in root.findall("atom:entry", NAMESPACE):
            title_node = entry_node.find("atom:title", NAMESPACE)
            date = title_node.text.strip() if title_node is not None else "Unknown Date"
            
            link_node = entry_node.find("atom:link[@rel='alternate']", NAMESPACE)
            if link_node is None:
                link_node = entry_node.find("atom:link", NAMESPACE)
            link = link_node.attrib.get("href", "") if link_node is not None else ""
            
            content_node = entry_node.find("atom:content", NAMESPACE)
            if content_node is not None and content_node.text:
                html_content = content_node.text
                soup = BeautifulSoup(html_content, "html.parser")
                
                # BigQuery release notes usually group items by <h3> headers
                # (e.g. <h3>Feature</h3>, <h3>Issue</h3>) followed by description tags
                h3s = soup.find_all("h3")
                
                if h3s:
                    for idx, h3 in enumerate(h3s):
                        item_type = h3.text.strip()
                        
                        # Gather sibling tags until next h3
                        desc_elements = []
                        sibling = h3.next_sibling
                        while sibling and sibling.name != "h3":
                            if sibling.name:  # Avoid empty text nodes
                                desc_elements.append(str(sibling))
                            sibling = sibling.next_sibling
                        
                        desc_html = "".join(desc_elements).strip()
                        # Extract plain text for tweet composer
                        desc_soup = BeautifulSoup(desc_html, "html.parser")
                        desc_text = desc_soup.get_text().strip()
                        
                        item_id = f"{date.replace(' ', '_').replace(',', '')}_{idx}"
                        
                        entries.append({
                            "id": item_id,
                            "date": date,
                            "type": item_type,
                            "content_html": desc_html,
                            "content_text": desc_text,
                            "link": link
                        })
                else:
                    # Fallback if no h3 tags are found in the entry
                    desc_text = soup.get_text().strip()
                    item_id = f"{date.replace(' ', '_').replace(',', '')}_0"
                    entries.append({
                        "id": item_id,
                        "date": date,
                        "type": "General",
                        "content_html": html_content,
                        "content_text": desc_text,
                        "link": link
                    })
        return entries
    except Exception as e:
        print(f"Error parsing feed XML: {e}")
        return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/release-notes")
def get_release_notes():
    notes = parse_release_notes()
    if notes is None:
        return jsonify({"error": "Failed to fetch or parse release notes"}), 500
    return jsonify(notes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
