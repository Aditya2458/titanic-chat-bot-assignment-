🚢 Titanic Dataset Chat Agent

An interactive AI-powered chatbot that analyzes the Titanic dataset using natural language.
Users can ask questions in plain English and receive both textual insights and visualizations.

Built as part of the TailorTalk Chat Agent Assignment.

📌 Features

✅ Ask questions in natural language
✅ Get instant data-driven answers
✅ Auto-generate charts & visual insights
✅ Clean Streamlit user interface
✅ Fast and lightweight backend API

🛠 Tech Stack
Layer	Technology
Backend	FastAPI
AI Agent	LangChain
Frontend	Streamlit
Data	Titanic CSV Dataset
Language	Python
📂 Project Structure
titanic-chat-agent/
│
├── backend/
│   ├── main.py
│   └── agent.py
│
├── frontend/
│   └── app.py
│
├── data/
│   └── titanic.csv
│
├── requirements.txt
└── README.md
⚙️ Installation & Setup
1️⃣ Clone the repo
git clone <your-repo-url>
cd titanic-chat-agent
2️⃣ Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
3️⃣ Install dependencies
pip install -r requirements.txt
▶️ Run the Project
Start FastAPI backend:
uvicorn backend.main:app --reload
Start Streamlit frontend:
streamlit run frontend/app.py

Open browser at:

http://localhost:8501
💬 Example Questions

What percentage of passengers were male?

Show survival rate by passenger class

How many children survived?

Compare survival by gender

📊 Visualizations

The bot dynamically generates:

Bar charts

Survival distributions

Class comparisons

All inside Streamlit.

🎯 Objective

To demonstrate:

API integration

LLM-based data querying

Real-time analytics

Clean UI for data exploration

🚀 Future Improvements

Upload custom datasets

Advanced chart controls

Model fine-tuning

User authentication

👤 Author

Aditya
Python Developer | Backend & AI Enthusiast
