# 🎓 Student Support AI

An AI-powered student support and analytics platform built with **Django**, **RAG (ChromaDB)**, and **Make.com** workflow automation.

## 🚀 Key Features
- **AI Study Assistant (RAG):** Answers student queries using local vector embeddings stored in ChromaDB.
- **Student Accounts & Feedback:** Tracks active students, questions asked, topic difficulty, and course ratings.
- **Automated Weekly Analytics API:** Exposes a REST endpoint (`/analytics/api/weekly-summary/`) consumed by **Make.com** via Ngrok tunneling to automatically log weekly metrics and student feedback directly into **Google Sheets**.

## 🛠️ Tech Stack
- **Backend:** Python, Django
- **AI / Vector DB:** LangChain / ChromaDB
- **Automation & Integration:** Make.com (HTTP Webhook + Google Sheets API), Ngrok
- **Database:** SQLite3

## ⚙️ Local Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/MuhammadHaris1122/student-support-ai.git](https://github.com/MuhammadHaris1122/student-support-ai.git)
   cd student-support-ai