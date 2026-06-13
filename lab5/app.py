import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
import glob

st.set_page_config(layout="wide", page_title="Аналіз індексів VCI, TCI, VHI (ЛР5)")

noaa_to_ua = {
    1: (22, "Черкаська"), 2: (24, "Чернігівська"), 3: (23, "Чернівецька"),
    4: (3, "Дніпропетровська"), 5: (4, "Донецька"), 6: (11, "Луганська"),
    7: (9, "Київська"), 8: (8, "Івано-Франківська"), 9: (21, "Хмельницька"),
    10: (10, "Кіровоградська"), 11: (12, "Львівська"), 12: (13, "Миколаївська"),
    13: (14, "Одеська"), 14: (15, "Полтавська"), 15: (16, "Рівненська"),
    16: (17, "Сумська"), 17: (18, "Тернопільська"), 18: (19, "Харківська"),
    19: (20, "Херсонська"), 20: (7, "Запорізька"), 21: (6, "Закарпатська"),
    22: (2, "Волинська"), 23: (5, "Житомирська"), 24: (1, "Вінницька"),
    25: (25, "Крим"), 26: (26, "Севастополь"), 27: (27, "Київ місто")
}

DOWNLOAD_DIR = "vhi_data"

@st.cache_data
def load_and_clean_data_lr5():
    all_dfs = []
    files = glob.glob(os.path.join(DOWNLOAD_DIR, "vhi_id_*.csv"))
    
    if not files:
        files = glob.glob(os.path.join("../lab2/vhi_data", "vhi_id_*.csv"))
        
    if not files:
        return pd.DataFrame()
        
    for file in files:
        filename = os.path.basename(file)
        old_id = int(filename.split("_")[2])
        if old_id not in noaa_to_ua:
            continue
            
        new_id, region_name = noaa_to_ua[old_id]
        df = pd.read_csv(
            file, 
            skiprows=1, 
            names=['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI'], 
            usecols=range(7)
        )
        df = df.dropna(subset=['Year'])
        df = df[df['Year'].astype(str).str.isnumeric()]
        df = df.astype({'Year': int, 'Week': int, 'VCI': float, 'TCI': float, 'VHI': float})
        df = df[['Year', 'Week', 'VCI', 'TCI', 'VHI']]
        df['Area_ID'] = new_id
        df['Area_Name'] = region_name
        all_dfs.append(df)
        
    if not all_dfs:
        return pd.DataFrame()
        
    return pd.concat(all_dfs, ignore_index=True)

df = load_and_clean_data_lr5()

if df.empty:
    st.error("❌ Помилка: Не знайдено завантажених файлів у папці vhi_data.")
else:
    if 'index_sel' not in st.session_state:
        st.session_state.index_sel = 'VHI'
        st.session_state.region_sel = sorted(df['Area_Name'].unique())[0]
        st.session_state.weeks_sel = (1, 52)
        st.session_state.years_sel = (int(df['Year'].min()), int(df['Year'].max()))
        st.session_state.sort_asc = False
        st.session_state.sort_desc = False

    def reset_filters():
        st.session_state.index_sel = 'VHI'
        st.session_state.region_sel = sorted(df['Area_Name'].unique())[0]
        st.session_state.weeks_sel = (1, 52)
        st.session_state.years_sel = (int(df['Year'].min()), int(df['Year'].max()))
        st.session_state.sort_asc = False
        st.session_state.sort_desc = False

    st.title("📊 Інтерактивний аналіз екологічних індексів України")
    st.write("Побудовано на реальних даних NOAA з Лабораторної роботи №2.")

    col1, col2 = st.columns([1, 3])

    with col1:
        st.header("🎛️ Налаштування фільтрів")
        selected_index = st.selectbox("Оберіть екологічний індекс:", options=['VHI', 'VCI', 'TCI'], key='index_sel')
        selected_region = st.selectbox("Оберіть область України:", options=sorted(df['Area_Name'].unique()), key='region_sel')
        selected_weeks = st.slider("Діапазон тижнів:", min_value=1, max_value=52, key='weeks_sel')
        selected_years = st.slider("Діапазон років:", min_value=int(df['Year'].min()), max_value=int(df['Year'].max()), key='years_sel')
        st.subheader("Сортування")
        sort_ascending = st.checkbox("За зростанням значення індексу", key='sort_asc')
        sort_descending = st.checkbox("За спаданням значення індексу", key='sort_desc')
        st.button("Скинути всі фільтри 🔄", on_click=reset_filters)

    filtered_df = df[
        (df['Area_Name'] == selected_region) &
        (df['Year'] >= selected_years[0]) & (df['Year'] <= selected_years[1]) &
        (df['Week'] >= selected_weeks[0]) & (df['Week'] <= selected_weeks[1])
    ].copy()

    filtered_df['Time'] = filtered_df['Year'] + (filtered_df['Week'] - 1) / 52

    if sort_ascending and sort_descending:
        st.warning("⚠️ Актировано обидва чекбокси сортування! Пріоритет надано сортуванню за зростанням.")
        filtered_df = filtered_df.sort_values(by=selected_index, ascending=True)
    elif sort_ascending:
        filtered_df = filtered_df.sort_values(by=selected_index, ascending=True)
    elif sort_descending:
        filtered_df = filtered_df.sort_values(by=selected_index, ascending=False)

    with col2:
        st.header("📈 Результати аналізу")
        tab1, tab2, tab3 = st.tabs(["📋 Таблиця даних", "📉 Графік часового ряду", "🗺️ Порівняння областей"])
        
        with tab1:
            st.subheader(f"Зріз даних для області: {selected_region}")
            st.dataframe(filtered_df[['Year', 'Week', 'Area_Name', 'VHI', 'VCI', 'TCI']], use_container_width=True)
        
        with tab2:
            st.subheader(f"Динаміка індексу {selected_index} у часі ({selected_years[0]}-{selected_years[1]})")
            if not filtered_df.empty:
                plot_df = filtered_df.sort_values(by='Time')
                fig1 = px.line(plot_df, x='Time', y=selected_index, title=f"Зміна індексу {selected_index} ({selected_region} область)", labels={'Time': 'Рік', selected_index: f'Значення {selected_index}'})
                fig1.update_traces(line_color='#1f77b4', line_width=2.5)
                st.plotly_chart(fig1, use_container_width=True)
            else:
                st.info("Немає даних для відображення за обраними фільтрами.")
                
        with tab3:
            st.subheader(f"Порівняння індексу {selected_index} обраної області з іншими регіонами")
            comp_df = df[
                (df['Year'] >= selected_years[0]) & (df['Year'] <= selected_years[1]) &
                (df['Week'] >= selected_weeks[0]) & (df['Week'] <= selected_weeks[1])
            ].copy()
            comp_df['Time'] = comp_df['Year'] + (comp_df['Week'] - 1) / 52
            comp_df = comp_df.sort_values(by='Time')
            
            if not comp_df.empty:
                fig2 = px.line(comp_df, x='Time', y=selected_index, color='Area_Name', title=f"Порівняльний аналіз {selected_index} по областях України", labels={'Time': 'Рік', selected_index: selected_index})
                for trace in fig2.data:
                    if trace.name == selected_region:
                        trace.line.width = 4.5

                        trace.line.opacity = 1.0
                    else:
                        trace.line.width = 1.0
                        trace.line.opacity = 0.4
=======
                        trace.opacity = 1.0
                    else:
                        trace.line.width = 1.0
                        trace.opacity = 0.4
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("Немає даних для побудови порівняльного графіка.")