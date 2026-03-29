import streamlit as st
import pandas as pd
import pickle

# --- 0. KONFIGURASI HALAMAN (HARUS PALING ATAS) ---
st.set_page_config(page_title="Telco Churn Predictor", page_icon="🌲", layout="centered")

# --- 1. SUNTIKAN DESAIN "NORDIC FOREST" ---
css_nordic_forest = """
<style>
    /* Background utama (Hijau Hutan Super Gelap) */
    .stApp {
        background-color: #0E1F19; 
    }
    
    /* Warna Teks Normal (Putih Kehijauan/Abu) */
    p, span, label, div {
        color: #E0EAE5 !important;
    }

    /* Warna Judul (Hijau Mint Terang) */
    h1, h2, h3 {
        color: #A7F3D0 !important; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 800;
    }

    /* Styling Kotak Input Data */
    .stNumberInput > div > div > input, 
    .stSelectbox > div > div > div {
        background-color: #1A362D !important; /* Hijau tua elegan */
        color: #FFFFFF !important;
        border-radius: 8px;
        border: 1px solid #2A5245 !important;
    }

    /* Styling Tombol Prediksi Super Kece */
    .stButton > button {
        background-color: #10B981; /* Hijau Zamrud */
        color: #000000 !important;
        font-weight: 900;
        border-radius: 8px;
        border: none;
        padding: 12px 24px;
        transition: all 0.3s ease;
        width: 100%; /* Biar tombolnya panjang penuh */
    }
    
    /* Efek Animasi Pas Mouse Lewat di Atas Tombol */
    .stButton > button:hover {
        background-color: #34D399; /* Mint nyala */
        color: #000000 !important;
        transform: scale(1.02);
        box-shadow: 0px 4px 15px rgba(52, 211, 153, 0.4);
    }

    /* Garis pembatas elegan */
    hr {
        border-color: #2A5245;
    }
</style>
"""
st.markdown(css_nordic_forest, unsafe_allow_html=True)

# --- MULAI DARI SINI KODINGANNYA SAMA KAYAK SEBELUMNYA ---

# 2. Load Model dari toples Pickle
with open('model_churn.pkl', 'rb') as f:
    paket = pickle.load(f)

model = paket['model']
fitur = paket['fitur']

# 3. Desain Tampilan Web
st.title("🌲 Telco Customer Churn Predictor")
st.write("Aplikasi AI interaktif untuk memprediksi apakah pelanggan akan kabur atau setia.")
st.markdown("---")

# 4. Form Input Data Pelanggan
col1, col2 = st.columns(2)

with col1:
    tenure = st.number_input("Lama Berlangganan (Bulan)", min_value=0, max_value=100, value=12)
    monthly_charges = st.number_input("Tagihan Bulanan ($)", min_value=0.0, max_value=200.0, value=50.0)

with col2:
    contract = st.selectbox("Tipe Kontrak", ["Month-to-month", "One year", "Two year"])
    tech_support = st.selectbox("Punya Tech Support?", ["Yes", "No"])

st.markdown("---")

# 5. Tombol Eksekusi
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