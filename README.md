# Multi-Modal Digital Forgery Detection System (IDF-CODEX)

> A comprehensive case-based forensic web application for detecting image forgery, AI-edited images, and document tampering using hybrid techniques such as SIFT, ELA, OCR, metadata inspection, and heuristic artifact analysis.

---

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Future Scope](#future-scope)
- [Conclusion](#conclusion)

---

## Introduction

**IDF-CODEX** (Image and Document Forgery Detection - CODEX) is an advanced forensic platform designed to detect and analyze digital forgeries across multiple media types. The system employs cutting-edge computer vision, image processing, and machine learning techniques to identify copy-move forgeries, AI-generated content, document tampering, and metadata anomalies.

### Project Vision

In an era of deepfakes and sophisticated image manipulation, IDF-CODEX provides law enforcement, digital forensics teams, and content verification specialists with an intuitive, powerful platform to:
- Authenticate digital media with confidence scores
- Generate detailed forensic reports for legal proceedings
- Streamline case management and evidence tracking
- Support multi-modal forgery detection (images, documents, AI-generated content)

### Use Cases

- **Law Enforcement**: Investigate digital evidence in criminal cases
- **Cybersecurity Teams**: Detect compromised or falsified documents
- **Content Platforms**: Verify authenticity of user-submitted media
- **Forensic Analysts**: Generate comprehensive reports for litigation
- **AI Safety Researchers**: Identify AI-generated or AI-enhanced content

---

## Features

### 🎯 Core Capabilities

#### **Multi-Modal Detection**
- **Image Forgery Detection**: Copy-Move Forgery (CMF) detection using SIFT keypoint matching
- **Error Level Analysis (ELA)**: Identifies compression artifacts and editing traces
- **AI-Generated Content Detection**: Identifies images created or significantly modified by AI models
- **Document Tampering**: OCR-based text verification and metadata inspection
- **Metadata Analysis**: EXIF data extraction and anomaly detection

#### **Streamlined Workflow**
- Intuitive multi-step UI workflow:
  1. **Case Creation**: Securely generate cases with unique Case IDs and access keys
  2. **Evidence Upload**: Upload images, PDFs, or documents for analysis
  3. **Analysis Dashboard**: Run forensic algorithms on uploaded media
  4. **Interactive Review**: Visual representation of findings with confidence scores
  5. **Report Generation**: Automatically generate downloadable PDF forensic reports

#### **Interactive Dashboards**
- **Case Management Dashboard**: Overview of all cases with status indicators
- **Evidence Log**: Color-coded verdict badges (Authentic, Forged, Suspicious, Inconclusive)
- **Confidence Score Tooltips**: Detailed confidence metrics for each analysis
- **Visual Artifact Display**: Side-by-side comparison of original and analyzed images
- **Interactive Controls**: Filter, sort, and download evidence

#### **Comprehensive Reporting**
- **PDF Export**: Professionally formatted forensic reports
- **Detailed Findings**: Systematic presentation of all analysis results
- **Visual Evidence**: High-quality artifact images embedded in reports
- **Legal Compliance**: Reports suitable for court proceedings
- **Customizable Headers**: Include case metadata, analyst information, timestamps

#### **Security Features**
- **Case Isolation**: Secure case creation with access keys
- **Session Management**: User authentication and role-based access
- **Data Privacy**: Local storage option for sensitive investigations
- **Audit Logging**: Track all analysis and report generation activities

---

## Tech Stack

### Frontend
- **Framework**: [Next.js 15.1.4](https://nextjs.org/) - React-based full-stack framework
- **Styling**: [Tailwind CSS 3.4.17](https://tailwindcss.com/) - Utility-first CSS framework
- **UI Components**: [shadcn-style components](https://ui.shadcn.com/) - Accessible, customizable React components
- **Icons**: [Lucide React 0.468.0](https://lucide.dev/) - Beautiful icon library
- **Testing**: [Vitest 2.1.8](https://vitest.dev/) - Unit testing framework
- **Language**: TypeScript 5.7.2 (45.9% of codebase)

### Backend
- **Framework**: [FastAPI 0.115.6](https://fastapi.tiangolo.com/) - Modern, fast Python API framework
- **Server**: [Uvicorn 0.32.1](https://www.uvicorn.org/) - ASGI server
- **Database ORM**: [SQLAlchemy 2.0.36](https://www.sqlalchemy.org/) - Python SQL toolkit
- **Validation**: [Pydantic 2.10.4](https://docs.pydantic.dev/) - Data validation using Python type annotations
- **Language**: Python 3.11+ (53.1% of codebase)

### Forensics & Image Processing
- **Computer Vision**: [OpenCV 4.10.0](https://opencv.org/) - Image processing library
- **Numerical Computing**: [NumPy 2.2.0](https://numpy.org/) - Array operations
- **Image Processing**: [scikit-image 0.24.0](https://scikit-image.org/) - Advanced image algorithms
- **Document Processing**: [PyMuPDF 1.25.1](https://pymupdf.readthedocs.io/) - PDF manipulation
- **OCR**: [Tesseract OCR 4.1+](https://github.com/UB-Mannheim/tesseract/wiki) - Text extraction from images

### Database & Storage
- **Primary DB**: PostgreSQL (production) with automatic fallback to SQLite (development)
- **ORM**: SQLAlchemy with Alembic migrations
- **Storage Backend**: 
  - Local disk storage (development)
  - [Cloudinary 1.42.2](https://cloudinary.com/) (production) - Cloud-based media storage
  - Driver-based architecture for easy extension

### Report Generation
- **PDF Generation**: [ReportLab 4.2.5](https://www.reportlab.com/) - Programmatic PDF creation
- **Text Processing**: Python's built-in libraries for document handling

### Additional Dependencies
- **Authentication**: Passlib 1.7.4 with bcrypt hashing
- **HTTP Client**: Httpx 0.28.1 for async HTTP requests
- **Configuration**: python-dotenv 1.0.1 for environment management
- **Database Driver**: psycopg 3.2.3 for PostgreSQL connectivity
- **Testing**: pytest 8.3.4, pytest-asyncio 0.25.0

### Architecture
```
IDF-CODEX (Monorepo)
├── frontend/          Next.js multi-page application
├── backend/           FastAPI microservice
├── docs/              Deployment & operational documentation
└── .github/           CI/CD workflows & GitHub configurations
```

---

## Installation

### Prerequisites

#### System Requirements
- **OS**: Linux, macOS, or Windows (WSL2)
- **Memory**: Minimum 4GB RAM (8GB recommended for large image analysis)
- **Disk**: 5GB free space for dependencies and cache

#### Software Requirements

**Backend:**
- Python 3.11 or higher
- pip (Python package manager)
- Tesseract OCR engine
- PostgreSQL 12+ (optional, for production deployment)

**Frontend:**
- Node.js 18+ or 20 LTS
- npm or yarn package manager

### Step-by-Step Setup

#### 1. Clone the Repository

```bash
git clone https://github.com/Sarathsk29/IDF-CODEX.git
cd IDF-CODEX
```

#### 2. Backend Setup

**Install Python Dependencies:**

```bash
cd backend

# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

**Install Tesseract OCR:**

*Linux (Ubuntu/Debian):*
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

*macOS (using Homebrew):*
```bash
brew install tesseract
```

*Windows:*
- Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
- Follow the installation wizard

**Configure Environment:**

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings:
# DATABASE_URL=sqlite:///./forensics.db  # For local development
# STORAGE_BACKEND=local                  # Use local storage
# TESSERACT_CMD=/usr/bin/tesseract       # Set if not in PATH
# OPTIONAL_AI_MODEL_PATH=               # Optional: path to AI model binary
```

**Initialize Database:**

```bash
# Run migrations (if applicable)
python -m alembic upgrade head

# Or for SQLite, the database will auto-initialize on first run
```

**Start Backend Server:**

```bash
cd ..  # Back to root
uvicorn app.main:app --reload --app-dir backend --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`

#### 3. Frontend Setup

**Install Node Dependencies:**

```bash
cd frontend

# Install dependencies
npm install
# or
yarn install
```

**Configure Environment:**

```bash
# Copy example environment file
cp .env.example .env.local

# Edit .env.local:
# NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Start Development Server:**

```bash
npm run dev
# or
yarn dev
```

The frontend will be available at `http://localhost:3000`

#### 4. Verification

Open your browser and navigate to:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/docs (Swagger UI)

---

## Usage

### Core Workflow

#### Step 1: Create a Case

1. Navigate to the **Dashboard** page
2. Click **"Create New Case"**
3. Enter case details:
   - **Case Name**: Descriptive name for your investigation
   - **Case Type**: Select forensic investigation type
   - **Description**: Add investigation notes
4. System generates:
   - Unique **Case ID** (secure, random)
   - **Access Key** (for case retrieval)
5. Copy and save the access key securely

#### Step 2: Upload Evidence

1. Go to **Evidence Upload** page
2. Select your case from the dropdown
3. Upload media files:
   - **Images**: JPG, PNG, BMP (up to 50MB each)
   - **Documents**: PDF, TIFF scans
4. Add metadata for each file:
   - Source/origin
   - Collection date
   - Any known alterations
5. Click **"Analyze"** to proceed

#### Step 3: Run Forensic Analysis

1. Navigate to **Analysis Dashboard**
2. Select evidence item from the evidence log
3. Choose analysis type:

**For Images:**
- **Copy-Move Forgery Detection**: Identifies duplicated regions
  - Confidence threshold slider: Adjust sensitivity
  - View SIFT keypoint matches overlay
- **Error Level Analysis (ELA)**: Highlights compression artifacts
  - Compression levels comparison
  - Visual heatmap overlay
- **AI-Generated Detection**: Identifies AI-created content
  - Model confidence score
  - Feature analysis

**For Documents:**
- **OCR & Text Verification**: Extract and verify text authenticity
  - Identified text regions
  - Font analysis
  - Layout consistency checks
- **Metadata Inspection**: Extract and analyze file metadata
  - EXIF data (images)
  - PDF properties (documents)
  - Creation/modification timestamps
  - Anomaly flags

4. Review **Visual Artifacts**:
   - Original image/document
   - Processing results
   - Highlighted regions
   - Confidence overlays

#### Step 4: Review Findings

The **Evidence Log** displays:

| Field | Description |
|-------|-------------|
| **File Name** | Original uploaded filename |
| **Verdict** | Authentic / Forged / Suspicious / Inconclusive |
| **Confidence** | 0-100% confidence score |
| **Analysis Date** | Timestamp of analysis |
| **Actions** | View details, download report |

**Color Coding:**
- 🟢 **Green**: Authentic (>85% confidence)
- 🟡 **Yellow**: Suspicious (50-85% confidence)
- 🔴 **Red**: Forged (<50% confidence)
- ⚫ **Gray**: Inconclusive (insufficient data)

#### Step 5: Generate Report

1. Click **"Generate Report"** for evidence item
2. Select report options:
   - Include visual artifacts
   - Include metadata analysis
   - Include confidence scores
   - Add custom notes
3. Preview PDF
4. Click **"Download Report"** to save

**Report Contents:**
- Case information header
- Evidence file details
- Analysis summary
- Detailed findings with visual artifacts
- Confidence metrics
- Analyst signature section
- Generated timestamp

### API Endpoints (Backend)

All endpoints require authentication token in header: `Authorization: Bearer <token>`

#### Case Management

```bash
# Create case
POST /api/cases
{
  "name": "Case Name",
  "type": "image_forgery",
  "description": "Investigation description"
}

# List cases
GET /api/cases

# Get case details
GET /api/cases/{case_id}

# Reopen case
POST /api/cases/{case_id}/reopen
```

#### Evidence Upload

```bash
# Upload evidence
POST /api/cases/{case_id}/evidence
Content-Type: multipart/form-data
file: <binary_file>

# List evidence for case
GET /api/cases/{case_id}/evidence

# Get evidence details
GET /api/evidence/{evidence_id}
```

#### Analysis

```bash
# Run copy-move forgery detection
POST /api/evidence/{evidence_id}/analyze/copy-move
{
  "threshold": 0.8,
  "algorithm": "sift"
}

# Run ELA analysis
POST /api/evidence/{evidence_id}/analyze/ela
{
  "compression_level": 90
}

# Run AI detection
POST /api/evidence/{evidence_id}/analyze/ai-generated
{}

# Run OCR/metadata analysis
POST /api/evidence/{evidence_id}/analyze/document
{
  "analyze_text": true,
  "analyze_metadata": true
}
```

#### Reports

```bash
# Generate report
POST /api/evidence/{evidence_id}/report
{
  "include_artifacts": true,
  "include_metadata": true
}

# Get report
GET /api/evidence/{evidence_id}/report

# Download report PDF
GET /api/evidence/{evidence_id}/report/download
```

### Configuration Examples

#### Development Environment (.env)

```env
# Database
DATABASE_URL=sqlite:///./forensics.db

# Storage
STORAGE_BACKEND=local
LOCAL_STORAGE_PATH=./uploads

# Forensics
TESSERACT_CMD=/usr/bin/tesseract
OPTIONAL_AI_MODEL_PATH=

# Server
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true
```

#### Production Environment (.env)

```env
# Database
DATABASE_URL=postgresql://user:password@db.example.com/forensics

# Storage
STORAGE_BACKEND=cloudinary
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# Security
SECRET_KEY=your-super-secret-key
JWT_EXPIRATION_HOURS=24

# Forensics
TESSERACT_CMD=/usr/bin/tesseract
OPTIONAL_AI_MODEL_PATH=/models/ai_classifier.pt

# Server
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false
```

### Command Examples

#### Analyze a Single Image Locally (CLI)

```bash
# Backend CLI tool example
python backend/app/cli.py analyze \
  --image path/to/image.jpg \
  --algorithm copy-move \
  --output result.json
```

#### Run Tests

```bash
# Backend tests
cd backend
pytest -v

# Frontend tests
cd frontend
npm run test

# With coverage
pytest --cov=app
```

---

## Screenshots

### Dashboard
The main landing page provides an overview of all cases with quick statistics and recent activity. Users can create new cases or access existing investigations.

**Key Elements:**
- Case list with status indicators
- Quick stats (Total Cases, Active Investigations, Reports Generated)
- Recent activity timeline
- Create Case button

### Case Details
Detailed view of a selected case showing:
- Case metadata (ID, creation date, type)
- Evidence count and status
- Analysis summary
- Available actions (upload evidence, generate report)

### Evidence Upload
Multi-step upload interface with:
- File drag-and-drop area
- File preview
- Progress indicators
- Metadata input fields
- Upload history

### Analysis Dashboard
Interactive analysis interface featuring:
- Evidence selector and preview
- Analysis algorithm selection
- Real-time processing indicators
- Visual artifact display (side-by-side comparison)
- Confidence score visualization
- Detailed findings panel

### Evidence Log
Comprehensive table view showing:
- All uploaded evidence files
- Analysis verdicts with color coding
- Confidence scores
- Timestamp information
- Quick action buttons (view, download, delete)
- Filtering and sorting options

### Report Viewer
PDF preview interface with:
- Full report display
- Page navigation
- Zoom controls
- Download button
- Print functionality

### API Documentation
Interactive Swagger UI at `/docs` endpoint showing:
- All available endpoints
- Request/response schemas
- Try-it-out functionality
- Authentication requirements

---

## Future Scope

### Phase 2: Enhanced Detection Capabilities

- **Deep Learning Integration**
  - Fine-tuned YOLO models for object detection
  - Vision Transformers (ViT) for forgery classification
  - Conditional GANs for forgery generation and detection

- **Video Forensics**
  - Frame-by-frame analysis
  - Temporal inconsistency detection
  - Deepfake and face-swap detection
  - Audio-visual synchronization verification

- **Advanced AI Detection**
  - Stable Diffusion artifact detection
  - DALL-E generated content identification
  - Midjourney image fingerprinting
  - ChatGPT/Claude text fingerprinting

### Phase 3: Scalability & Performance

- **Distributed Processing**
  - Celery task queue for asynchronous analysis
  - Distributed feature extraction across multiple workers
  - Horizontal scaling with load balancing

- **Performance Optimization**
  - GPU acceleration for CUDA-enabled servers
  - Batch processing for large datasets
  - Caching layer for repeated analyses
  - Query optimization for large datasets

### Phase 4: Advanced Features

- **Machine Learning Pipeline**
  - Custom model training interface
  - Transfer learning from public datasets
  - Active learning feedback loop
  - Model versioning and comparison

- **Collaboration Tools**
  - Multi-user case access with roles (Analyst, Reviewer, Admin)
  - Real-time collaboration on analysis
  - Comment and annotation system
  - Case sharing with secure links

- **Integration Ecosystem**
  - Third-party API integrations (Slack, Teams notifications)
  - SIEM integration for enterprise deployment
  - Mobile app (React Native)
  - Browser extension for quick uploads

### Phase 5: Enterprise & Compliance

- **Legal Compliance**
  - Chain of custody tracking
  - Audit logging with tamper detection
  - Digital signatures for reports
  - Compliance with ISO 27001, HIPAA, GDPR

- **Advanced Reporting**
  - Custom report templates
  - Batch report generation
  - Multi-language support
  - Expert testimony support features

- **Analytics & Insights**
  - Case statistics dashboard
  - Trend analysis
  - False positive rates tracking
  - Algorithm performance metrics

### Phase 6: Research & Development

- **Novel Detection Methods**
  - Blockchain-based authenticity verification
  - Quantum-resistant forensic signatures
  - Neural network interpretability (XAI) for forensic findings
  - Federated learning for privacy-preserving training

- **International Collaboration**
  - Multi-jurisdiction legal frameworks
  - Cross-border case sharing
  - Standardized forensic protocols
  - International dataset contribution

---

## Conclusion

**IDF-CODEX** represents a comprehensive solution to the growing challenge of digital forgery detection in an increasingly digital world. By combining multiple forensic techniques with an intuitive user interface and powerful backend infrastructure, the platform empowers investigators, security teams, and content verification specialists to authenticate digital media with confidence and generate detailed forensic reports suitable for legal proceedings.

### Key Achievements

✅ **Multi-modal Forgery Detection**: Simultaneous support for image forgery, AI-generated content, and document tampering  
✅ **Production-Ready Architecture**: Scalable monorepo with clear separation between frontend and backend  
✅ **Comprehensive Analysis**: Integration of SIFT, ELA, OCR, and metadata analysis in a unified platform  
✅ **User-Friendly Interface**: Intuitive workflow from case creation through report generation  
✅ **Legal-Grade Reporting**: PDF reports suitable for court proceedings and expert testimony  

### Impact

The IDF-CODEX platform addresses critical gaps in digital forensics:
- **Democratizes Forensic Analysis**: Advanced algorithms accessible to organizations of all sizes
- **Reduces False Positives**: Confidence-scored verdicts with visual evidence
- **Accelerates Investigations**: Automated analysis pipeline reduces manual effort
- **Ensures Accountability**: Complete audit trail and chain of custody

### Getting Involved

We welcome contributions from the open-source community:
- **Report Issues**: Found a bug? Open an issue on GitHub
- **Submit Enhancements**: Have an idea? Create a pull request
- **Share Datasets**: Contribute test images for algorithm validation
- **Improve Documentation**: Help us make this resource even better

### Support & Resources

- **Documentation**: See [docs/](./docs/) directory
- **Deployment Guide**: [docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md)
- **API Reference**: Access at `/docs` when backend is running
- **Issues & Discussions**: GitHub repository

### License

This project is open source and available under the [MIT License](LICENSE).

### Acknowledgments

Built with love and advanced computer vision techniques for the digital forensics community.

---

**Last Updated**: April 2026  
**Version**: 1.0.0  
**Maintainer**: [@Sarathsk29](https://github.com/Sarathsk29)
