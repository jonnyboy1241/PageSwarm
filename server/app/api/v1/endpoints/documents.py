"""Document ingestion endpoints for PDF upload and job enqueue metadata."""

import io
from datetime import UTC, datetime
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, Request, UploadFile, status
from pypdf import PdfReader

from app.core.logging import get_logger
from app.schemas.documents import UploadDocumentResponse

router = APIRouter(prefix="/documents")
logger = get_logger(__name__)


# Keep uploads bounded to 25 MB to reduce memory and parsing DoS risk.
MAX_UPLOAD_SIZE_BYTES = 25 * 1024 * 1024


@router.post(
    "/upload",
    response_model=UploadDocumentResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def upload_document(
    request: Request,
    file: UploadFile = File(...),
) -> UploadDocumentResponse:
    """Validate an uploaded PDF and return queued job metadata.

    Args:
        request: Incoming HTTP request containing headers for size prechecks.
        file: Uploaded PDF file payload provided by multipart form-data.

    Returns:
        UploadDocumentResponse containing accepted upload metadata and queue status.
    """
    if file.content_type not in {"application/pdf", "application/x-pdf"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported",
        )

    content_length = request.headers.get("content-length")
    if content_length:
        try:
            if int(content_length) > MAX_UPLOAD_SIZE_BYTES:
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"Uploaded file exceeds {MAX_UPLOAD_SIZE_BYTES} bytes",
                )
        except ValueError:
            logger.warning(
                "invalid_content_length_header",
                extra={"content_length": content_length},
            )

    file.file.seek(0, io.SEEK_END)
    size_bytes = file.file.tell()
    file.file.seek(0)

    if size_bytes == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty",
        )

    if size_bytes > MAX_UPLOAD_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Uploaded file exceeds {MAX_UPLOAD_SIZE_BYTES} bytes",
        )

    try:
        reader = PdfReader(file.file)
        page_count = len(reader.pages)
    except Exception as exc:
        logger.warning(
            "invalid_pdf_upload",
            extra={"document_name": file.filename, "error": str(exc)},
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
        size_bytes=size_bytes,
        total_pages=page_count,
        status="queued",
        accepted_at=datetime.now(UTC),
    )
    logger.info(
        "pdf_upload_accepted",
        extra={
            "job_id": response.job_id,
            "document_name": response.filename,
            "size_bytes": response.size_bytes,
            "total_pages": response.total_pages,
        },
    )
    return response
