import pandas as pd
import streamlit as st


def extract_names(files):
    return [file.name for file in files if file.name.endswith((".csv", ".xlsx"))]

@st.cache_data(show_spinner=False)
def read_file(files):
    dfs = []
    columns = None
    
    for file in files:
        if ".csv" in file.name:
            data = pd.read_csv(file)
        elif ".xlsx" in file.name:
            data = pd.read_excel(file)
        else:
            st.warning(f"Unsupported file format: {file.name}")
            continue  # Skip unsupported file formats
        
        if columns is None:
            columns = set(data.columns)
            dfs.append(data)
        elif set(data.columns) == columns:
            dfs.append(data)
        else:
            st.error("The tables do not have the same columns!", icon="🚨")
            return None
    
    return pd.concat(dfs)

def display_files_list(names):
    files_list = ''
    if names:
        for name in names:
            files_list += name + ', '
      
    st.write('The files that are currently in Data Checker are: ' + str(files_list))

    
st.set_page_config(page_title="Data checker", page_icon="📶", layout="wide", initial_sidebar_state="expanded", menu_items={"About": "Mass Analytics"})

rows_per_page = st.number_input("Number of Rows per Page", min_value=1000, max_value=10000, value=1000)

number_of_page= st.number_input("Number of page", min_value=1, max_value=50, value=1)

uploaded_files = st.file_uploader("Input csv or excel file", type=["xlsx","csv"],accept_multiple_files=True)

list_names=extract_names(uploaded_files)

if list_names:
    st.session_state['names'] = list_names
elif 'names' in st.session_state:
    list_names = st.session_state['names']
     
display_files_list(list_names) 
     
if len(uploaded_files)>0:
    df = read_file(uploaded_files)
elif "df" in st.session_state:
    df = st.session_state["df"]
else:
    df = pd.DataFrame()

st.session_state["df"] = df
st.session_state["rows_per_page"] = rows_per_page
st.session_state["number_of_page"] = number_of_page
    


