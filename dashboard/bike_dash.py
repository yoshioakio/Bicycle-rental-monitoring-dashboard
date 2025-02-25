import os
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>Analisis Data Penyewaan Sepeda</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>by Fajri Haryanto | muhamadfajri2804@gmail.com | mijimo</p>", unsafe_allow_html=True)

# Masukan file data
csv_path = os.path.join(os.path.dirname(__file__), "bike.csv")
bike_df = pd.read_csv(csv_path)

# Filter data berdasarkan rentang tanggal
bike_df['dteday'] = pd.to_datetime(bike_df['dteday'])
st.sidebar.header("Filter Tanggal")
tanggal_mulai = st.sidebar.date_input("Tanggal Mulai", bike_df['dteday'].min())
tanggal_akhir = st.sidebar.date_input("Tanggal Akhir", bike_df['dteday'].max())

filtered_df = bike_df[(bike_df['dteday'] >= pd.Timestamp(tanggal_mulai)) & 
                           (bike_df['dteday'] <= pd.Timestamp(tanggal_akhir))]

# Buat Tampilkan Grafik
def display_graph(figure):
    st.pyplot(figure)

# 1️⃣ Bagaimana Tren Penyewaan Sepeda Sepanjang Hari? (Line Chart)
st.subheader("1️⃣ Grafik Tren Penyewaan Sepeda Sepanjang Hari")
plt.figure(figsize=(12, 5))
sns.lineplot(x='hr', y='cnt_hour', data=filtered_df, marker='o', markersize=8, markevery=4, linestyle='-', color='b')
plt.xlabel('Jam')
plt.ylabel('Jumlah rata-rata Penyewaan')
plt.title('Grafik Tren Penyewaan Sepeda Sepanjang Hari')
plt.grid(True)
display_graph(plt)

# 2️⃣ Bagaimana Pola Penyewaan Sepeda Selama Perminggu dan Perbulannya? (Bar Chart)
st.subheader("2️⃣ Pola Penyewaan Sepeda per Hari dalam Seminggu dan Bulan")
filtered_df['weekday_day'] = filtered_df['dteday'].dt.weekday  # Get weekday (0=Monday, 6=Sunday)
filtered_df['mnth_day'] = filtered_df['dteday'].dt.month  # Get month (1=January, 12=December)

weekday_counts = filtered_df.groupby('weekday_day', observed=False)['cnt_hour'].sum().reset_index()
month_counts = filtered_df.groupby('mnth_day', observed=False)['cnt_hour'].sum().reset_index()
top3_weekday = weekday_counts.nlargest(3, 'cnt_hour')['weekday_day'].values
top3_month = month_counts.nlargest(3, 'cnt_hour')['mnth_day'].values

# Visualisi grafik
base_color = '#f4a582' 
highlight_color = '#b2182b'  
weekday_colors = [highlight_color if x in top3_weekday else base_color for x in weekday_counts['weekday_day']]
month_colors = [highlight_color if x in top3_month else base_color for x in month_counts['mnth_day']]

plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
sns.barplot(x='weekday_day', y='cnt_hour', hue='weekday_day', data=weekday_counts, palette=weekday_colors, legend=False)
plt.title("Pola Penyewaan Sepeda per Hari dalam Seminggu")
plt.xlabel("Hari dalam Seminggu (mulai dari minggu 0 sampai sabtu 6)")
plt.ylabel("Jumlah Penyewaan")

plt.subplot(1, 2, 2)
sns.barplot(x='mnth_day', y='cnt_hour', hue='mnth_day', data=month_counts, palette=month_colors, legend=False)
plt.title("Pola Penyewaan Sepeda per Bulan")
plt.xlabel("Bulan")
plt.ylabel("Jumlah Penyewaan")
plt.tight_layout()
display_graph(plt)

# 3️⃣ Bagaimana Distribusi Penyewaan Sepeda Berdasarkan Musim? (Pie Chart)
st.subheader("3️⃣ Distribusi Penyewaan Berdasarkan Musim")
season_counts = filtered_df.groupby('season_day', observed=False)['cnt_hour'].sum()
season_counts = season_counts[season_counts > 0]
custom_colors = ['#488f31', '#86b970', '#f7e384', '#f09452']
season_labels = {1: 'Musim Semi (Spring)', 2: 'Musim Panas (Summer)', 3: 'Musim Gugur (Fall)', 4: 'Musim Dingin (Winter)'}
season_labels_mapped = [season_labels[s] for s in season_counts.index]
col1, col2 = st.columns(2)

# Menampilkan Pie Chart di kolom pertama (tanpa label)
with col1:
    plt.figure(figsize=(8, 8))
    plt.pie(season_counts, autopct='%1.1f%%', colors=custom_colors[:len(season_counts)], startangle=140)
    plt.title('Distribusi Penyewaan Sepeda Berdasarkan Musim')
    plt.legend(title='Musim', labels=season_labels_mapped, loc="upper right")
    display_graph(plt)

# Menampilkan distribusi penyewaan dalam bentuk teks di kolom kedua
with col2:
    st.subheader("Jumlah Distribusi Penyewaan Sepeda Berdasarkan Musim")
    for season, count in zip(season_labels_mapped, season_counts):
        st.write(f"{season}: {count} Penyewaan")

# 4️⃣ Bagaimana Perbandingan Penyewaan Sepeda Antara Pengguna Kasual dan Terdaftar? (Line Chart)
st.subheader("4️⃣ Perbandingan Penyewaan Sepeda: Casual vs Registered")
plt.figure(figsize=(12, 5))
sns.lineplot(x='hr', y='casual_hour', data=filtered_df, label='Casual', marker='o', markevery=4, color='r')
sns.lineplot(x='hr', y='registered_hour', data=filtered_df, label='Registered', marker='o', markevery=4, color='g')
plt.xlabel('Jam')
plt.ylabel('Jumlah Penyewaan')
plt.title('Distribusi Penyewaan Sepeda: Casual vs Registered Users')
plt.legend()
plt.grid(True)
display_graph(plt)

# 5️⃣ Pada Hari Apa Penyewaan Sepeda Mencapai Jumlah Tertinggi dan Terendah? (Bar Chart)
st.subheader("5️⃣ Penyewaan Sepeda Tertinggi dan Terendah")
daily_rentals = filtered_df.groupby('dteday')['cnt_day'].first().reset_index()

top10_days = daily_rentals.nlargest(10, 'cnt_day').reset_index(drop=True)
plt.figure(figsize=(14, 5))
plt.subplot(1, 2, 1)
sns.barplot(x=top10_days.index, y='cnt_day', data=top10_days, color='orange')
plt.title('Top 10 Hari dengan Penyewaan Tertinggi')
plt.xlabel('Hari')
plt.ylabel('Jumlah Penyewaan')
plt.xticks(ticks=top10_days.index, labels=[d.strftime('%Y-%m-%d') for d in top10_days['dteday']], rotation=45)

bottom10_days = daily_rentals.nsmallest(10, 'cnt_day').reset_index(drop=True)
plt.subplot(1, 2, 2)
sns.barplot(x=bottom10_days.index, y='cnt_day', data=bottom10_days, color='lightgreen')
plt.title('Top 10 Hari dengan Penyewaan Terendah')
plt.xlabel('Hari')
plt.ylabel('Jumlah Penyewaan')
plt.xticks(ticks=bottom10_days.index, labels=[d.strftime('%Y-%m-%d') for d in bottom10_days['dteday']], rotation=45)
plt.tight_layout()
display_graph(plt)

# 6️⃣ Bagaimana Perilaku Penyewaan Pelanggan Berdasarkan RFM Analysis? (Bar Chart - Histograms)
st.subheader("6️⃣ Pola Perilaku Penyewaan sepedah Berdasarkan RFM Analysis?")
rfm_df = filtered_df.groupby('dteday').agg({'cnt_hour': 'sum', 'casual_hour': 'sum', 'registered_hour': 'sum'}).reset_index()
rfm_df['Recency'] = (rfm_df['dteday'].max() - rfm_df['dteday']).dt.days
rfm_df['Frequency'] = rfm_df['casual_hour'] + rfm_df['registered_hour']
rfm_df['Monetary'] = rfm_df['cnt_hour']

fig, axes = plt.subplots(1, 3, figsize=(18, 5))
sns.histplot(rfm_df['Recency'], bins=20, kde=True, ax=axes[0], color='skyblue')
axes[0].set_title('Distribusi Recency (Hari Sejak Terakhir Menyewa)')

sns.histplot(rfm_df['Frequency'], bins=20, kde=True, ax=axes[1], color='lightcoral')
axes[1].set_title('Distribusi Frequency (Frekuensi Penyewaan)')

sns.histplot(rfm_df['Monetary'], bins=20, kde=True, ax=axes[2], color='limegreen')
axes[2].set_title('Distribusi Monetary (Total Penyewaan)')
display_graph(plt)

# 7️⃣ Bagaimana Pola Penyewaan Sepeda Berdasarkan Kategori Waktu? (Horizontal Bar Chart)
st.subheader("7️⃣ Pola Penyewaan Sepeda Berdasarkan Kategori Waktu")
def kategori_waktu(jam):
    if 0 <= jam <= 4:
        return "Tengah Malam"
    elif 5 <= jam <= 10:
        return "Pagi"
    elif 11 <= jam <= 14:
        return "Siang"
    elif 15 <= jam <= 18:
        return "Sore"
    else:
        return "Malam"
    
filtered_df['Kategori Waktu'] = filtered_df['hr'].apply(kategori_waktu)
pola_waktu_df = filtered_df.groupby('Kategori Waktu')['cnt_hour'].sum().reset_index()
pola_waktu_df.rename(columns={'cnt_hour': 'Jumlah Penyewa'}, inplace=True)
kategori_urutan = ["Tengah Malam", "Pagi", "Siang", "Sore", "Malam"]
pola_waktu_df['Kategori Waktu'] = pd.Categorical(pola_waktu_df['Kategori Waktu'], categories=kategori_urutan, ordered=True)
pola_waktu_df = pola_waktu_df.sort_values('Kategori Waktu')
custom_colors = ['#de425b', '#d2c69e', '#85a776', '#488f31', '#d48d5c']

# Grafik Pola Penyewaan Sepeda Berdasarkan Waktu
plt.figure(figsize=(10, 6))
sns.barplot(y='Kategori Waktu', x='Jumlah Penyewa', hue='Kategori Waktu', data=pola_waktu_df, palette=custom_colors, legend=False)
plt.title("Pola Penyewaan Sepeda Berdasarkan Waktu", fontsize=14, fontweight="bold")
plt.ylabel("Kategori Waktu")
plt.xlabel("Total Penyewaan")
display_graph(plt)

# Menambahkan Tabel Penyewaan Sepeda Berdasarkan Waktu
fig, ax = plt.subplots(figsize=(8, 2))
ax.axis('off')  
table = ax.table(cellText=pola_waktu_df.values.tolist(), colLabels=pola_waktu_df.columns, loc='center', cellLoc='center')

for (i, j), cell in table.get_celld().items():
    if i == 0:  
        cell.set_text_props(weight='bold')
        cell.set_facecolor('#4CAF50')  
    else:
        cell.set_facecolor('#f9f9f9')  

plt.title("Pola Penyewaan Sepeda Berdasarkan Waktu", fontsize=12, fontweight="bold", pad=10)
st.pyplot(fig)
