import io
from datetime import UTC, datetime
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from pypdf import PdfReader

from app.core.logging import get_logger
from app.schemas.documents import UploadDocumentResponse

router = APIRouter(prefix="/documents")
logger = get_logger(__name__)


@router.post(
    "/upload",
    response_model=UploadDocumentResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def upload_document(file: UploadFile = File(...)) -> UploadDocumentResponse:
    if file.content_type not in {"application/pdf", "application/x-pdf"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported",
        )

    payload = await file.read()
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty",
        )

    try:
        reader = PdfReader(io.BytesIO(payload))
        page_count = len(reader.pages)
    except Exception as exc:
        logger.warning(
            "invalid_pdf_upload",
            extra={"filename": file.filename, "error": str(exc)},
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is not a valid PDF",
        ) from exc

    if page_count == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded PDF contains no pages",
        )

    job_id = str(uuid4())
    response = UploadDocumentResponse(
        job_id=job_id,
        filename=file.filename or "uploaded.pdf",
        size_bytes=len(payload),
        total_pages=page_count,
        status="queued",
        accepted_at=datetime.now(UTC),
    )
    logger.info(
        "pdf_upload_accepted",
        extra={
            "job_id": response.job_id,
            "filename": response.filename,
            "size_bytes": response.size_bytes,
            "total_pages": response.total_pages,
        },
    )
    return response
