# Technical Documentation: Production-Ready Architecture

## 1. Data Layer (Persistence & Management)
* **Dockerized Volumes:** The architecture utilizes Docker volumes to ensure data persistence. [cite_start]This prevents data loss when containers are restarted or rebuilt[cite: 1, 2].
* [cite_start]**Automated Pipeline:** Data flows through a structured pipeline from raw ingestion to cleaned artifacts, with each step validated by JSON statistics[cite: 1, 2].
* [cite_start]**Storage Strategy:** Separation of `raw`, `processed`, and `final` data directories ensures clear lineage and auditability of the datasets[cite: 1, 2].

## 2. API Layer (Real-time Prediction Engine)
* [cite_start]**FastAPI Backend:** The core logic is served via a **FastAPI** microservice, chosen for its high performance and native support for asynchronous operations[cite: 1, 2].
* [cite_start]**Model Serving:** The `churn_model.pkl` (XGBoost) and the `scaler.pkl` are loaded into memory upon container startup to provide near-instant churn probabilities[cite: 1, 3].
* [cite_start]**Swagger Integration:** Automated API documentation is available at `/docs`, allowing developers to test endpoints interactively[cite: 1, 2].

## 3. UI Layer (Business Intelligence Dashboard)
* [cite_start]**Streamlit Frontend:** A dedicated **Streamlit** application provides an intuitive interface for non-technical stakeholders to interact with the model[cite: 1, 2].
* [cite_start]**Features:** The dashboard allows users to upload customer transaction files and receive immediate batch predictions or visualize RFM distributions[cite: 1, 2].
* [cite_start]**Accessibility:** By separating the UI from the API, the system remains modular, allowing the dashboard to be updated without affecting the underlying prediction logic[cite: 1, 2].

## 4. Infrastructure & Deployment
* [cite_start]**Containerization:** The entire stack is orchestrated using **Docker Compose**, ensuring a "Build Once, Run Anywhere" workflow that eliminates environment-specific issues[cite: 1, 2].
* [cite_start]**Scalability:** The microservice architecture allows for independent scaling of the API and UI layers based on user demand[cite: 1, 2].