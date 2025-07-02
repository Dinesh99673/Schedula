# 📅 Schedula - Smart Appointment Booking Assistant

Schedula is a conversational AI agent that helps users book appointments seamlessly via natural language. It integrates with Google Calendar and uses Google's Gemini model (gemini-1.5-flash) for understanding booking intents.

---

## 🚀 Features

- 🗣️ Conversational interface using Gemini (via LangChain)
- 📅 Real-time Google Calendar integration
- 🧠 Intelligent intent detection (with slot-based availability)
- 🧪 Checks conflicts and avoids double booking
- 🌐 FastAPI backend and Streamlit frontend
- 🔐 Secure credential management via environment variables

---

## 🛠️ Technologies Used

- **FastAPI** – Backend API
- **Streamlit** – Conversational frontend UI
- **Google Calendar API** – Calendar events & availability
- **Gemini API** – Natural language understanding (gemini-1.5-flash)
- **Render** – Backend deployment
- **Streamlit Cloud** – Frontend deployment

---

## ⚙️ Setup Instructions

### 🔧 Backend (FastAPI)

1. Clone the repository:
   ```bash
   git clone https://github.com/Dinesh99673/Schedula.git
   cd schedula
   ```

2. Create `.env` and add:
   ```
   GOOGLE_API_KEY="your-gemini-key"
   SERVICE_ACCOUNT_JSON_BASE64="your-base64-service-json"
   CALENDAR_ID="CalendarID@group.calendar.google.com
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

---

### 💬 Frontend (Streamlit)

1. Go to `frontend/` folder:
   ```bash
   cd frontend
   ```

2. Run Streamlit app:
   ```bash
   streamlit run app.py
   ```

---

## 🌍 Deployment

### 🔹 Backend (Render)

- Connect GitHub repo
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn main:app --host=0.0.0.0 --port=10000`
- Add environment variables from `.env`

### 🔹 Frontend (Streamlit Cloud)

- Deploy `frontend/app.py`
- Done!

---

## 📁 Project Structure

```
Schedula/
├── backend/
│   ├── main.py
│   ├── agent.py
│   ├── calendar_utils.py
│   ├── service.json        # (ignored with .gitignore and encoded via .env)
│   └── .env                # (Not Commited)
│
├── frontend/
│   └── app.py              # Streamlit frontend
│
├── .gitignore
├── requirements.txt        # For both frontend & backend
├── README.md

```

---

## 🙋‍♂️ Author

Made with ❤️ by Dinesh Chaudhari

