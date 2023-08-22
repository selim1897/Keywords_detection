import streamlit as st
import pandas as pd
from mass_analytics import keywords as kw
import io


st.set_page_config(page_title="Data", page_icon="📶", layout="wide", initial_sidebar_state="expanded", menu_items={"About": "Mass Analytics"})
if "df" in st.session_state:
    df = st.session_state["df"]
json_data = kw.see_all()
col1, col2= st.columns(2)

def to_excel(data):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer) as writer:
        for categorie in data.keys():
            nb_cols = [len(data[categorie][key]) for key in data[categorie].keys()]
            max_nb_cols = max(nb_cols)
            for key in data[categorie].keys():
                while len(data[categorie][key]) < max_nb_cols:
                    data[categorie][key].append("")
            df = pd.DataFrame(data[categorie])
            df.to_excel(writer, sheet_name=categorie, index=False)
    return buffer

def send_data(uploaded_file, access_token):
    xl = pd.ExcelFile(uploaded_file)

    result = {}
    for cat in xl.sheet_names:
        result[cat] = {}
        df = xl.parse(cat)
        for col in df.columns:
            result[cat][col] = list(df[col].dropna())
    kw.update_data(result, access_token)
    
        
with col1:
    category = st.selectbox(
    'Please choose a category',
    json_data.keys())

    key = st.selectbox(
    'Please choose a sub-category',
    json_data[category].keys())

    xlsx = to_excel(json_data)

    st.download_button(
        label="Download Current keywords",
        data=xlsx,
        file_name='keywords.xlsx',
    )


with col2:
    st.json(json_data[category][key])

col3, col4= st.columns([1,2])

with col3:
    with st.form("my_form"):
        st.write("**Would you like to modify the keywords?**")
        uploaded_file = st.file_uploader("Excel file", type="xlsx")
        access_token = st.text_input('Access token', type="password")
        submitted = st.form_submit_button("Submit")
        if submitted:
            try:
                send_data(uploaded_file, access_token)
                st.write(r":green[Content updated successfully]")
            except Exception as e:
                st.error(e)
                print(e)
    

    
