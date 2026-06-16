# BigQuery Release Explorer 🚀

A modern web application built using Python Flask, vanilla HTML, CSS, and JavaScript that fetches Google Cloud's BigQuery release notes in real time, parses them into individual updates, and allows you to share them on X (formerly Twitter).

---

## 🌟 Features

* **Real-time Feed Integration:** Pulls release notes directly from Google's official BigQuery Atom feed.
* **Granular Extraction:** Segments compound daily updates into separate cards by type (Features, Issues, Deprecations) using BeautifulSoup.
* **Modern Glassmorphic UI:** Features a high-fidelity responsive dark mode theme with Outfit and Plus Jakarta Sans typography.
* **Search & Filter:** Instantly filter release notes on the client side by category or keywords.
* **Interactive X/Twitter Composer:** Opens an elegant modal featuring:
  * A pre-populated draft based on the release note description.
  * A live circular character counter enforcing the 280-character limit.
  * A real-time mockup preview of the post.
  * A button linking directly to Twitter Web Intents.

---

## ⚙️ Tech Stack

* **Backend:** Python 3.x, Flask, Requests, BeautifulSoup4
* **Frontend:** Vanilla HTML5, Vanilla CSS3 (Custom Properties, Flexbox, Grid), Vanilla JavaScript (ES6+), FontAwesome Icons

---

## 📁 Project Directory Structure

```text
bq-release-notes/
├── app.py                  # Flask application backend
├── templates/
│   └── index.html          # Front-end dashboard template
├── .gitignore              # Project environment exclusions
├── news.txt                # Cached global world news (auxiliary)
├── summary.txt             # Cached world news summary (auxiliary)
└── README.md               # Project documentation (this file)
```

---

## 🚀 Getting Started

### 1. Prerequisites
Make sure Python 3 is installed on your system.

### 2. Install Dependencies
Install the required packages using pip:
```bash
pip install Flask requests beautifulsoup4
```

### 3. Run the Application
Start the Flask development server:
```bash
python app.py
```

By default, the application runs on **`http://localhost:5000`**. Open this URL in your web browser.

---

## 🔌 API Endpoints

### `GET /`
Renders the front-end dashboard interface.

### `GET /api/release-notes`
Fetches the XML feed from Google, parses the XML, and returns a JSON array of parsed updates.

#### Sample JSON Response:
```json
[
  {
    "id": "June_15_2026_0",
    "date": "June 15, 2026",
    "type": "Feature",
    "content_html": "<p>Use Gemini Cloud Assist to analyze your SQL queries...</p>",
    "content_text": "Use Gemini Cloud Assist to analyze your SQL queries...",
    "link": "https://docs.cloud.google.com/bigquery/docs/release-notes#June_15_2026"
  }
]
```

---

## 📝 License
This project is open-source and available under the MIT License.
