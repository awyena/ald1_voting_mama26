import streamlit as st
import requests

# Set halaman ke mode lebar & judul
st.set_page_config(
    page_title="ALD1 MAMA 2026 VOTING ROUND 1",
    page_icon="🔥",
    layout="wide"
)

# Judul Utama
st.markdown("<h1 style='text-align: center;'>【ALD1 MAMA 2026 VOTING ROUND 1】</h1>", unsafe_allow_html=True)

# Masukkan URL Web App Google Apps Script Anda di sini (format JSON)
GAS_API_URL = "PASANG_LINK_WEB_APP_GOOGLE_SCRIPT_ANDA_DI_SINI"

@st.cache_data(ttl=30) # Refresh data setiap 30 detik
def fetch_data():
    try:
        res = requests.get(GAS_API_URL)
        return res.json()
    except:
        return None

data = fetch_data()

if data:
    st.caption(f"Terakhir Diperbarui: {data.get('lastUpdated', '-')}")

    # Section 1: Ringkasan Metrics Utama
    c1, c2, c3 = st.columns(3)
    c1.metric("Grand Target Votes", f"{data.get('grandTarget', 0):,}")
    c2.metric("Grand Total Votes", f"{data.get('grandCurrent', 0):,}")
    c3.metric("Grand Total Deficit", f"{data.get('grandDeficit', 0):,}")

    st.divider()

    # Section 2: Collab Per-Artis (Grid Ke Samping)
    collabs = data.get('collabs', [])
    if collabs:
        cols = st.columns(len(collabs))
        for idx, collab in enumerate(collabs):
            with cols[idx]:
                # Tampilkan Gambar & Nama Artis
                st.image(collab.get('image'), width=120)
                st.subheader(collab.get('name'))
                
                # Progress Bar
                progress_val = float(collab.get('progress', 0)) / 100.0
                st.progress(min(1.0, max(0.0, progress_val)))
                st.caption(f"Progres: {collab.get('progress')}% | Target: {collab.get('target'):,}")

                # Tabel Leaderboard User
                users = collab.get('users', [])
                if users:
                    st.dataframe(
                        users,
                        column_config={
                            "username": "Username / Account",
                            "totalVotes": "Total Votes"
                        },
                        hide_index=True,
                        use_container_width=True
                    )
                else:
                    st.info("Belum ada data user.")
else:
    st.error("Gagal mengambil data dari Google Sheets. Pastikan URL API sudah benar.")