import streamlit as st
from string import ascii_lowercase as ascii_l
from gauss import *
import numpy as np
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="Gauß",
    page_icon="🤔",
    layout="wide"
)

st.markdown(
    '''
    <style>
        footer {visibility: hidden;}
        .edgvbvh1 {
            width: 100% !important;
        }
    </style>
    ''', unsafe_allow_html=True
)

st.header("Gauß-Algorithmus")

values = [[3125, 625, 125, 25, 5, 1, 2.5],
          [3125, 500, 75, 10, 1, 0, -1],
          [2500, 300, 30, 2, 0, 0, 0],
          [0, 0, 0, 1, 0, 0, 0],
          [0, 0, 0, 0, 1, 0, 2],
          [0, 0, 0, 0, 0, 1, 0]]

n = st.number_input(label="Anzahl Variablen:",
                    min_value=2, max_value=6, value=6)

cols = list(st.columns(int(n)+1))
a = [[] for _ in range(int(n))]
b = []

for idx, col in enumerate(cols):
    for row in range(int(n)):
        if idx == n:
            b.append(col.number_input(
                label=f"y{row+1}", value=float(values[row][-1])))
        else:
            a[row].append(col.number_input(
                label=f"{ascii_l[idx]}{row+1}", value=float(values[row][idx])))

eliminate = st.button("Lösen")

def PolyGraph(koeffs):
    Xs = np.linspace(-20, 20, 400)
    Ys = []
    for x in Xs:
        Yx = 0
        for idx, j in enumerate(koeffs):
            Yx += j * (x ** (len(koeffs)-idx-1))
        Ys.append(Yx)
    return Xs, Ys

if eliminate:
    a1, b1 = eliminieren(a, b)
    eigeneLösung = backsubstitution(a1, b1)
    eigeneLösungString = []
    for idx, i in enumerate(eigeneLösung):
        eigeneLösungString.append(f"{ascii_l[idx]} = ")
        eigeneLösungString.append(round(eigeneLösung[idx], 6))
    st.write("eigene Lösung:", *eigeneLösungString)
    eingebauteLösung = np.round(np.linalg.solve(a, b), 6)
    eingebauteLösungString = []
    for idx, i in enumerate(eingebauteLösung):
        eingebauteLösungString.append(f"{ascii_l[idx]} = ")
        eingebauteLösungString.append(eingebauteLösung[idx])
    st.write("Numpy Lösung:", *eingebauteLösungString)
    superScriptDict = {
        1: '',
        2: '²',
        3: '³',
        4: '⁴',
        5: '⁵',
    }
    Xs, Ys = PolyGraph(eigeneLösung)
    df = pd.DataFrame(dict(
        x = Xs,
        y = Ys
    ))
    myString = []
    for idx, i in enumerate(eigeneLösung):
        if i != 0:
            if idx < len(eigeneLösung) -1:
                myString.append(f"{round(i, 6)}x{superScriptDict[len(eigeneLösung)-idx-1]}")
            else:
                myString.append(f"{round(i, 6)}")
    fig = px.line(df, x="x", y="y", title="Graph: " + " + ".join(myString))
    fig.update_xaxes(range=[-1, 6])
    fig.update_yaxes(range=[-5, 5])
    st.plotly_chart(fig, use_container_width=True)
    st.write("Eliminierungs Dreieck")
    _ = [a1[i].append(b1[i]) for i in range(len(b1))]
    st.write(np.array(a1))

st.markdown("---")

st.code(
    """
def eliminieren(a, b):
    for i in range(len(b)-1): # iteriere von der ersten bis zur vorletzten Spalte/"Koeffs von jeweils einer Variable"
        if a[i][i] < 1.0e-12: # wenn sich Wert direkt über dem Dreieck 0 annähert, probiere Reihenfolge zu ändern, um 0-Division zu umgehen
            for j in range(i+1, len(b)): # iteriere über Werte innerhalb der Spalte ab Spalte+1
                if a[j][i] > a[i][i]: # wenn iterierter Wert größer als Wert über Dreieck (ca. Null)
                    a[i], a[j] = a[j], a[i] # vertausche Reihen
                    b[i], b[j] = b[j], b[i] # vertausche B/Y-Werte
                    break # breche Schleife ab
        for j in range(i+1, len(b)): # iteriere über Werte innerhalb der Spalte ab Spalte+1 für Dreiecksform insgesamt
            if a[j][i] == 0: continue # überspringe, wenn Wert schon 0
            factor = a[i][i] / a[j][i] # ermittle Verhältnis von aktuellem Koeff und dem Koeff über Dreieck
            for k in range(i, len(b)): # iteriere über ausgewählte ganze Reihe
                a[j][k] = a[i][k] - a[j][k]*factor # Setze Koeff auf 0 oder berechne anderen neuen Werte
            b[j] = b[i] - b[j]*factor # berechne neuen B/Y-Wert für Reihe
    return a, b # gib LGS mit eliminiertem Dreieck zurück 

def backsubstitution(a, b):
    x = [0 for _ in range(len(b))] # jeder Variable wird erst 0 zugewiesen
    x[len(b)-1] = b[len(b)-1] / a[len(b)-1][len(b)-1] # Variable unten rechts im LGS wird gelöst
    for i in range(len(b)-2, -1, -1): # iteriert von unten nach oben über restliche Gleichungen
        sum_ax = sum([a[i][j] * x[j] for j in range(i+1, len(b))]) # addiere bisher gelöste Variablen * Koeff
        x[i] = (b[i] - sum_ax) / a[i][i] # berechne die neue Variable der Reihe
    return x # gib gelöste Variablen zurück
    """
)

st.markdown(
            """
            <div>
                <a style='text-decoration: none; display:flex; align-items: center; justify-content: center; gap: 5px;' href="https://github.com/foersterrobert/Gauss" target='_blank'>
                    <h4>Der code ist auch auf GitHub</h4>
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("---")

st.subheader("Videos über die Theorie")
st.video("https://www.youtube.com/watch?v=ZDxONtacA_4")
st.video("https://www.youtube.com/watch?v=i7f9PBe-j_Y")