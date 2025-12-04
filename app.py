import streamlit as st
import rumus as r
import fungsi1 as f1
import matplotlib.pyplot as plt
from datetime import datetime

# =========================
# LOGIN
# =========================
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("WELCOME TO KAMI BANG!")
    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == "admin" and pw == "123":
            st.session_state.login = True
            st.success("✅ Login Berhasil!")
            st.rerun()
        else:
            st.error("❌ Username atau Password salah!")

    st.stop()

# =========================
# MENU SIDEBAR (3 MENU)
# =========================
menu = st.sidebar.radio("📋 MENU", ["Menu Utama", "About Us", "Logout"])

# =========================
# QUESTION BOX + SAVE FILE
# =========================
st.sidebar.markdown("---")
st.sidebar.subheader("💬 Any Question?")

pertanyaan = st.sidebar.text_area("Tulis pertanyaan kamu:")

if st.sidebar.button("📩 Kirim"):
    if pertanyaan.strip() == "":
        st.sidebar.warning("⚠️ Pertanyaan tidak boleh kosong!")
    else:
        with open("question_box.txt", "a", encoding="utf-8") as file:
            file.write(f"{datetime.now()} - {pertanyaan}\n")
        st.sidebar.success("✅ Pertanyaan berhasil disimpan!")

# =========================
# SESSION STATE
# =========================
if "step" not in st.session_state:
    st.session_state.step = 1

if "tahun" not in st.session_state:
    st.session_state.tahun = 0

if "data_now" not in st.session_state:
    st.session_state.data_now = {}

if "data_last" not in st.session_state:
    st.session_state.data_last = {}

# =========================================================
# ===================== MENU UTAMA =========================
# =========================================================
if menu == "Menu Utama":
    st.title("KAMI BANG! (Kalkulator Efektivitas Mineral Tambang)")

    # =========================
    # STEP 1 - INPUT TAHUN
    # =========================
    if st.session_state.step == 1:
        st.header("📅 Tahun")
        tahun = st.number_input("Masukkan Tahun Sekarang", step=1)

        if st.button("✅ Simpan & Lanjut ➡️"):
            st.session_state.tahun = int(tahun)
            st.success("✅ Tahun berhasil disimpan")
            st.session_state.step = 2
            st.rerun()

    # =========================
    # STEP 2 - DATA TAHUN INI
    # =========================
    elif st.session_state.step == 2:
        st.header(f"📥 Data Tahun {st.session_state.tahun}")

        mesin = f1.verifikasi2(st.number_input("Jam Mesin per Hari"))
        maintenance = f1.verifikasi2(st.number_input("Jam Maintenance per Hari"))
        bijih = f1.verifikasi2(st.number_input("Bijih per Hari"))
        pekerja = f1.verifikasi2(st.number_input("Jumlah Pekerja"))
        bbm = f1.verifikasi2(st.number_input("BBM (liter) per Jam"))

        if st.button("✅ Simpan & Lanjut ➡️"):
            st.session_state.data_now = {
                "mesin": mesin,
                "maintenance": maintenance,
                "bijih": bijih,
                "pekerja": pekerja,
                "bbm": bbm,
            }
            st.success("✅ Data tahun ini berhasil disimpan")
            st.session_state.step = 3
            st.rerun()

    # =========================
    # STEP 3 - DATA TAHUN LALU
    # =========================
    elif st.session_state.step == 3:
        st.header(f"📥 Data Tahun {st.session_state.tahun - 1}")

        mesin = f1.verifikasi2(st.number_input("Jam Mesin per Hari"))
        maintenance = f1.verifikasi2(st.number_input("Jam Maintenance per Hari"))
        bijih = f1.verifikasi2(st.number_input("Bijih per Hari"))
        pekerja = f1.verifikasi2(st.number_input("Jumlah Pekerja"))
        bbm = f1.verifikasi2(st.number_input("BBM per Jam"))

        if st.button("✅ Simpan & Lanjut ➡️"):
            st.session_state.data_last = {
                "mesin": mesin,
                "maintenance": maintenance,
                "bijih": bijih,
                "pekerja": pekerja,
                "bbm": bbm,
            }
            st.success("✅ Data tahun lalu berhasil disimpan")
            st.session_state.step = 4
            st.rerun()

    # =========================
    # STEP 4 - OUTPUT (DROPDOWN)
    # =========================
    elif st.session_state.step == 4:
        st.header("📊 Hasil Perhitungan")

        d1 = st.session_state.data_now
        d2 = st.session_state.data_last

        # HITUNG EFISIENSI
        ef_mesin_1 = r.mesin(d1["mesin"], d1["maintenance"])
        ef_bijih_1 = r.bijih(d1["bijih"])
        ef_bbm_1 = r.bahan_bakar(d1["mesin"], d1["maintenance"], d1["bbm"])
        ef_total_1 = r.total(ef_mesin_1, ef_bijih_1, ef_bbm_1)

        ef_mesin_2 = r.mesin(d2["mesin"], d2["maintenance"])
        ef_bijih_2 = r.bijih(d2["bijih"])
        ef_bbm_2 = r.bahan_bakar(d2["mesin"], d2["maintenance"], d2["bbm"])
        ef_total_2 = r.total(ef_mesin_2, ef_bijih_2, ef_bbm_2)

        laba1 = r.laba(
            r.penjualan(d1["bijih"]),
            r.gaji(d1["pekerja"]) + r.bensin(d1["bbm"], d1["mesin"]),
        )

        laba2 = r.laba(
            r.penjualan(d2["bijih"]),
            r.gaji(d2["pekerja"]) + r.bensin(d2["bbm"], d2["mesin"]),
        )

        output_menu = st.selectbox(
            "📌 Pilih Output yang Ditampilkan",
            [
                "Efisiensi Mesin",
                "Efisiensi Bijih",
                "Efisiensi Bahan Bakar",
                "Efisiensi Total",
                "Laba Perusahaan",
                "Grafik Laba",
            ],
        )

        if output_menu == "Efisiensi Mesin":
            st.write("Tahun Ini:", ef_mesin_1, "%")
            st.write("Tahun Lalu:", ef_mesin_2, "%")

        elif output_menu == "Efisiensi Bijih":
            st.write("Tahun Ini:", ef_bijih_1, "%")
            st.write("Tahun Lalu:", ef_bijih_2, "%")

        elif output_menu == "Efisiensi Bahan Bakar":
            st.write("Tahun Ini:", ef_bbm_1, "%")
            st.write("Tahun Lalu:", ef_bbm_2, "%")

        elif output_menu == "Efisiensi Total":
            st.write("Tahun Ini:", ef_total_1, "%")
            st.write("Tahun Lalu:", ef_total_2, "%")

        elif output_menu == "Laba Perusahaan":
            st.write(f"Laba Tahun {st.session_state.tahun}:", laba1)
            st.write(f"Laba Tahun {st.session_state.tahun - 1}:", laba2)

            if laba1 > laba2:
                st.success("📈 Perusahaan Mengalami Kenaikan Laba")
            else:
                st.error("📉 Perusahaan Mengalami Penurunan Laba")

        elif output_menu == "Grafik Laba":
            fig, ax = plt.subplots()
            ax.plot(
                [st.session_state.tahun, st.session_state.tahun - 1],
                [laba1, laba2]
            )
            ax.set_title("Grafik Laba Perusahaan")
            ax.set_xlabel("Tahun")
            ax.set_ylabel("Laba")
            st.pyplot(fig)

        if st.button("🔁 Mulai dari Awal"):
            st.session_state.step = 1
            st.session_state.data_now = {}
            st.session_state.data_last = {}
            st.rerun()

# =========================
# ABOUT US
# =========================
elif menu == "About Us":
    st.title("👨‍💻 About Us")
    st.write("1. Chantica Fepy Ardiantis (16425080)")
    st.write("2. Kayla Putri Nafisha (16425160)")
    st.write("3. Yonathan Samuel Fentason (16425230)")
    st.write("4. Muhammad Fikri Alghifari (16425445)")
    st.write("5. Fatih Azzam Daeli (16425480)")

# =========================
# LOGOUT
# =========================
elif menu == "Logout":
    st.session_state.login = False
    st.session_state.step = 1
    st.success("✅ Logout berhasil!")
    st.rerun()
