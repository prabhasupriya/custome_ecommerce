# Phase 14: Self-Assessment Report
**Project:** E-commerce Customer Churn Prediction  
**Student:** Bandaru Prabha Supriya  
**Student ID:** 23A91A6106  

## 1. Project Overview & Objectives
This project was an incredible deep dive into the real-world complexities of machine learning, moving far beyond simple notebook tutorials into a professional MLOps workflow. Aligning perfectly with my goal of becoming a Full-Stack Data Scientist, the task challenged me to manage a massive dataset of over 500,000 raw transactions and address a **28.09% churn rate** through a containerized Docker environment.

## 2. Key Challenges & Technical Growth
The difficulty level was significant, particularly in the following areas:
* **Infrastructure:** Troubleshooting local kernel failures and transitioning to a robust `docker-compose` execution strategy. This served as a high-value lesson in environment isolation and reproducibility.
* **Engineering:** Building a live FastAPI backend unlocked critical skills in API development and high-performance model serving.
* **Business Translation:** Learning how to translate raw model metrics like **ROC-AUC (0.84)** into meaningful business outcomes, such as protecting an estimated **£179,560 in net monthly profit** through targeted retention.

## 3. Tool Utilization & Methodology
I used AI as a strategic collaborator throughout this process to:
* **Brainstorm Feature Engineering:** Developing 30+ features including RFM scores and purchase velocity.
* **Debug Docker Environments:** Resolving complex pathing issues and volume mapping within the container.
* **Refine Documentation:** Ensuring the final system was not just accurate, but production-ready with standardized JSON artifacts.

## 4. Requirement Traceability (Self-Check)
| Requirement | Status | Evidence |
| :--- | :--- | :--- |
| **ROC-AUC ≥ 0.75** | ✅ Met | Final XGBoost model achieved **0.84**. |
| **Recall ≥ 0.65** | ✅ Met | Final model achieved **0.71**. |
| **Docker Configuration** | ✅ Met | Full `Dockerfile` and `docker-compose.yml` included. |
| **JSON Artifacts** | ✅ Met | All 5 required JSON schemas validated in `data/`. |
| **Live Deployment** | ✅ Met | Streamlit App is functional with Batch Prediction. |

## 5. Final Reflection
The biggest takeaway from this project was that a model is only as good as its deployment. By containerizing the entire pipeline, I have ensured that this project is fully reproducible, scalable, and ready for a real-world production environment.