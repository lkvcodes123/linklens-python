# LinkLens — Python edition

An educational phishing URL checker with a Python Flask backend and an HTML/CSS/JavaScript interface.

## Start locally

Requires Python 3.10 or later.

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

On Windows, activate using `.venv\Scripts\activate` instead.

Open http://127.0.0.1:8000. Open the website through this server, not by double-clicking the HTML file.

## Files

- `analyzer.py`: URL parsing, validation, and weighted heuristic rules.
- `app.py`: Flask server and POST `/api/check` endpoint.
- `static/`: website interface; JavaScript calls the Python API.
- `test_analyzer.py`, `test_api.py`: standard-library unittest tests.

## Tests

```sh
python -m unittest discover -v
```

## API

Send POST `/api/check` with `Content-Type: application/json` and a body such as:

```json
{"url":"https://example.com"}
```

The response includes `host`, `notes`, `score`, and `https`. Invalid input returns a JSON error with HTTP 400; unsupported content types return 415, and oversized requests return 413.

Scores are illustrative heuristic weights, not probabilities: 0 means no obvious URL warning signs, 1–3 means caution, and 4+ means strong warning signs. The checker detects clues including misleading brand names, user information before @, HTTP, IP addresses, internationalized domains, shorteners, and apparent downloads.

## Privacy and limitations

Unlike the original browser-only version, this edition sends submitted URLs to the Python server. The application does not persist them or fetch the destination. Hosting providers may have their own request logging. Do not submit URLs containing passwords or private tokens to an untrusted deployment.

This is not a malware scanner or a guarantee of safety. It does not inspect page content, certificates, redirects, or live threat databases. False positives and false negatives are possible. The rules have not been validated against a labeled phishing dataset.

## GitHub and hosting

Upload this folder's contents to a GitHub repository. Do not upload `.venv`, `.env`, or credentials. GitHub Pages cannot run this Python backend; deploy with a Python-compatible host and a production WSGI server. The included Flask development server is for local use.

This download does not replace the previously published browser-only website.

## Attribution

Initial implementation was generated with OpenAI Codex from the project owner's requirements. Describe your own contributions accurately and follow any course AI-use rules.
