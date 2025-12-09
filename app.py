"""
app.py - Streamlit app for CBR-based skin problem recommendation.
Place this file in the same folder as 'cases.csv' (the dataset).
Run: streamlit run app.py
"""
import streamlit as st
from data_loader import load_cases
from cbr import recommend_solution, find_similar_cases
import pandas as pd

st.set_page_config(page_title="CBR Skin Care Recommender", layout="centered")

st.title("Sistem Rekomendasi Perawatan Kulit (CBR)")
st.markdown("Masukkan informasi pasien / pengguna, pilih gejala yang relevan, lalu tekan **Rekomendasikan**.")

# Load dataset
@st.cache_data
def get_cases():
    return load_cases('cases.csv')

cases_df = get_cases()

with st.form('query_form'):
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Usia", min_value=1, max_value=120, value=25)
        gender = st.selectbox("Jenis Kelamin", options=['female','male','other'])
        skin_type = st.selectbox("Tipe Kulit", options=sorted(cases_df['skin_type'].dropna().unique().tolist()))
    with col2:
        st.write("Pilih gejala yang dialami:")
        symptom_cols = [c for c in cases_df.columns if c not in ['id','age','gender','skin_type','solution']]
        cols_per_col = (len(symptom_cols)+1)//2
        s1 = st.columns(2)
        selected = {}
        for i, sym in enumerate(symptom_cols):
            if i < cols_per_col:
                val = s1[0].checkbox(sym.replace('_',' ').capitalize(), key=sym)
            else:
                val = s1[1].checkbox(sym.replace('_',' ').capitalize(), key=sym)
            selected[sym] = int(val)
    k = st.slider("Jumlah kasus teratas yang ditampilkan (k)", min_value=1, max_value=10, value=3)
    submitted = st.form_submit_button("Rekomendasikan")

if submitted:
    query = {'age': age, 'gender': gender, 'skin_type': skin_type}
    query.update(selected)
    result = recommend_solution(query, cases_df, k=k)
    st.subheader("Rekomendasi Perawatan")
    st.markdown(result['recommendation'])
    st.subheader(f"Kasus teratas (k={k})")
    for c in result['cases']:
        st.write(f"- ID: {c['id']} | Similarity: {c['similarity']:.3f} | Age: {c['age']} | Gender: {c['gender']} | Skin: {c['skin_type']}")
        st.write("  - Solution: " + str(c.get('solution')))
