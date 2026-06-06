# 📊 Analytics Pro — Streamlit Dashboard

A beautiful, interactive **business analytics dashboard** built with Python and Streamlit.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.58-FF4B4B?logo=streamlit)
![Plotly](https://img.shields.io/badge/Plotly-6.x-3F4F75?logo=plotly)

---

## ✨ Features

| Page | Description |
|------|-------------|
| 📊 **Overview** | KPI metrics, revenue area chart, donut chart, profit margin heatmap |
| 📈 **Sales Deep Dive** | Weekly bar charts by region, bubble chart, box plots |
| 👥 **User Insights** | Age vs. spend scatter, satisfaction distribution, segment breakdown |
| 🌍 **Regional Map** | Interactive choropleth world map with switchable metrics |

- **Dark glassmorphism** UI with purple/indigo gradient
- **Live sidebar filters** — date range, categories, regions
- Fully interactive **Plotly** charts (zoom, hover, legend toggle)
- Generated with synthetic data (no external API needed)

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/analytics-pro-dashboard.git
cd analytics-pro-dashboard
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
python -m streamlit run app.py
```

Then open **http://localhost:8501** in your browser.

---

## 📦 Tech Stack

- [Streamlit](https://streamlit.io/) — web app framework
- [Plotly](https://plotly.com/python/) — interactive charts
- [Pandas](https://pandas.pydata.org/) — data manipulation
- [NumPy](https://numpy.org/) — numerical computing

---

## 📁 Project Structure

```
analytics-pro-dashboard/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

---

## 🌐 Deploy to Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set **Main file path** to `app.py`
5. Click **Deploy** 🚀

---

## 📄 License

MIT License — feel free to use and modify.
