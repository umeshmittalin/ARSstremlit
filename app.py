
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Auto-Replenishment Bot", layout="wide")

st.title("🚚 Auto-Replenishment Inventory Bot")
st.markdown("Upload your sales & inventory Excel file to get Suggested Order Quantities (SOQ).")

# Upload Excel file
uploaded_file = st.file_uploader("Upload Excel File", type=[".xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        # Display raw input
        st.subheader("📃 Raw Data Preview")
        st.dataframe(df.head(), use_container_width=True)

        # Add default norm and uplift if missing
        if "Stock" not in df.columns or "Avg_Monthly_Sales" not in df.columns:
            st.error("Excel must contain at least 'SKU', 'Distributor', 'Stock', 'Avg_Monthly_Sales'.")
        else:
            df['Norm_Days'] = df.get('Norm_Days', 30)
            df['Uplift_Factor'] = df.get('Uplift_Factor', 1.0)

            # Calculate suggested order quantity
            df['Forecasted_Demand'] = df['Avg_Monthly_Sales'] * df['Uplift_Factor']
            df['SOQ'] = (df['Forecasted_Demand'] - df['Stock']).clip(lower=0).round(0)

            # Show results
            st.subheader("📊 Suggested Orders")
            st.dataframe(df[['SKU', 'Distributor', 'Stock', 'Avg_Monthly_Sales', 'Uplift_Factor', 'SOQ']], use_container_width=True)

            # Download result
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
