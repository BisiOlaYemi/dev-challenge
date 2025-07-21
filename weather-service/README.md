# Weather Service

## Setup & Run Instructions

These steps will get the app running locally. Please follow them in order:

### 1. Clone the repository (if you haven't already)
```bash
git clone <repo-url>
cd weather-service
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the FastAPI app
```bash
uvicorn main:app --reload
```

- The API will be available at: http://127.0.0.1:8000
- Interactive docs: http://127.0.0.1:8000/docs

### 5. Run the tests
```bash
pytest test_main.py
```

---

## Notes
- Make sure your virtual environment is activated before running or testing the app.
- All configuration is via environment variables (see `.env.example`).
- For architecture and design details, see `TECHNICAL_DESIGN.md`.
- If you want to view the architecture diagram, open `architecture.svg` or see the rendered diagram in the design doc.

---

_If you have any issues, please reach out to me, my name is Olayemi._ 