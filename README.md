## SmartCart — Full-Stack Intelligent Shopping Cart System

SmartCart is a full-stack e-commerce platform built entirely in Python: a 
Flask REST API backed by SQLite, paired with a multi-page Streamlit web app. 
Developed as a graduate Python programming project, it goes well beyond 
basic CRUD — layering in a **web scraping module**, a **machine learning 
sales-forecasting engine**, and an **LLM-powered cart evaluator** on top of 
the core shopping flow.

### Architecture
The backend follows a clean **routes → repository → model** layered design, 
and the frontend is a separate Streamlit multi-page app that talks to it 
purely over HTTP:
- **Backend (Flask)** — routes handle HTTP only; repositories 
  (`ProductRepository`, `CartItemRepository`, `PurchaseRepository`, 
  `AnalysisRepository`, `AIRepository`) own all SQLite access and business 
  logic; models (`Product`, `CartItem`, `Purchase`, `PurchaseItem`) are plain 
  data classes with `to_dict()` / `from_dict()` serialization.
- **Frontend (Streamlit)** — a 5-page app (Products, Cart, Purchases, Web 
  Scraping, Analysis) that consumes the REST API exclusively via `requests`, 
  with no direct database access from the UI layer — a genuine client/server 
  separation rather than a monolithic script.

### Key Features
- **Product catalog** — dynamic filtering (category, price range, name 
  search) and sorting via safe, parameterized SQL, with a Streamlit page 
  offering live sidebar filters (category multiselect, price slider, search).
- **Cart management** — add, update quantity, remove, and clear cart items, 
  with an interactive UI for adjusting quantities and totals in real time.
- **Checkout & order history** — completes purchases by snapshotting cart 
  contents into a `purchases` / `purchase_items` schema, with a UI for 
  browsing past orders and expanding into line-item detail per order.
- **Data analytics dashboard** — a tabbed Streamlit view rendering 
  server-generated Matplotlib charts for top-selling products (overall and 
  per category) and sales forecasts, pulled live from the API.
- **ML-based sales forecasting** — trains a **scikit-learn linear regression 
  model per product category** to predict expected sales by day of week, 
  with MSE evaluation and per-category regression-line visualizations.
- **Live web scraping** — `requests` + `BeautifulSoup` pull real-time 
  competitor pricing, descriptions, and images for a product category from 
  an external retail site, surfaced through a dedicated comparison page.
- **AI cart evaluation** — sends the current cart as a structured prompt to 
  an LLM (Llama 4 via the Groq API) and returns a natural-language quality 
  assessment, displayed inline in the Cart page.

### Tech Stack
`Python` · `Flask` (REST API) · `SQLite` · `Streamlit` (frontend) · `pandas` 
· `scikit-learn` (Linear Regression) · `Matplotlib` · `BeautifulSoup` / 
`requests` (web scraping) · `Groq LLM API` (AI evaluation)

### Why it matters
This project touches nearly every layer a data analyst/data engineer role 
requires day to day: relational schema design and parameterized SQL, REST 
API design with a decoupled client, external data extraction via scraping, 
and turning transactional data into statistics, visualizations, and an 
actual trained ML forecasting model — plus a working UI to make all of it 
usable end to end.
