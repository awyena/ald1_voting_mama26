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

# URL API Google Apps Script
GAS_API_URL = "https://script.google.com/macros/s/AKfycbwUI3UPKZ669AWqI-Voyc6OVRglUGZiIegPx1CSbMg0ZfNK6vuB62AlzRuBn-Ox2GXDfA/exec"

@st.cache_data(ttl=30) # Refresh data setiap 30 detik
def fetch_data():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        # Mengikuti redirect otomatis Google Apps Script dan mengirimkan User-Agent
        res = requests.get(GAS_API_URL, headers=headers, allow_redirects=True, timeout=15)
        
        # Cek jika status HTTP bukan 200 OK
        if res.status_code != 200:
            st.error(f"HTTP Error Status: {res.status_code}")
            return None
            
        return res.json()
    except Exception as e:
        # Tampilkan pesan error yang spesifik agar mudah di-debug
        st.error(f"Detail Error: {str(e)}")
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
                if collab.get('image'):
                    st.image(collab.get('image'), width=120)
                st.subheader(collab.get('name', 'Collab'))
                
                # Progress Bar
                try:
                    progress_val = float(collab.get('progress', 0)) / 100.0
                except (ValueError, TypeError):
                    progress_val = 0.0
                    
                st.progress(min(1.0, max(0.0, progress_val)))
                st.caption(f"Progres: {collab.get('progress', 0)}% | Target: {collab.get('target', 0):,}")

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
    st.error("Gagal mengambil data dari Google Sheets. Periksa detail pesan di atas.")
