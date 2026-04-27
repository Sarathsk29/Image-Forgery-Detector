# Multi-Modal Digital Forgery Detection System

Case-based forensic web application for detecting image forgery, AI-edited images, and document tampering using hybrid techniques such as SIFT, ELA, OCR, metadata inspection, and heuristic artifact analysis.

## Key Features

- **Multi-Modal Detection**: Supports image forgery (Copy-Move, ELA), document tampering (OCR, metadata), and AI-generated image detection.
- **Streamlined Workflow**: Intuitive multi-step UI separating case creation, evidence upload, analysis, and reporting.
- **Interactive Dashboards**: Clear visual evidence log with color-coded verdict badges and confidence score tooltips.
- **Comprehensive Reporting**: Automatically generated, downloadable PDF reports summarizing findings and visual artifacts.

## Stack

- Frontend: Next.js, Tailwind CSS, shadcn-style component structure
- Backend: FastAPI, Uvicorn, SQLAlchemy
- Forensics: OpenCV, NumPy, scikit-image, PyMuPDF, Tesseract OCR
- Database: PostgreSQL in deployment, SQLite fallback for local development
- Reports: ReportLab
- Storage: Local disk in development, Cloudinary in production

## Monorepo Structure

- `frontend/` Next.js multi-page investigation interface (Dashboard, Evidence Upload, Analysis, Reports)
- `backend/` FastAPI API, forensic pipelines, storage adapters, report generation
- `docs/` deployment and operations notes

## Core Workflow

1. **Case Management**: Create a new case or reopen an existing one using a securely generated `Case ID` and `access key`.
2. **Evidence Upload**: Use the dedicated upload page to securely submit one or more images or documents.
3. **Forensic Analysis Dashboard**: Navigate to the analysis page to run specific algorithms (image forgery, document forgery, or AI-edited detection).
4. **Interactive Review**: Review structured findings, visual artifacts, and confidence-scored verdict badges directly within the UI.
5. **Reporting**: Generate, view, and download detailed PDF forensic reports highlighting forgery verdicts.

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

