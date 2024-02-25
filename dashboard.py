import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def create_daily_user_df(df):
    daily_user_df = df.resample(rule='D', on='dteday').agg({
        "cnt": "sum",
        "casual" : "sum",
        "registered" : "sum"
    })
    daily_user_df = daily_user_df.reset_index()
    daily_user_df.rename(columns={
        "cnt": "Total_Jumlah_Pengguna",
        "casual" : "Pengguna_Biasa",
        "registered" : "Pengguna_Terdaftar"
    }, inplace=True)
    
    return daily_user_df

def create_sum_user_month_df(df):
    sum_user_in_month = df.groupby("mnth").cnt.sum().sort_values(ascending=False).reset_index()
    return sum_user_in_month

def create_sum_user_in_season(df):
    sum_user_in_season = df.groupby("season").cnt.sum().sort_values(ascending=False).reset_index()
    return sum_user_in_season

def create_sum_user_in_hours(df):
    sum_user_in_hour = df.groupby('hr').cnt.sum().reset_index()
    return sum_user_in_hour

hour_df = pd.read_csv("hour.csv")

datetime_columns = ["dteday"]
hour_df.sort_values(by="dteday", inplace=True)
hour_df.reset_index(inplace=True)
 
for column in datetime_columns:
    hour_df[column] = pd.to_datetime(hour_df[column])

min_date = hour_df["dteday"].min()
max_date = hour_df["dteday"].max()


with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("bike.jpg")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = hour_df[(hour_df["dteday"] >= str(start_date)) & 
                (hour_df["dteday"] <= str(end_date))]

daily_user_df = create_daily_user_df(main_df)
sum_user_in_month = create_sum_user_month_df(main_df)
sum_user_in_season = create_sum_user_in_season(main_df)
sum_user_in_hour = create_sum_user_in_hours(main_df)

st.header('Sharing Bike Dashboard :sparkles:')

st.subheader('Daily Users')
 
col1, col2, col3 = st.columns(3)
with col1:
    total_user = daily_user_df.Total_Jumlah_Pengguna.sum()
    st.metric("Total Pengguna", value= total_user)
with col2:
    total_user = daily_user_df.Pengguna_Biasa.sum()
    st.metric("Pengguna Biasa", value= total_user)
with col3:
    total_user = daily_user_df.Pengguna_Terdaftar.sum()
    st.metric("Pengguna Terdaftar", value= total_user)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_user_df["dteday"],
    daily_user_df["Total_Jumlah_Pengguna"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

st.subheader("Jumlah Pengguna Setiap Jam")
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    sum_user_in_hour["hr"],
    sum_user_in_hour["cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.set_ylabel("Jumalah Pengguna", fontsize=20, rotation=90)
ax.set_xlabel("Format 24 Jam", fontsize=20)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

st.subheader("Bulan dengan Jumlah Pengguna Terbanyak")
fig, ax = plt.subplots(figsize=(35, 15))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(x="mnth", y="cnt", data=sum_user_in_month.head(12), palette=colors)
ax.set_ylabel("Jumalah Pengguna", fontsize=30, rotation=90)
ax.set_xlabel("Bulan", fontsize=30)
ax.set_title("Pengguna Per Bulan", loc="center", fontsize=50)
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=30)
st.pyplot(fig)

st.subheader("Frekuensi Pengguna Sharing Bike di Setiap Musim")
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
fig, ax = plt.subplots(figsize=(35, 15))
sns.barplot(x='season', y='cnt', data=sum_user_in_season.head(4), palette=colors )
ax.set_ylabel("Jumalah Pengguna", fontsize=30, rotation=90)
ax.set_xlabel("Musim", fontsize=30)
ax.set_title("Jumlah Pengguna di Setiap Musim", loc="center", fontsize=50)
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=30)
# season = ["springer","summer", "fall", "winter"]
# ax.set_xticks(sum_user_in_season['cnt'],season)
st.pyplot(fig)

