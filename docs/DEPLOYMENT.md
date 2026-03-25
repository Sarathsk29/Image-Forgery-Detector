# Deployment Guide

## Architecture

- Frontend: Vercel project using `frontend/`
- Backend: Render web service using `backend/`
- Database: Render PostgreSQL
- File/image artifact storage: Cloudinary free tier

## Backend on Render

1. Create a new Render Web Service pointing to the repo.
2. Set the root directory to `backend`.
3. Build command:

```bash
pip install -r requirements.txt
```

4. Start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

5. Add environment variables:

- `APP_ENV=production`
- `API_V1_PREFIX=/api`
- `DATABASE_URL=<render-postgres-url>`
- `STORAGE_BACKEND=cloudinary`
- `ALLOW_ORIGIN=<vercel-frontend-url>`
- `CLOUDINARY_CLOUD_NAME=<value>`
- `CLOUDINARY_API_KEY=<value>`
- `CLOUDINARY_API_SECRET=<value>`
- `MAX_UPLOAD_SIZE_MB=5`
- `TESSERACT_CMD=/usr/bin/tesseract`

## Tesseract on Render

Render free web services do not always include OCR binaries by default. If your chosen runtime image lacks Tesseract, use either:

- a Render native environment that includes `tesseract-ocr`, or
- a custom Docker deployment for the backend with Tesseract installed

If Docker is needed, install:

```dockerfile
RUN apt-get update && apt-get install -y tesseract-ocr libgl1 && rm -rf /var/lib/apt/lists/*
```

## Frontend on Vercel

1. Import the same repo into Vercel.
2. Set the root directory to `frontend`.
3. Add:

- `NEXT_PUBLIC_API_BASE_URL=<render-backend-url>`

4. Deploy the project.

## PostgreSQL

- Use a Render free PostgreSQL instance.
- Copy the external database URL into the backend `DATABASE_URL`.
- SQLAlchemy will work with PostgreSQL once the correct driver is installed in the runtime environment.

If you want strict PostgreSQL-only local parity, install `psycopg[binary]` and point `DATABASE_URL` to a local Postgres instance.

## Cloudinary

- Create folders automatically per case via the backend storage adapter.
- Evidence goes to `forensic-platform/uploads/<case_id>`
- Artifacts go to `forensic-platform/artifacts/<case_id>`
- Reports go to `forensic-platform/reports/<case_id>`

## Recommended Post-Deploy Check

1. Create a case from the public Vercel URL.
2. Upload a small image.
3. Start one analysis.
4. Poll until completion.
5. Open the report page and verify the PDF download.
6. Confirm the generated assets exist in Cloudinary.
