import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

def getResult(df, A, B):
    conditions = {
    'Egalité': 'Egalité',
    'Victoire': 'Défaite',
    'Défaite': 'Victoire'}
    df.loc[df['CompoAway'].isin(A), 'Résultat'] = df.loc[df['CompoAway'].isin(A), 'Résultat'].apply(lambda x: conditions.get(x, x))
    return df

def getWinner(score):
    numbers = score.split(':')
    try:  # Divisez la première partie en deux nombres: '2' et '5'
    	x = int(numbers[0])
    except:
    	st.write(score)
    y = int(numbers[1])

    if x > y:
        return "Victoire"
    elif x == y:
        return "Egalité"
    else:
        return "Défaite"

def addPoint(df):
    for index, row in df.iterrows():
        if 'tab' in row['score']:
            df.at[index, 'Résultat'] = "Egalité"
        elif 'ap' in row['score']:
            parts = row["score"].split(' ')[0]
            point = getWinner(parts)
            df.at[index, 'Résultat'] = point
        else:
            point = getWinner(row["score"])
            df.at[index, 'Résultat'] = point
    return df


uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df['score'] = df['score'].astype(str)
    df['influence'] = df['influence'].str.replace('.', '').str.replace('X', '0').fillna(0).astype(int)
    # Supprimez les lignes où la colonne 'score' contient le caractère "-"
    df = df[df['score'] != "-"]
    df = df.drop('compo', axis=1)
    df = df.drop('selected_team', axis=1)
    df = df.dropna(subset=["CompoHome"])
    df = df.dropna(subset=["CompoAway"])
    df = df[df['score'] != '-:-']
    df = addPoint(df)
    valeurs_uniques_home = df['CompoHome'].unique()
    valeurs_uniques_away = df['CompoAway'].unique()
    valeurs_uniques_concat = list(set(valeurs_uniques_home) | set(valeurs_uniques_away))

    st.sidebar.title("Choisir votre(vos) formation(s)")
    compoA = st.sidebar.multiselect("Choix formation équipe A",valeurs_uniques_concat)
    st.sidebar.title("Choisir la(les) formation(s) de l'équipe adverse")
    compoB = st.sidebar.multiselect("Choix formation équipe B",valeurs_uniques_concat)
    # Convertissez la colonne 'score' en entiers (si nécessaire)
    influence = st.sidebar.slider("Affluence",0,max(df["influence"]),value=0)
    if (len(compoA)>0) & (len(compoB)>0):
    	new_df = df[(((df['CompoHome'].isin(compoA)) & (df['CompoAway'].isin(compoB))) | ((df['CompoAway'].isin(compoA)) & (df['CompoHome'].isin(compoB)))) & (df["influence"] >= influence)]
    	new_df = getResult(new_df, compoA, compoB)
    	new_df = new_df.reset_index(drop=True)
    	st.title("Liste des matchs")
    	st.write(new_df)
    	st.title('Distribution des Résultats')
    	fig = createPieChart(new_df)
    	st.pyplot(fig)
