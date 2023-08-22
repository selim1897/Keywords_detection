import pandas as pd
import numpy as np
import streamlit as st
from mass_analytics import keywords as kw
import re


st.set_page_config(page_title="Keyword Colorizer", page_icon="📶", layout="wide", initial_sidebar_state="expanded", menu_items={"About": "Mass Analytics"})
min_value=1000
max_value=10000
json_data = kw.see_all()
categories = json_data.keys()
color_palette = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',  # Blues, Orange, Green, Red, Purple
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',  # Brown, Pink, Gray, Yellow, Cyan
    '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5',  # Light blues, Light orange, Light green, Light red, Light purple
    '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5'   # Light brown, Light pink, Light gray, Light yellow, Light cyan
]

def remove_ponctuation(string):
    if string is not None:
        clean = re.sub(r"[,.;:@#?!&$_/-]+", " ", string)
    else:
        return None 
    return clean

def color_cell(v, color, cat_data):
    bo = False
    if type(v) is str:
        bo = len(set(map(str.upper, remove_ponctuation(v).split())).intersection(cat_data)) > 0
    return f"background-color: {color}; color: white;" if bo else None

def style_by_category(new_df, category_choosen, df_style):
    for index,cat in enumerate(category_keys):        
        cat_data = [val.upper() for val in json_data[category_choosen][cat]]
        for col in new_df.columns:
            if remove_ponctuation(col) in cat_data:
                total_style = pd.DataFrame({col: ["background-color: "+color_palette[index]+"; color: white;"]*new_df.shape[0]})
                df_style.apply(lambda s: total_style, axis=None)
            else:
                if np.issubdtype(new_df[col].dtype, np.object_):
                    df_style.applymap(color_cell, color=color_palette[index], cat_data=cat_data)
   
    return df_style

def display_dataframe_with_pagination(df, rows_per_page):
    try:
        start_idx = 0
        n=0
        while start_idx < len(df):
            new_df = df.iloc[start_idx:start_idx + rows_per_page]
            new_df.reset_index(inplace=True)
            df_style = new_df.style
            st.dataframe(style_by_category(new_df, category_choosen, df_style), hide_index=True)
            start_idx += rows_per_page
            n=n+1
            if number_of_page==n:
                break
    except:
        pass

if "df" in st.session_state:
    df = st.session_state["df"]
    rows_per_page = st.session_state["rows_per_page"]
    number_of_page = st.session_state["number_of_page"]
    category_choosen = st.radio("Choose a category:",categories, horizontal=True)
    
    category_keys = json_data[category_choosen].keys()
    string_to_display = r"---"
    for index,cat in enumerate(category_keys):
        string_to_display = string_to_display + r"$\textcolor{"+color_palette[index]+"}{"+cat+"}$ ---"
    
    st.markdown(string_to_display)

    display_dataframe_with_pagination(df,min(rows_per_page,len(df)))
