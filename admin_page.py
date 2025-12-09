import streamlit as st
import pandas as pd
from data_loader import load_cases, save_cases

def admin_page():
    st.subheader("🔐 Halaman Admin – Manajemen Kasus")

    # Password sederhana (bisa diganti)
    password = st.text_input("Password Admin", type="password")
    if password != "admin123":
        st.warning("Masukkan password admin")
        return

    df = load_cases("cases.csv")

    st.write("### Data Kasus Saat Ini")
    st.dataframe(df, use_container_width=True)

    st.write("### ➕ Tambah / ✏️ Edit Kasus")

    with st.form("form_kasus"):
        cols = df.columns.tolist()

        new_data = {}
        for col in cols:
            if col == "id":
                new_data[col] = st.number_input("ID", min_value=1, step=1)
            elif col in ["age"]:
                new_data[col] = st.number_input("Usia", min_value=1, max_value=120)
            elif col in ["gender"]:
                new_data[col] = st.selectbox("Gender", ["male", "female", "other"])
            elif col in ["skin_type"]:
                new_data[col] = st.text_input("Tipe Kulit")
            elif col == "solution":
                new_data[col] = st.text_area("Solusi / Perawatan")
            else:
                new_data[col] = st.checkbox(col.replace("_", " ").capitalize())

        submit = st.form_submit_button("Simpan Kasus")

    if submit:
        new_data = {k: int(v) if isinstance(v, bool) else v for k, v in new_data.items()}

        if new_data["id"] in df["id"].values:
            df.loc[df["id"] == new_data["id"], :] = new_data
            st.success("✅ Kasus berhasil DIUPDATE")
        else:
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            st.success("✅ Kasus berhasil DITAMBAHKAN")

        save_cases(df)
        st.rerun()

    st.write("### ❌ Hapus Kasus")
    delete_id = st.number_input("Masukkan ID yang akan dihapus", min_value=1, step=1)
    if st.button("Hapus"):
        df = df[df["id"] != delete_id]
        save_cases(df)
        st.success("🗑️ Kasus berhasil dihapus")
        st.rerun()
