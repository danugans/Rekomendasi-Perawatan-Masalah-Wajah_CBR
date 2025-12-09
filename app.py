import streamlit as st
from data_loader import load_cases
from cbr import recommend_solution
from admin_page import admin_page

st.set_page_config(page_title="CBR Perawatan Kulit", layout="centered")

menu = st.sidebar.selectbox(
    "Menu",
    ["Rekomendasi Perawatan", "Admin"]
)

if menu == "Admin":
    admin_page()
    st.stop()

# ================= USER PAGE =================
st.title("🧴 Sistem Rekomendasi Perawatan Kulit (CBR)")

df = load_cases("cases.csv")

with st.form("user_form"):
    age = st.number_input("Usia", min_value=1, max_value=120, value=25)
    gender = st.selectbox("Gender", ["male", "female", "other"])
    skin_type = st.selectbox("Tipe Kulit", sorted(df["skin_type"].unique()))

    st.write("### Gejala yang Dialami")
    symptom_cols = [c for c in df.columns if c not in ["id", "age", "gender", "skin_type", "solution"]]
    selected = {}
    for s in symptom_cols:
        selected[s] = int(st.checkbox(s.replace("_", " ").capitalize()))

    k = st.slider("Jumlah Kasus Pembanding", 1, 10, 3)
    submit = st.form_submit_button("🔍 Rekomendasikan")

if submit:
    query = {
        "age": age,
        "gender": gender,
        "skin_type": skin_type,
        **selected
    }

    result = recommend_solution(query, df, k=k)

    st.subheader("✅ Rekomendasi Perawatan")
    st.success(result["recommendation"])

    st.write("### Kasus Pembanding")
    for c in result["cases"]:
        st.write(f"- ID {c['id']} | Similarity: {c['similarity']:.2f}")
