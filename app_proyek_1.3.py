import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
    url1 = 'https://raw.githubusercontent.com/TrimoA/Dataset-Analisis-Data/refs/heads/main/day.csv'
    url2 = 'https://raw.githubusercontent.com/TrimoA/Dataset-Analisis-Data/refs/heads/main/hour.csv'
    day_df = pd.read_csv(url1, parse_dates=['dteday'])
    hour_df = pd.read_csv(url2, parse_dates=['dteday'])
    return day_df, hour_df

day_df, hour_df = load_data()

#Dashboard UI
st.title('Dashboard Analisis Penyewaan Sepeda')

with st.sidebar:
    #Menambahkan logo perusahaan
    st.image('https://github.com/TrimoA/Dataset-Analisis-Data/raw/main/Logo sepeda.png')
    #Pilih rentang tanggal
    min_date = day_df['dteday'].min()
    max_date = day_df['dteday'].max()
    start_date, end_date = st.sidebar.date_input('Pilih Rentang Waktu', [min_date, max_date], min_value=min_date, max_value=max_date)

#Filter data berdasarkan tanggal yang dipilih
day_df_filtered = day_df[(day_df['dteday'] >= pd.to_datetime(start_date)) & (day_df['dteday'] <= pd.to_datetime(end_date))]
hour_df_filtered = hour_df[(hour_df['dteday'] >= pd.to_datetime(start_date)) & (hour_df['dteday'] <= pd.to_datetime(end_date))]

#Membuat tabs
tab1, tab2, tab3= st.tabs(['Tren Penyewaan Sepeda per Jam', 'Perbandingan Hari Biasa & Hari Libur', 'Penyewaan Berdasarkan Musim'])

#Tab 1: Visualisasi Tren Penyewaan Sepeda per jam
tab1.subheader('Tren Penyewaan Sepeda per Jam')
hourly_rentals = hour_df_filtered.groupby('hr')['cnt'].mean()
fig, ax = plt.subplots(figsize=(10, 5))
hourly_rentals.index = hourly_rentals.index.astype(str).str.zfill(2)
ax.plot(hourly_rentals.index, hourly_rentals.values, marker='o', markersize=8,
         markerfacecolor='#FFA500', markeredgecolor='#000000', linestyle='--',
         linewidth=2, color='#00008B', alpha=0.8, label='Hourly Rentals')
ax.set_xlabel('Jam')
ax.set_ylabel('Jumlah Penyewaan')
ax.set_title('Penyewaan Sepeda Berdasarkan Jam')
tab1.pyplot(fig)

#Tab 2: Perbandingan Hari Biasa & Hari Libur
tab2.subheader('Perbandingan Penyewaan Sepeda: Hari Biasa & Hari Libur')
holiday_rentals = day_df_filtered.groupby('holiday')['cnt'].mean()
holiday_labels = {0: 'Hari Biasa', 1: 'Hari Libur'}
fig, ax = plt.subplots(figsize=(6, 4))
colors =['#3366FF', '#FF6600']
ax.bar(holiday_rentals.index, holiday_rentals.values, tick_label=[holiday_labels[h] for h in holiday_rentals.index],
       color=colors)
ax.set_xlabel('Kategori')
ax.set_ylabel('Rata-rata Penyewaan')
ax.set_title('Penyewaan Sepeda: Hari Biasa & Hari Libur')
tab2.pyplot(fig)

#Tab 3: Penyewaan Sepeda Berdasarkan Musim
tab3.subheader('Penyewaan Sepeda Berdasarkan Musim')
seasonal_rentals = day_df_filtered.groupby('season')['cnt'].mean()
season_labels = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
fig, ax = plt.subplots(figsize=(10, 7))
colors = ['#33FF57', '#FFD700', '#FFA500', '#3357FF']
ax.bar(seasonal_rentals.index, seasonal_rentals.values, tick_label=[season_labels[s] for s in seasonal_rentals.index],color=colors)
ax.set_xlabel('Musim')
ax.set_ylabel('Rata-rata Penyewaan')
ax.set_title('Penyewaan Sepeda Berdasarkan Musim')
tab3.pyplot(fig)
