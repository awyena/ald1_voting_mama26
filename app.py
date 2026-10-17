import streamlit as st
import requests
import re

# Set konfigurasi halaman
st.set_page_config(
    page_title="ALD1 MAMA 2026 VOTING ROUND 1",
    page_icon="🔥",
    layout="wide"
)

# Style Custom CSS untuk tampilan lebih modern
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 800;
        letter-spacing: -1px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>【ALD1 MAMA 2026 VOTING ROUND 1】</h1>", unsafe_allow_html=True)

# URL API Web App Google Apps Script Anda
GAS_API_URL = "https://script.google.com/macros/s/AKfycbwUI3UPKZ669AWqI-Voyc6OVRglUGZiIegPx1CSbMg0ZfNK6vuB62AlzRuBn-Ox2GXDfA/exec"

@st.cache_data(ttl=30) # Refresh otomatis tiap 30 detik
def fetch_data():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        # PENTING: allow_redirects=True agar mengikuti link script.googleusercontent.com
        res = requests.get(GAS_API_URL, headers=headers, allow_redirects=True, timeout=15)
        if res.status_code == 200:
            return res.json()
        else:
            st.error(f"HTTP Status Error: {res.status_code}")
            return None
    except Exception as e:
        st.error(f"Gagal terhubung ke API: {str(e)}")
        return None

data = fetch_data()

if data:
    st.caption(f"🕒 Terakhir Diperbarui: {data.get('lastUpdated', '-')}")

    # --- SECTION 1: METRICS RINGKASAN GLOBAL ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Grand Target Votes", f"{data.get('grandTarget', 0):,}")
    c2.metric("Grand Total Votes", f"{data.get('grandCurrent', 0):,}")
    c3.metric("Grand Deficit", f"{data.get('grandDeficit', 0):,}")

    st.divider()

    # --- SECTION 2: COLLAB PER ARTIS (GRID BERDAMPINGAN KE SAMPING) ---
    collabs = data.get('collabs', [])
    if collabs:
        cols = st.columns(len(collabs))
        
        for idx, collab in enumerate(collabs):
            with cols[idx]:
                # Tampilkan Foto Profil Artis & Nama Collab
                if collab.get('image'):
                    st.image(collab.get('image'), width=140)
                st.subheader(collab.get('name', 'Collab'))
                
                # Progres & Target
                try:
                    prog_float = float(collab.get('progress', 0)) / 100.0
                except:
                    prog_float = 0.0
                
                st.progress(min(1.0, max(0.0, prog_float)))
                st.caption(f"Progres: **{collab.get('progress', 0)}%** | Target: **{collab.get('target', 0):,}** | Defisit: **{collab.get('deficit', 0):,}**")

                # Format & Bersihkan Data User
                raw_users = collab.get('users', [])
                formatted_users = []
                
                for u in raw_users:
                    raw_name = u.get('username', '')
                    # Bersihkan teks tambahan seperti (470 vts) dari nama user agar rapi
                    clean_name = re.sub(r'\s*\(\d+\s*vts\)', '', raw_name, flags=re.IGNORECASE).strip()
                    formatted_users.append({
                        "Username / Account": clean_name,
                        "Total Votes": u.get('totalVotes', 0)
                    })

                if formatted_users:
                    st.dataframe(
                        formatted_users,
                        hide_index=True,
                        use_container_width=True,
                        height=400 # Membuat tabel bisa di-scroll rapi
                    )
                else:
                    st.info("Belum ada data user.")
else:
    st.warning("Memuat data dari Google Sheets...")
