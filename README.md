
# 📦 Auto-Replenishment Inventory Bot (FMCG Distributors)

This Streamlit app calculates Suggested Order Quantities (SOQ) for FMCG distributors based on past sales, stock levels, and seasonal uplift factors.

## 🚀 Features
- Upload Excel sheets with distributor-wise sales & stock data
- Auto-generates SOQ using uplifted forecasts
- Download processed results in Excel format
- Ideal for CPG/FMCG supply chain optimization

## 📁 Sample Input Columns
- `SKU`
- `Distributor`
- `Stock`
- `Avg_Monthly_Sales`
- `Uplift_Factor` *(optional, default is 1.0)*

## 💡 Example Calculation
```
SOQ = (Avg_Monthly_Sales × Uplift_Factor × Festival_Uplift) - Stock
```

## 🧪 Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then visit: `http://localhost:8501`

## ☁️ Deploy on Streamlit Cloud
1. Fork or clone this repo
2. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect your GitHub account and deploy this app

## 📄 License
MIT License
