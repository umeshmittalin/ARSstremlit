
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Auto-Replenishment Bot", layout="wide")

st.title("🚚 Auto-Replenishment Inventory Bot")
st.markdown("Upload your sales & inventory Excel file to get Suggested Order Quantities (SOQ) with optional festival-based uplift.")

# Festival uplift calendar (simple version)
FESTIVAL_UPLIFT = {
    "January": 1.0,
    "February": 1.0,
    "March": 1.0,
    "April": 1.0,
    "May": 1.2,
    "June": 1.2,
    "July": 1.0,
    "August": 1.3,
    "September": 1.2,
    "October": 1.5,
    "November": 1.5,
    "December": 1.1
}

uploaded_file = st.file_uploader("Upload Excel File", type=[".xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        st.subheader("📃 Raw Data Preview")
        st.dataframe(df.head(), use_container_width=True)

        if "Stock" not in df.columns or "Avg_Monthly_Sales" not in df.columns:
            st.error("Excel must contain at least 'SKU', 'Distributor', 'Stock', 'Avg_Monthly_Sales'.")
        else:
            df['Norm_Days'] = df.get('Norm_Days', 30)
            df['Uplift_Factor'] = df.get('Uplift_Factor', 1.0)

            current_month = datetime.today().strftime('%B')
            festival_uplift = FESTIVAL_UPLIFT.get(current_month, 1.0)
            df['Final_Uplift'] = df['Uplift_Factor'] * festival_uplift

            df['Forecasted_Demand'] = df['Avg_Monthly_Sales'] * df['Final_Uplift']
            df['SOQ'] = (df['Forecasted_Demand'] - df['Stock']).clip(lower=0).round(0)

            st.subheader("📊 Suggested Orders (with Festival Uplift)")
            st.dataframe(df[['SKU', 'Distributor', 'Stock', 'Avg_Monthly_Sales', 'Uplift_Factor', 'Final_Uplift', 'SOQ']], use_container_width=True)

            st.download_button(
                label="📄 Download SOQ Excel",
                data=df.to_excel(index=False, engine='openpyxl'),
                file_name=f"SOQ_Output_{datetime.today().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"Error reading file: {e}")
else:
    st.info("Please upload a valid Excel file to begin.")
