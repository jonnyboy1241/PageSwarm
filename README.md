<div align="center">

# 🐝 PageSwarm

**Distributed Document Processing — Break It Down, Swarm It Out**

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![AWS](https://img.shields.io/badge/AWS-S3%20%7C%20SQS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)](https://aws.amazon.com)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docs.docker.com/compose/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

<br/>

<img src="https://img.shields.io/badge/status-in%20development-blueviolet?style=flat-square" alt="Status"/>

*Upload a PDF. Fan out every page. Process them in parallel. Reassemble the result.*

<br/>

```
          📄 Upload PDF
               │
               ▼
        ┌──────────────┐
        │   API Service │  ← FastAPI
        └──────┬───────┘
               │
        ┌──────▼───────┐
        │  Object Store │  ← S3 / LocalStack
        └──────┬───────┘
               │
        ┌──────▼───────┐
        │ Message Queue │  ← SQS
        └──┬───┬───┬───┘
           │   │   │
     ┌─────▼┐ ┌▼────┐ ┌▼─────┐
     │ 🐝 W1│ │🐝 W2│ │🐝 W3 │  ← Worker Swarm
     └──┬───┘ └──┬──┘ └──┬───┘
        │        │       │
        └────────┼───────┘
                 ▼
        ┌──────────────┐
        │ Result Store  │
        └──────────────┘
               │
               ▼
        📋 Aggregated Output
```

</div>

---

## 📌 What Is This?

PageSwarm is a **distributed document processing pipeline** that takes a PDF, splits it into individual pages, and fans out processing across a swarm of parallel workers. Each worker independently extracts text from its assigned page, and the system reassembles everything into a single coherent result.

It's a showcase of real-world distributed systems patterns — built with **Python**, **FastAPI**, **AWS (LocalStack)**, and **Docker Compose**.

### Key Concepts

| Concept | How It's Demonstrated |
|---|---|
| **Distributed Job Processing** | Documents are broken into page-level jobs dispatched to independent workers |
| **Queue-Based Architecture** | SQS decouples the API from workers — producers and consumers operate independently |
| **Parallel Processing** | Multiple workers drain the queue concurrently, slashing total processing time |
| **Fault Tolerance & Retries** | If a worker crashes mid-page, the message returns to the queue for another worker |
| **Horizontal Scaling** | Spin up more workers with a single flag: `--scale worker=5` |
| **Idempotent Operations** | Processing the same page twice won't corrupt results |

---

## 📋 Functional Requirements

### Document Upload

- Accept a PDF document via the API
- Store the document in object storage (S3)
- Generate a unique job ID
- Determine the total number of pages

### Page Job Fan-Out

- Split the uploaded document into individual pages
- Create one job per page
- Publish each job to a message queue (SQS)
- Each job must include the job ID, page number, and document location

### Worker Processing

- Workers poll the queue for page jobs
- Retrieve the assigned document page from storage
- Extract text from the page
- Produce structured output with the extracted content
- Support horizontal scaling (multiple workers running simultaneously)

### Result Storage

- Store processed page results in a persistent datastore
- Each result must contain: job ID, page number, extracted content, and processing timestamp

### Result Aggregation

- Once all pages for a job are processed, aggregate results in correct page order
- Produce a final combined document result

### Job Status

- Users can query the progress of any job
- Statuses: `queued` → `processing` → `completed` or `failed`
- Response includes pages processed vs. total pages

---

## ⚙️ Non-Functional Requirements

| Requirement | Detail |
|---|---|
| **Scalability** | Horizontal worker scaling — more workers = faster processing |
| **Fault Tolerance** | Worker crashes return the job to the queue for retry by another worker |
| **Idempotency** | Duplicate processing of the same page must not corrupt results |
| **Observability** | Structured logging of job creation, page dispatch, worker activity, and completion |

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| **Language** | Python |
| **API** | FastAPI |
| **Object Storage** | AWS S3 (LocalStack) |
| **Message Queue** | AWS SQS (LocalStack) |
| **AWS SDK** | boto3 |
| **PDF Processing** | PyPDF |
| **Infrastructure** | Docker Compose + LocalStack |

---

## 🗺️ Roadmap

- [ ] Core API: upload, status, result endpoints
- [ ] S3 document storage integration
- [ ] SQS fan-out for page jobs
- [ ] Worker pool with queue polling
- [ ] Text extraction with PyPDF
- [ ] Result aggregation pipeline
- [ ] Docker Compose orchestration
- [ ] Fault tolerance & retry logic
- [ ] Structured logging & observability
- [ ] Integration tests
- [ ] Dead letter queue for poison messages
- [ ] WebSocket for real-time progress updates
- [ ] Support for additional file types (DOCX, images via OCR)
- [ ] Prometheus metrics endpoint

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

**Built by [Jonathan](https://github.com/jonnyboy1241)** · Distributed systems in action · 🐝

</div>