# SpecAudit-IS

AI-assisted procurement tender auditing with traceable evidence and explicit officer review. The included browser experience is an offline-first, deterministic DEMO and makes no claims that its synthetic standard identifiers or certification rules are real BIS data.

## Run the frontend

```powershell
npm install
npm run dev
```

Open http://localhost:3000. Select **New audit → Start demo audit** to open the LED tender review. The workspace includes 17 synthetic requirements, selected-source highlighting, evidence and review controls, decision-point coverage, unverified registry results, a version review example, a proposed tender edit, and sample audit history. Demo actions are explicitly labelled and session-local.

## Run the API

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API health: http://localhost:8000/health · OpenAPI: http://localhost:8000/docs. REST endpoints expose the deterministic demo records and safe unknown states. Uploaded documents are size/type checked but not stored or processed until a secure object-store and OCR provider are configured. API review responses are not persisted without a configured database.

## Database foundation

`backend/app/db/schema.sql` defines the PostgreSQL relational schema, including pgvector-ready requirement embeddings, dated registry snapshots, recommendations, evidence, checklist decisions, officer reviews and append-only audit events. `backend/app/db/demo_seed.sql` creates a synthetic LED audit with 17 structured requirement records and three clearly synthetic standard identifiers, plus metadata for the other sample audits. No standard record is marked verified. `docker compose up -d db` starts PostgreSQL with pgvector. Configure `DATABASE_URL` from `.env.example` before adding a database-backed repository. The current API reports that database persistence is not configured instead of implying writes succeeded.

## Trust boundaries

- `DEMO-*` identifiers and all inline sample requirements are synthetic training/demo content, not authoritative standards.
- The IS Checker returns `UNVERIFIED` when a verified registry source is absent.
- Version and certification endpoints return `REQUIRES_REVIEW` / `UNKNOWN` without dated source records.
- Evaluation metrics stay empty until an expert-labelled dataset is provided.
- Officer review remains mandatory. No AI/demo action silently finalizes an audit.
- OCR, model, vector search, and live registry providers are abstraction points, not connected external services.
