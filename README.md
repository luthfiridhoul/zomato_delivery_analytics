# 🛵 Delivery Time Analytics Dashboard

---

## 🇬🇧 English

**Interactive dashboard for analyzing factors that affect food delivery time.**  
Built with **Streamlit** and **Plotly**, this app provides insights from a food delivery dataset (Zomato) with interactive visualizations and dynamic filters.

---

### 📊 Dataset Description

The main dataset is `processed_zomato_dataset.xlsx`, containing order information, courier profiles, weather, traffic conditions, and other operational details.  
Each row represents one delivery record, containing order info, courier profile, weather & traffic conditions, and operational details.

**Example columns:**
- `Order_Date` → Order date
- `Time_taken (min)` → Delivery time in minutes
- `Weather_conditions` → Weather condition
- `Road_traffic_density` → Traffic density
- `Type_of_order` → Order type
- `Type_of_vehicle` → Vehicle type
- `Delivery_person_Ratings` → Courier rating
- `City` → Delivery city
- `Festival` → Festival indicator (Yes/No)

---

### 🎯 Project Goals

- **Analyze** internal & external factors affecting delivery time.  
- **Provide visual insights** to support operational decisions.  
- **Build an interactive app** for dynamic data exploration.  

---

### 🔍 Data Processing Steps

1. **Data Understanding**  
   - Check data types & missing values.  
   - Ensure important columns are present.  

2. **Data Preprocessing**  
   - Numeric: type casting & missing value imputation.  
   - Categorical: text standardization & mode imputation.  
   - Calculate delivery distance (Haversine) if coordinates are available.  

3. **EDA (Exploratory Data Analysis)**  
   - Monthly delivery time trend.  
   - Weather & traffic combination heatmap.  
   - Delivery time by order type & vehicle type.  
   - Courier rating vs delivery time scatter.  

---

### 🖥️ Dashboard Features

- **KPI Cards**: Average time, total orders, on-time percentage.  
- **Slicers / Filters**: City, festival, weather, traffic.  
- **Monthly Trend Chart**: All month labels displayed.  
- **Heatmap**: Weather & traffic impact on delivery time.  
- **Bar Charts**: Average time by order/vehicle type.  
- **Scatter Plot**: Courier rating vs delivery time.  

---

### 🚀 How to Run

---

### 📂 Project Structure
```
delivery-time-analytics/
├── delivery_dashboard_localxlsx_monthlabels.py   # Streamlit app
├── processed_zomato_dataset.xlsx                 # Dataset
├── requirements.txt                              # Dependencies
└── README.md                                     # Documentation
```

---

### ✨ Technologies
- Python
- Pandas, NumPy
- Plotly
- Streamlit

---

💡 *Created as a Data Analytics portfolio project for food delivery time analysis.*

---

## 🇮🇩 Bahasa Indonesia

**Dashboard interaktif untuk menganalisis faktor-faktor yang mempengaruhi waktu pengiriman makanan.**  
Dibuat menggunakan **Streamlit** dan **Plotly**, aplikasi ini menampilkan insight dari dataset pengiriman makanan (Zomato) dengan visualisasi interaktif dan filter dinamis.

---

### 📊 Deskripsi Dataset

Dataset utama adalah `processed_zomato_dataset.xlsx`, berisi informasi pesanan, profil kurir, kondisi cuaca, lalu lintas, dan detail operasional lainnya.  
Setiap baris mewakili satu catatan pengiriman, berisi informasi pesanan, profil kurir, cuaca, lalu lintas, dan detail operasional.

**Contoh kolom:**
- `Order_Date` → Tanggal pesanan
- `Time_taken (min)` → Lama pengiriman (menit)
- `Weather_conditions` → Kondisi cuaca
- `Road_traffic_density` → Kepadatan lalu lintas
- `Type_of_order` → Jenis pesanan
- `Type_of_vehicle` → Jenis kendaraan
- `Delivery_person_Ratings` → Rating kurir
- `City` → Kota pengiriman
- `Festival` → Apakah saat festival

---

### 🎯 Tujuan Project

- **Menganalisis** faktor internal & eksternal yang mempengaruhi lama pengiriman.  
- **Memberikan insight visual** untuk mendukung keputusan operasional.  
- **Membuat aplikasi interaktif** yang memungkinkan eksplorasi data secara dinamis.  

---

### 🔍 Tahapan Pengolahan Data

1. **Data Understanding**  
   - Memeriksa tipe data & missing values.  
   - Memastikan kolom penting tersedia.  

2. **Data Preprocessing**  
   - Numerik: konversi tipe data, imputasi nilai hilang.  
   - Kategorikal: standardisasi teks, imputasi modus.  
   - Perhitungan jarak pengiriman (Haversine) jika data koordinat tersedia.  

3. **EDA (Exploratory Data Analysis)**  
   - Tren waktu pengiriman per bulan.  
   - Heatmap kombinasi cuaca & lalu lintas.  
   - Perbandingan waktu antar per jenis pesanan & kendaraan.  
   - Scatter hubungan rating kurir & waktu pengiriman.  

---

### 🖥️ Fitur Dashboard

- **KPI Cards**: Rata-rata waktu, total pesanan, persentase tepat waktu.  
- **Slicers / Filters**: Kota, festival, cuaca, lalu lintas.  
- **Monthly Trend Chart**: Label semua bulan ditampilkan.  
- **Heatmap**: Dampak cuaca & lalu lintas terhadap waktu.  
- **Bar Charts**: Rata-rata waktu per jenis pesanan/kendaraan.  
- **Scatter Plot**: Hubungan rating kurir & waktu antar.  

---

### 🚀 Cara Menjalankan

---

### 📂 Struktur Project
```
delivery-time-analytics/
├── delivery_dashboard_localxlsx_monthlabels.py   # Streamlit app
├── processed_zomato_dataset.xlsx                 # Dataset
├── requirements.txt                              # Dependencies
└── README.md                                     # Dokumentasi
```

---

### ✨ Teknologi
- Python
- Pandas, NumPy
- Plotly
- Streamlit

---

💡 *Dibuat sebagai portofolio Data Analytics untuk analisis waktu pengiriman makanan.*

