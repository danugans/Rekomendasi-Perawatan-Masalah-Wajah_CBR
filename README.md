# CBR Skin Care Recommender

Project structure (single folder):
- `app.py` : Streamlit app (entry point).
- `cbr.py` : CBR engine (similarity, retrieval, recommendation).
- `data_loader.py` : helper to load `cases.csv`.
- `cases.csv` : dataset of past cases (already provided).
- `requirements.txt` : Python dependencies.

How to run locally:
1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate   # or venv\\Scripts\\activate on Windows
   pip install -r requirements.txt
   ```
2. Ensure `cases.csv` is in the same folder as `app.py`.
3. Run:
   ```
   streamlit run app.py
   ```

Deploy to Streamlit Community Cloud:
- Push this entire folder to a GitHub repository.
- On Streamlit Cloud, choose "New app" → connect your GitHub repo → set `app.py` as the main file → deploy.
- Make sure `requirements.txt` is present.

Notes:
- The CBR implementation is simple and explainable. You can improve it by:
  - Adding more features, weights tuning, and better adaptation rules.
  - Storing case metadata and treatment outcomes.
  - Adding admin pages to add/edit cases (saved back to CSV or a database).
