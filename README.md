# Multi-Modal Digital Forgery Detection System

Case-based forensic web application for detecting image forgery, AI-edited images, and document tampering using hybrid techniques such as SIFT, ELA, OCR, metadata inspection, and heuristic artifact analysis.

## Stack

- Frontend: Next.js, Tailwind CSS, shadcn-style component structure
- Backend: FastAPI, Uvicorn, SQLAlchemy
- Forensics: OpenCV, NumPy, scikit-image, PyMuPDF, Tesseract OCR
- Database: PostgreSQL in deployment, SQLite fallback for local development
- Reports: ReportLab
- Storage: Local disk in development, Cloudinary in production

## Monorepo Structure

- `frontend/` Next.js investigation interface
- `backend/` FastAPI API, forensic pipelines, storage adapters, report generation
- `docs/` deployment and operations notes

## Core Workflow

1. Create a case and receive a `Case ID` plus `access key`
2. Reopen a case using both values
3. Upload one or more evidence files
4. Start image forgery, document forgery, or AI-edited analysis
5. Poll asynchronous job status
6. Review structured findings and visual artifacts
7. Download the generated PDF forensic report

## Local Development

### Backend

1. Install Python 3.11+ and Tesseract OCR.
2. Create a virtual environment inside `backend/`.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Copy `backend/.env.example` to `backend/.env` and update values if needed.
5. Start the API:

```bash
uvicorn app.main:app --reload --app-dir backend
```

### Frontend

1. Install Node.js dependencies inside `frontend/`:

```bash
npm install
```

2. Copy `frontend/.env.example` to `frontend/.env.local`.
3. Start the app:

```bash
npm run dev
```

The frontend expects the backend at `http://localhost:8000` by default.

## Environment Notes

- `DATABASE_URL` can point to PostgreSQL for production or stay on SQLite for local work.
- Set `STORAGE_BACKEND=cloudinary` with Cloudinary credentials to store assets remotely.
- Set `TESSERACT_CMD` when the Tesseract executable is not on the system PATH.
- Set `OPTIONAL_AI_MODEL_PATH` only when you have a TorchScript binary classifier to plug in.

## Suggested Demo Dataset

- One clear copy-move tampered image
- One AI-enhanced or generatively edited image
- One scanned PDF with altered values or pasted text region
- One authentic control image/document for comparison

## Tests

### Backend

```bash
pytest
```

### Frontend

```bash
npm run test
```

## Deployment

See [docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md) for Vercel, Render, PostgreSQL, and Cloudinary deployment steps.

