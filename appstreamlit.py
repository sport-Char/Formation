import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def getWinner(score):
    numbers = score.split(':')  # Divisez la première partie en deux nombres: '2' et '5'
    x = int(numbers[0])
    y = int(numbers[1])

    if x > y:
        return "Victoire"
    elif x == y:
        return "Egalité"
    else:
        return "Défaite"

def getResult(df, A, B):
    conditions = {
    'Egalité': 'Egalité',
    'Victoire': 'Défaite',
    'Défaite': 'Victoire'}
    df.loc[df['compoB'].isin(A), 'Résultat'] = df.loc[df['compoB'].isin(A), 'Résultat'].apply(lambda x: conditions.get(x, x))
    return df

def addPoint(df):
    for index, row in df.iterrows():
        if 'tab' in row['result']:
            df.at[index, 'Résultat'] = "Egalité"
        elif 'ap' in row['result']:
            parts = row["result"].split(' ')[0]
            point = getWinner(parts)
            df.at[index, 'Résultat'] = point
        else:
            point = getWinner(row["result"])
            df.at[index, 'Résultat'] = point
    return df

def createPieChart(df):
    plt.rcParams['font.sans-serif'] = 'Arial'
    custom_colors = {'Egalité': '#4861db', 'Victoire': '#8cd071', 'Défaite': '#ec4f42'}


    result_counts = df['Résultat'].value_counts()

    colors = [custom_colors.get(value, sns.color_palette('pastel')[i]) for i, value in enumerate(result_counts.index)]
    fig, ax = plt.subplots()
    ax.pie(result_counts, labels=result_counts.index, autopct='%1.1f%%', startangle=90, colors=colors)
    ax.axis('equal')  # Assurez-vous que le graphique est un cercle parfait
    ax.legend(result_counts.index, title="Résultats", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    plt.title("Répartition des Résultats")
    return fig

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df = df[(df['compoA'] != '?') & (df['compoB'].notna())& (df['compoA'].notna())& (df['compoB'] != '?')]
    df = df.reset_index(drop=True)
    df = addPoint(df)
    st.sidebar.title("Choisir la formation de l'équipe A")
    compoA = st.sidebar.multiselect("Choix formation équipe A",df["compoA"].unique())
    st.sidebar.title("Choisir la formation de l'équipe B")
    compoB = st.sidebar.multiselect("Choix formation équipe B",df["compoB"].unique())
    st.sidebar.title("Choisir les continents")
    continents = st.sidebar.multiselect("Choix continent(s)", df["Continent"].unique())
    influence = st.sidebar.slider("Affluence",0,max(df["influence"]),value=0)
    if (len(compoA)>0) & (len(compoB)>0):
        if len(continents)==0:
            new_df = df[(((df['compoA'].isin(compoA)) & (df['compoB'].isin(compoB))) | ((df['compoB'].isin(compoA)) & (df['compoA'].isin(compoB)))) & (df["influence"] >= influence)]
            new_df = getResult(new_df, compoA, compoB)
        else :
            new_df = df[(((df['compoA'].isin(compoA)) & (df['compoB'].isin(compoB))) | ((df['compoB'].isin(compoA)) & (df['compoA'].isin(compoB))))& (df["influence"]>=influence)&(df["Continent"].isin(continents))]
            new_df = getResult(new_df, compoA, compoB)
        new_df = new_df.reset_index(drop=True)
        st.title("Liste des matchs")
        st.write(new_df)
        st.title('Distribution des Résultats')
        fig = createPieChart(new_df)
        st.pyplot(fig)
