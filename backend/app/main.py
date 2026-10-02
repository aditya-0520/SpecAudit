from datetime import date
from typing import Any
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="SpecAudit-IS API", version="0.1.0", description="Evidence-oriented tender audit API. Included records are synthetic DEMO data.")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_methods=["*"], allow_headers=["*"])

REGISTRY_SNAPSHOT = date(2026, 9, 30)
SAMPLES = {
    "led": {"id":"AUD-DEMO-001","title":"LED Lighting Procurement","tender_id":"GEM/2026/B/7142081","category":"Lighting","state":"Needs review","coverage":71,"requirements":17,"gaps":3,"registry_snapshot":str(REGISTRY_SNAPSHOT),"data_state":"DEMO","requirements_data":[
        {"id":"R-01","name":"Luminaire rated power","text":"Nominal input power shall be 36 W ± 5%.","normalized_text":"Rated input power equals 36 W ± 5%","category":"Technical","parameter":"input power","value":"36","unit":"W","operator":"±","page":4,"section":"4.1","confidence":.96,"coverage":"Covered","standard":"DEMO-IS-LGT-2023"},
        {"id":"R-02","name":"Luminous efficacy","text":"Minimum system efficacy of 120 lm/W.","normalized_text":"Minimum luminous efficacy 120 lm/W","category":"Performance","parameter":"luminous efficacy","value":"120","unit":"lm/W","operator":">=","page":4,"section":"4.2","confidence":.94,"coverage":"Covered","standard":"DEMO-IS-LGT-2023"},
        {"id":"R-03","name":"Colour temperature","text":"Select 3000 K, 4000 K or 5700 K by site zone.","normalized_text":"Buyer must select correlated colour temperature per site zone","category":"Technical","parameter":"CCT","value":"3000 / 4000 / 5700","unit":"K","operator":"choice","page":5,"section":"4.3","confidence":.78,"coverage":"Partial","standard":"DEMO-IS-LGT-2023"},
        {"id":"R-04","name":"Ingress protection","text":"Minimum IP65 for outdoor fixtures.","normalized_text":"Outdoor fixture ingress protection at least IP65","category":"Safety","parameter":"IP rating","value":"65","unit":"IP","operator":">=","page":5,"section":"4.4","confidence":.91,"coverage":"Covered","standard":"DEMO-IS-LGT-2023"},
        {"id":"R-05","name":"Colour rendering index","text":"CRI shall be at least 70.","normalized_text":"Colour rendering index at least 70","category":"Performance","parameter":"CRI","value":"70","unit":"Ra","operator":">=","page":5,"section":"4.5","confidence":.83,"coverage":"Covered","standard":"DEMO-IS-LGT-2023"},
        {"id":"R-06","name":"Operating temperature","text":"Operating temperature range is not specified.","normalized_text":"Operating temperature range missing","category":"Environmental","parameter":"operating temperature","value":None,"unit":"°C","operator":None,"page":6,"section":"4.6","confidence":.89,"coverage":"Gap","standard":None},
        {"id":"R-07","name":"Product quality","text":"The product should be of good quality and latest technology.","normalized_text":"Vague, non-measurable quality wording","category":"Other","parameter":"quality","value":None,"unit":None,"operator":None,"page":6,"section":"4.7","confidence":.98,"coverage":"Gap","standard":None},
        {"id":"R-08","name":"Rated service life","text":"L70 lifetime of 50,000 hours at specified ambient conditions.","normalized_text":"L70 lifetime 50,000 hours","category":"Performance","parameter":"service life","value":"50000","unit":"h","operator":">=","page":6,"section":"4.8","confidence":.87,"coverage":"Partial","standard":"DEMO-IS-LGT-2023"},
        {"id":"R-09","name":"Power factor","text":"Power factor shall be ≥ 0.90 at full load.","normalized_text":"Power factor at least 0.90 full load","category":"Technical","parameter":"power factor","value":"0.90","unit":None,"operator":">=","page":7,"section":"4.9","confidence":.90,"coverage":"Covered","standard":"DEMO-IS-LGT-2023"},
        {"id":"R-10","name":"Harmonic distortion","text":"Total harmonic distortion ≤ 10%.","normalized_text":"Total harmonic distortion maximum ten percent","category":"Technical","parameter":"THD","value":"10","unit":"%","operator":"<=","page":7,"section":"4.10","confidence":.86,"coverage":"Covered","standard":"DEMO-IS-LGT-2023"},
        {"id":"R-11","name":"Surge protection","text":"Provide surge protection suited to the installation.","normalized_text":"Surge protection threshold not stated","category":"Safety","parameter":"surge protection","value":None,"unit":"kV","operator":None,"page":7,"section":"4.11","confidence":.81,"coverage":"Partial","standard":"DEMO-IS-SAFE-2022"},
        {"id":"R-12","name":"Test method","text":"Type test documentation shall be submitted.","normalized_text":"Type testing required, method not stated","category":"Testing","parameter":"type test","value":None,"unit":None,"operator":None,"page":8,"section":"4.12","confidence":.76,"coverage":"Partial","standard":"DEMO-IS-TEST-2021"},
        {"id":"R-13","name":"BIS certification","text":"Certification evidence to be supplied where applicable.","normalized_text":"Certification applicability unknown","category":"Certification","parameter":"BIS certification","value":None,"unit":None,"operator":None,"page":8,"section":"4.13","confidence":.70,"coverage":"Unverified","standard":None},
        {"id":"R-14","name":"Marking","text":"Marking content and permanence requirements not stated.","normalized_text":"Marking fields and durability incomplete","category":"Marking","parameter":"marking","value":None,"unit":None,"operator":None,"page":9,"section":"4.14","confidence":.88,"coverage":"Partial","standard":"DEMO-IS-LGT-2023"},
        {"id":"R-15","name":"Warranty","text":"Minimum warranty period of five years.","normalized_text":"Warranty at least five years","category":"Warranty","parameter":"warranty","value":"5","unit":"years","operator":">=","page":9,"section":"4.15","confidence":.95,"coverage":"Covered","standard":None},
        {"id":"R-16","name":"Packaging","text":"Fixtures must be protected during transport and storage.","normalized_text":"Protect fixtures during transport and storage","category":"Packaging","parameter":"packaging","value":None,"unit":None,"operator":None,"page":10,"section":"4.16","confidence":.83,"coverage":"Covered","standard":None},
        {"id":"R-17","name":"Inspection and acceptance","text":"Inspection and acceptance criteria are not defined.","normalized_text":"Inspection and acceptance criteria missing","category":"Inspection","parameter":"acceptance criteria","value":None,"unit":None,"operator":None,"page":10,"section":"4.17","confidence":.93,"coverage":"Gap","standard":None},
    ]},
    "panels": {"id":"AUD-DEMO-002","title":"Industrial Control Panels","tender_id":"EPC/2026/IND/0842","category":"Electrical · Industrial","state":"In progress","coverage":64,"requirements":14,"gaps":4,"registry_snapshot":str(REGISTRY_SNAPSHOT),"data_state":"DEMO"},
    "pumps": {"id":"AUD-DEMO-003","title":"Campus Water Pumps","tender_id":"UNI/PROC/2026/119","category":"Pumps · Water systems","state":"Approved","coverage":88,"requirements":12,"gaps":1,"registry_snapshot":str(REGISTRY_SNAPSHOT),"data_state":"DEMO"},
}

def _seed_product_demo(key: str, prefix: str, standard: str, rows: list[tuple[str, str, str, str, str]]) -> None:
    """Build synthetic structured checklist rows; these are not real tender extracts."""
    audit = SAMPLES[key]
    audit["requirements_data"] = [
        {"id":f"{prefix}-R-{i:02d}","name":name,"text":text,"normalized_text":name.lower(),"category":category,"parameter":name.lower(),"value":value,"unit":None,"operator":None,"page":4+(i-1)//2,"section":f"4.{i}","confidence":.82,"coverage":coverage,"standard":None if coverage=="Gap" else standard}
        for i, (name, text, category, value, coverage) in enumerate(rows, start=1)
    ]
    audit["requirements"] = len(rows)
    audit["gaps"] = sum(row[4] == "Gap" for row in rows)
    audit["coverage"] = round(100 * sum(row[4] == "Covered" for row in rows) / max(len(rows), 1))

_seed_product_demo("panels", "IC", "DEMO-IS-CTRL-2024", [
    ("Panel rated voltage","Three-phase 415 V AC supply.","Technical","415 V","Covered"),("Rated current","Continuous rated current of 630 A.","Technical","630 A","Covered"),("Short-circuit withstand","Prospective fault withstand value not stated.","Safety","Not specified","Gap"),("Enclosure protection","Minimum IP54 for indoor installation.","Safety","IP54","Covered"),("Busbar material","Copper busbar finish and grade are not stated.","Material","Unspecified","Partial"),("Temperature rise","Maximum permissible temperature rise not stated.","Performance","Not specified","Gap"),("Dielectric test","Routine dielectric test report required.","Testing","Report required","Partial"),("Earthing continuity","Protective earth bonding continuity required.","Safety","Required","Covered"),("Wiring identification","Terminal and conductor identification criteria missing.","Marking","Incomplete","Partial"),("Ingress and dust","Ingress protection class shall match the installation.","Environmental","Buyer choice open","Partial"),("Operating temperature","Ambient operating range not stated.","Environmental","Not specified","Gap"),("Drawings and schematics","Provide dimensioned drawings and circuit diagrams.","Inspection","Required","Covered"),("Warranty period","Minimum warranty period of two years.","Warranty","2 years","Covered"),("Inspection acceptance","Factory acceptance test witness points not defined.","Inspection","Not specified","Partial"),
])
_seed_product_demo("pumps", "WP", "DEMO-IS-PUMP-2022", [
    ("Pump duty point","Rated flow and total head to be supplied by buyer.","Performance","Buyer choice open","Partial"),("Pump efficiency","Minimum efficiency target not stated.","Performance","Not specified","Gap"),("Motor rating","Motor power rating shall be declared on the offer.","Technical","Declared","Covered"),("Supply voltage","Three-phase 415 V AC supply.","Technical","415 V","Covered"),("Wetted materials","Wetted part material grade is not stated.","Material","Unspecified","Gap"),("Casing pressure","Maximum working pressure to be declared.","Safety","Declared","Partial"),("Cavitation margin","NPSH acceptance limit not stated.","Performance","Not specified","Gap"),("Hydrostatic test","Hydrostatic test evidence required.","Testing","Evidence required","Partial"),("Vibration limits","Permissible vibration threshold not stated.","Testing","Not specified","Gap"),("Noise limits","Sound pressure acceptance criterion missing.","Environmental","Not specified","Gap"),("Ingress protection","Motor enclosure protection rating to be identified.","Safety","Buyer choice open","Partial"),("BIS certification evidence","Applicability and evidence source are not specified.","Certification","Unknown","Unverified"),
])

class AuditCreate(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    tender_id: str = Field(min_length=2, max_length=100)
    organization: str = Field(min_length=2, max_length=200)
    category: str = Field(min_length=2, max_length=100)
    tender_date: date
    language: str = "English"
    demo_key: str | None = None

class ReviewDecision(BaseModel):
    recommendation_id: str
    decision: str = Field(pattern="^(ACCEPT|MODIFY|REJECT|NOT_APPLICABLE)$")
    reason: str = Field(min_length=3, max_length=1000)
    modified_text: str | None = Field(default=None, max_length=5000)

@app.get("/health")
def health() -> dict[str, Any]:
    return {"status":"ok", "service":"specaudit-is-api", "registry_snapshot":str(REGISTRY_SNAPSHOT), "database":"not connected; deterministic demo mode"}

@app.get("/api/v1/audits")
def list_audits() -> dict[str, Any]:
    return {"items":list(SAMPLES.values()), "count":len(SAMPLES), "data_state":"DEMO"}

@app.post("/api/v1/audits")
def create_audit(body: AuditCreate) -> dict[str, Any]:
    if body.demo_key and body.demo_key not in SAMPLES:
        raise HTTPException(404, "Unknown demo dataset. No audit created.")
    if body.demo_key:
        return {**SAMPLES[body.demo_key], "tender_date":str(body.tender_date), "organization":body.organization, "created":True}
    return {"id":"AUD-LOCAL-DRAFT", "title":body.title, "tender_id":body.tender_id, "category":body.category, "organization":body.organization, "tender_date":str(body.tender_date), "state":"Draft", "requirements":0, "gaps":0, "registry_snapshot":str(REGISTRY_SNAPSHOT), "data_state":"LOCAL DRAFT - not yet analyzed"}

@app.get("/api/v1/audits/{audit_id}")
def get_audit(audit_id: str) -> dict[str, Any]:
    audit = next((a for a in SAMPLES.values() if a["id"] == audit_id or a["tender_id"] == audit_id), None)
    if not audit: raise HTTPException(404, "Audit not found in the local demo dataset.")
    return audit

@app.get("/api/v1/audits/{audit_id}/requirements")
def get_requirements(audit_id: str) -> dict[str, Any]:
    audit = get_audit(audit_id)
    items = audit.get("requirements_data", [])
    return {"items":items, "count":len(items), "data_state":"DEMO - synthetic extraction output", "audit_id":audit["id"]}

@app.post("/api/v1/requirements/{requirement_id}/retrieve")
def retrieve_for_requirement(requirement_id: str) -> dict[str, Any]:
    for audit in SAMPLES.values():
        requirement = next((r for r in audit.get("requirements_data", []) if r["id"] == requirement_id), None)
        if requirement:
            return {"requirement_id":requirement_id, "items":([{"standard_number":requirement["standard"], "evidence_state":"DEMO / UNVERIFIED", "confidence":None, "scores":None, "reason":"Synthetic requirement-to-record association for workflow demonstration."}] if requirement["standard"] else []), "data_state":"DEMO; no semantic search or registry verification configured"}
    raise HTTPException(404, "Requirement not found in demo dataset.")

@app.post("/api/v1/audits/{audit_id}/decision-audit")
def decision_audit(audit_id: str) -> dict[str, Any]:
    result = get_requirements(audit_id)
    items = result["items"]
    counts = {state: sum(1 for item in items if item.get("coverage") == state) for state in ("Covered", "Partial", "Gap", "Unverified")}
    return {"items":items, "counts":counts, "total":len(items), "data_state":"DEMO-only evaluation; checklist expert source not configured"}

@app.get("/api/v1/audits/{audit_id}/compliance")
def compliance_matrix(audit_id: str) -> dict[str, Any]:
    return decision_audit(audit_id)

@app.post("/api/v1/audits/{audit_id}/wording-analysis")
def wording_analysis(audit_id: str) -> dict[str, Any]:
    items = get_requirements(audit_id)["items"]
    vague = ("good quality", "latest technology", "high quality", "best quality", "as per relevant standards", "suitable material", "high efficiency")
    flags = [{"requirement_id":r["id"],"phrase":phrase,"issue":"Vague / non-measurable wording","state":"REQUIRES_REVIEW"} for r in items for phrase in vague if phrase in r["text"].lower()]
    return {"items":flags, "count":len(flags), "data_state":"Deterministic phrase flags; suggested edits require officer review"}

@app.post("/api/v1/audits/{audit_id}/conflict-check")
def conflict_check(audit_id: str) -> dict[str, Any]:
    get_audit(audit_id)
    return {"items":[], "state":"NOT_EVALUATED", "message":"No verified standard clauses are available to compare. Absence of a detected conflict is not a clearance."}

@app.post("/api/v1/audits/{audit_id}/improved-tender")
def propose_tender_edits(audit_id: str) -> dict[str, Any]:
    flags = wording_analysis(audit_id)["items"]
    return {"items":[{"requirement_id":f["requirement_id"], "original_text":next(r["text"] for r in get_requirements(audit_id)["items"] if r["id"] == f["requirement_id"]), "proposed_text":"Replace with purchaser-defined, measurable parameters. Include only standards verified against an authoritative, dated registry.", "state":"REQUIRES_REVIEW", "data_state":"DEMO"} for f in flags], "notice":"No unverified standard or certification clause has been added."}

@app.post("/api/v1/chat")
def grounded_assistant(payload: dict[str, str]) -> dict[str, Any]:
    return {"answer":"I cannot verify applicable standards from the available data. This demo has no connected authoritative standards registry; check a cited identifier in the IS Checker and ask an officer to verify the source.", "sources":[], "state":"INSUFFICIENT_VERIFIED_EVIDENCE", "language":"English", "notice":"No standards have been inferred or invented."}

@app.post("/api/v1/audits/{audit_id}/documents")
async def upload_document(audit_id: str, request: Request) -> dict[str, Any]:
    get_audit(audit_id)
    content_type = request.headers.get("content-type", "").split(";")[0].strip()
    allowed = {"application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain"}
    if content_type not in allowed: raise HTTPException(415, "Send a raw PDF, DOCX or TXT body with its content-type header.")
    content = await request.body()
    if len(content) > 25 * 1024 * 1024: raise HTTPException(413, "Maximum upload size is 25 MB.")
    filename = request.headers.get("x-filename", "uploaded-tender")
    return {"filename":filename[:255], "bytes_received":len(content), "state":"RECEIVED - OCR/extraction provider not configured", "ocr_provider":"not configured", "data_state":"No extracted facts claimed"}

@app.post("/api/v1/audits/{audit_id}/extract")
def extract_requirements(audit_id: str) -> dict[str, Any]:
    result = get_requirements(audit_id)
    if not result["items"]: raise HTTPException(501, "Extraction provider is not configured for this tender.")
    return result

@app.get("/api/v1/standards/search")
def search_standards(q: str = Query(min_length=1), limit: int = Query(default=20, ge=1, le=100)) -> dict[str, Any]:
    matches = [{"standard_number":x, "title":"Synthetic demonstration record", "status":"DEMO / UNVERIFIED", "official_source":None} for x in ("DEMO-IS-LGT-2023","DEMO-IS-SAFE-2022","DEMO-IS-TEST-2021") if q.lower() in x.lower()]
    return {"items":matches[:limit], "count":len(matches), "registry_snapshot":str(REGISTRY_SNAPSHOT), "notice":"Synthetic demo identifiers are not real BIS records."}

@app.get("/api/v1/is-checker")
def is_checker(number: str = Query(min_length=2)) -> dict[str, Any]:
    return {"query":number, "status":"UNVERIFIED", "verified":False, "registry_snapshot":str(REGISTRY_SNAPSHOT), "message":"No verified live registry source is configured. Officer verification required."}

@app.post("/api/v1/standards/check-version")
def check_version(payload: dict[str, str]) -> dict[str, Any]:
    return {"status":"REQUIRES_REVIEW", "verified":False, "data_state":"DEMO only", "message":"Version validation requires dated authoritative registry records. None are configured."}

@app.post("/api/v1/standards/check-certification")
def check_certification(payload: dict[str, str]) -> dict[str, Any]:
    return {"bis":"UNKNOWN", "qco":"UNKNOWN", "crs":"UNKNOWN", "hallmarking":"UNKNOWN", "verified":False, "source":None, "message":"No verified certification rule records are configured."}

@app.post("/api/v1/reviews")
def submit_review(body: ReviewDecision) -> dict[str, Any]:
    return {"recommendation_id":body.recommendation_id, "decision":body.decision, "reason":body.reason, "modified_text":body.modified_text, "state":"RECORDED IN DEMO RESPONSE ONLY", "audit_log_entry_created":False, "notice":"Persistent database is not configured; this response was not stored."}

@app.get("/api/v1/evaluation")
def evaluation() -> dict[str, Any]:
    return {"state":"DATASET_NOT_CONFIGURED", "metrics":None, "message":"No expert-labelled evaluation dataset is configured. Metrics are not fabricated."}

@app.get("/api/v1/audits/{audit_id}/audit-log")
def audit_log(audit_id: str) -> dict[str, Any]:
    get_audit(audit_id)
    return {"items":[], "state":"No persistent audit log configured. Demo UI events are session-local only."}
