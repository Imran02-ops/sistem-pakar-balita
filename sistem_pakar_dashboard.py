import streamlit as st
import matplotlib.pyplot as plt

# ==========================================================
# SISTEM PAKAR DIAGNOSA PENYAKIT MENULAR PADA BALITA
# Dashboard Interaktif (Streamlit)
# Berdasarkan Jurnal Afdal & Humani (2020)
# ==========================================================

GEJALA = {
    "G01": "Suhu badan di atas 38°C",
    "G02": "Mata merah dan berair",
    "G03": "Batuk",
    "G04": "Pilek",
    "G05": "Bercak putih di dalam mulut",
    "G06": "Kelainan kemerahan di kulit",
    "G07": "Ruam coklat kemerahan seluruh tubuh",
    "G08": "Ruam memudar hari ke-5 atau ke-6",
    "G09": "Demam ringan (bawah 38°C)",
    "G10": "Sakit kepala",
    "G11": "Kelenjar getah bening bengkak di leher",
    "G12": "Ruam merah muda 24-48 jam menyeluruh",
    "G13": "Bintik merah kecil",
    "G14": "Ruam memudar hari ke-3",
    "G15": "Mual",
    "G16": "Ruam di kulit",
    "G17": "Bekas cacar air membentuk cekungan",
    "G18": "Ruam terasa gatal",
    "G19": "Gangguan pernapasan",
    "G20": "Pipi anak berwarna merah",
    "G21": "Sakit tenggorokan",
    "G22": "Ruam menyebar ke tubuh/lengan/kaki",
    "G23": "Demam turun drastis",
    "G24": "Ruam berwarna merah tua",
    "G25": "Radang tenggorokan",
    "G26": "Tidak nafsu makan",
    "G27": "Diare ringan",
    "G28": "Kejang",
    "G29": "Infeksi sekitar hidung dan mulut",
    "G30": "Bintik kuning seperti madu",
    "G31": "Bintik pecah dan memerah",
    "G32": "Bintik bernanah dan berkerak",
    "G33": "Demam tinggi mendadak 2–7 hari",
    "G34": "Pendarahan kulit",
    "G35": "Pendarahan gusi",
    "G36": "Mimisan atau BAB berdarah",
    "G37": "Nyeri perut",
    "G38": "Ruam muncul setelah demam",
    "G39": "Muntah",
    "G40": "Kesadaran menurun",
    "G41": "Fase syok, gelisah, lesu"
}

RULES = {
    "Campak (P01)": ["G01","G02","G03","G04","G05","G06","G07","G08"],
    "Rubella (P02)": ["G02","G03","G06","G09","G10","G11","G12","G13","G14"],
    "Cacar Air (P03)": ["G09","G10","G15","G16","G17","G18"],
    "Sindrom Pipi Merah (P04)": ["G03","G04","G09","G19","G20","G21","G22"],
    "Roseola Infantum (P05)": ["G01","G03","G04","G06","G23","G24","G25","G26","G27","G28"],
    "Impetigo (P06)": ["G29","G30","G31","G32"],
    "Demam Berdarah (P07)": ["G01","G03","G15","G33","G34","G35","G36","G37","G38","G39","G40","G41"]
}

PENANGANAN = {
    "Campak (P01)": "Periksa ke dokter anak, isolasi, dan hidrasi cukup.",
    "Rubella (P02)": "Pantau ruam & demam, jaga kebersihan.",
    "Cacar Air (P03)": "Hindari menggaruk, jaga kebersihan kulit.",
    "Sindrom Pipi Merah (P04)": "Istirahat dan hindari kontak dekat dengan anak lain.",
    "Roseola Infantum (P05)": "Pantau suhu & kejang, segera ke dokter bila berat.",
    "Impetigo (P06)": "Gunakan salep antibiotik sesuai resep dokter.",
    "Demam Berdarah (P07)": "Segera ke rumah sakit, pantau cairan & perdarahan."
}

def forward_chaining(gejala_input):
    results = []
    for penyakit, daftar in RULES.items():
        cocok = set(gejala_input).intersection(daftar)
        skor = len(cocok) / len(daftar)
        results.append((penyakit, skor, len(cocok), len(daftar)))
    results.sort(key=lambda x: x[1], reverse=True)
    return results

st.set_page_config(page_title="Sistem Pakar Penyakit Balita", layout="wide")

st.sidebar.title("🩺 Menu Navigasi")
menu = st.sidebar.radio("Pilih Halaman:", ["Beranda", "Diagnosa", "Tentang"])

if menu == "Beranda":
    st.title("🧠 Sistem Pakar Diagnosa Penyakit Menular pada Balita")
    st.markdown('''
    Aplikasi ini merupakan implementasi dari penelitian **Afdal & Humani (2020)**  
    yang menggunakan metode **Forward Chaining** untuk membantu mendiagnosa penyakit menular pada balita.
    ''')
    st.markdown("---")
    st.subheader("🎯 Tujuan")
    st.write("Membantu orang tua mengenali gejala awal penyakit menular pada balita agar dapat melakukan tindakan cepat.")

elif menu == "Diagnosa":
    st.title("🔍 Diagnosa Penyakit Balita")
    st.markdown("Silakan pilih gejala yang terlihat pada balita:")
    col1, col2 = st.columns(2)
    with col1:
        g1 = list(GEJALA.items())[:21]
    with col2:
        g2 = list(GEJALA.items())[21:]
    selected_gejala = []
    with col1:
        for kode, desc in g1:
            if st.checkbox(desc, key=kode):
                selected_gejala.append(kode)
    with col2:
        for kode, desc in g2:
            if st.checkbox(desc, key=kode):
                selected_gejala.append(kode)
    if st.button("💡 Jalankan Diagnosa"):
        if not selected_gejala:
            st.warning("Pilih minimal satu gejala terlebih dahulu.")
        else:
            hasil = forward_chaining(selected_gejala)
            top = hasil[0]
            penyakit_utama = top[0]
            skor = round(top[1]*100, 1)
            st.success(f"**Kemungkinan terbesar:** {penyakit_utama} ({skor}% cocok)")
            st.info(f"💊 Saran: {PENANGANAN[penyakit_utama]}")
            st.markdown("### 📋 Hasil Diagnosa Lengkap")
            st.dataframe({
                "Penyakit": [r[0] for r in hasil],
                "Kecocokan (%)": [round(r[1]*100, 1) for r in hasil],
                "Gejala Cocok": [f"{r[2]}/{r[3]}" for r in hasil]
            })
            st.markdown("### 📊 Visualisasi Kecocokan")
            fig, ax = plt.subplots(figsize=(8,4))
            penyakit = [r[0] for r in hasil]
            skor_list = [r[1]*100 for r in hasil]
            ax.barh(penyakit, skor_list, color="#4dabf7")
            ax.set_xlabel("Tingkat Kecocokan (%)")
            ax.set_title("Grafik Diagnosa Penyakit Balita")
            ax.invert_yaxis()
            for i, s in enumerate(skor_list):
                ax.text(s + 1, i, f"{s:.1f}%", va="center", color="white")
            st.pyplot(fig)

elif menu == "Tentang":
    st.title("ℹ️ Tentang Aplikasi")
    st.markdown('''
    **Sistem Pakar Diagnosa Awal Penyakit Menular pada Balita (Web App)**  

    Berdasarkan jurnal:  
    > Afdal, M., & Humani, D. G. (2020).  
    > *Aplikasi Sistem Pakar Diagnosa Awal Penyakit Menular pada Balita Berbasis Android.*  
    > Jurnal Ilmiah Rekayasa dan Manajemen Sistem Informasi, 6(1).

    ⚠️ *Aplikasi ini bersifat edukatif dan bukan pengganti diagnosis medis profesional.*
    ''')
