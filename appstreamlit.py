import streamlit as st
import pandas as pd



uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df = df[(df['compoA'] != '?') & (df['compoB'].notna())& (df['compoA'].notna())& (df['compoB'] != '?')]
    df = df.reset_index(drop=True)
    st.sidebar.title("Choisir la formation de l'équipe A")
    compoA = st.sidebar.multiselect("Choix formation équipe A",df["compoA"].unique())
    st.sidebar.title("Choisir la formation de l'équipe B")
    compoB = st.sidebar.multiselect("Choix formation équipe B",df["compoB"].unique())
    st.sidebar.title("Choisir les continents")
    continents = st.sidebar.multiselect("Choix continent(s)", df["Continent"].unique())
    influence = st.sidebar.slider("Affluence",0,200,max(df["influence"]))
    if (len(compoA)>0) & (len(compoB)>0):
        if len(continents)==0:
            new_df = df[(((df['compoA'].isin(compoA)) & (df['compoB'].isin(compoB))) | ((df['compoB'].isin(compoA)) & (df['compoA'].isin(compoB)))) & (df["influence"] >= influence)]

        else :
            new_df = df[(((df['compoA'].isin(compoA)) & (df['compoB'].isin(compoB))) | ((df['compoB'].isin(compoA)) & (df['compoA'].isin(compoB))))& (df["influence"]>=influence)&(df["Continent"].isin(continents))]
        new_df = new_df.reset_index(drop=True)
        st.title("Liste des matchs")
        st.write(new_df)
