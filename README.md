# 📘 Enterprise Centralized Secrets Architecture in GCP

This repository contains the implementation and documentation for a **Hub‑and‑Spoke secrets management model** in Google Cloud Platform (GCP).  
It demonstrates how a **Central Secrets Project** securely manages secrets and SSL certificates for multiple **Consumer Projects** using **Workload Identity Federation** and **automation pipelines**.

---

## 🗂️ Repository Structure

| Directory / File | Description |
|------------------|-------------|
| `.github/workflows/` | CI/CD workflows for automation and validation. |
| `scripts/` | Helper scripts for deployment, rotation, and automation tasks. |
| `architecture.png` | Visual diagram of the centralized secrets architecture. |
| `migration-plan.md` | Step‑by‑step plan for migrating existing secrets to the centralized model. |
| `migration-implementation.md` | Detailed implementation guide for executing the migration plan. |

---

## 🧩 Overview

The architecture follows a **least‑privilege design**:
- **Central Project (`prj-secrets-core`)** hosts all sensitive assets (secrets, SSL certificates).
- **Consumer Projects (`prj-app-a`, `prj-app-b`)** run workloads (GKE clusters, Load Balancers) that consume secrets securely.
- **Workload Identity Federation** enables keyless authentication between GKE and Secret Manager.
- **Automation pipelines** handle certificate distribution to consumer projects.

---

## 🧱 Key Components

- **Secret Manager** → Stores application credentials and SSL certificates centrally.  
- **GKE Workload Identity** → Allows pods to impersonate GSAs securely.  
- **Certificate Manager** → Manages SSL certificates for Load Balancers.  
- **Cloud Function / CI Pipeline** → Automates certificate updates and pushes to consumer projects.  

---

## 🚀 Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-org>/<repo-name>.git
   cd <repo-name>
