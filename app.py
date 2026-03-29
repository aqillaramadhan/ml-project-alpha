import streamlit as st
import pandas as pd
import pickle

# 1. Load Model dari toples Pickle
with open('model_churn.pkl', 'rb') as f:
    paket = pickle.load(f)

model = paket['model']
fitur = paket['fitur']

# 2. Desain Tampilan Web
st.title("🔮 Telco Customer Churn Predictor")
st.write("Aplikasi AI interaktif untuk memprediksi apakah pelanggan akan kabur atau setia.")
st.markdown("---")

# 3. Form Input Data Pelanggan
col1, col2 = st.columns(2)

with col1:
    tenure = st.number_input("Lama Berlangganan (Bulan)", min_value=0, max_value=100, value=12)
    monthly_charges = st.number_input("Tagihan Bulanan ($)", min_value=0.0, max_value=200.0, value=50.0)

with col2:
    contract = st.selectbox("Tipe Kontrak", ["Month-to-month", "One year", "Two year"])
    tech_support = st.selectbox("Punya Tech Support?", ["Yes", "No"])

st.markdown("---")

# 4. Tombol Eksekusi
if st.button("🚀 Prediksi Sekarang!"):
    # Bikin kerangka data kosong sesuai format XGBoost lu
    input_data = pd.DataFrame(columns=fitur)
    input_data.loc[0] = 0 # Isi angka 0 semua sebagai default
    
    # Timpa default dengan inputan user
    input_data['Tenure_Months'] = tenure
    input_data['Monthly_Charges'] = monthly_charges
    input_data['Total_Charges'] = tenure * monthly_charges
    
    # Logic One-Hot Encoding manual sesuai pilihan user
    if contract == "One year" and 'Contract_One year' in fitur: 
        input_data['Contract_One year'] = 1
    elif contract == "Two year" and 'Contract_Two year' in fitur: 
        input_data['Contract_Two year'] = 1
        
    if tech_support == "Yes" and 'Tech_Support_Yes' in fitur:
        input_data['Tech_Support_Yes'] = 1
        
    # Lakukan Prediksi
    prediksi = model.predict(input_data)
    
    # Tampilkan Hasil
    if prediksi[0] == 1:
        st.error("🚨 WADUH! Pelanggan ini kemungkinan besar bakal CHURN (Kabur) pindah ke kompetitor!")
    else:
        st.success("✅ AMAN! Pelanggan ini diprediksi bakal SETIA.")