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
                label=f"y{row+1}", value=values[row][-1]))
        else:
            a[row].append(col.number_input(
                label=f"{ascii_l[idx]}{row+1}", value=values[row][idx]))

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
    st.write("in Numpy eingebaute Lösung:", *eingebauteLösungString)
    with st.expander("Details"):
        s1, s2 = st.columns(2)
        s1.write(np.array(a1))
        s2.write(np.array(b1))
        Xs, Ys = PolyGraph(eigeneLösung)
        df = pd.DataFrame(dict(
            x = Xs,
            y = Ys
        ))
        myString = []
        for idx, i in enumerate(eigeneLösung):
            myString.append(f"{i}x\u00b3{len(eigeneLösung)-idx-1}")
        fig = px.line(df, x="x", y="y", title="Graph: " + " + ".join(myString))
        fig.update_xaxes(range=[-1, 6])
        fig.update_yaxes(range=[-5, 5])
        st.plotly_chart(fig)

st.code(
    """
def eliminieren(a, b):
    for i in range(len(b)-1):
        for j in range(i+1, len(b)):
            if a[j][i] == 0:
                continue
            factor = a[i][i] / a[j][i]
            for k in range(i, len(b)):
                a[j][k] = a[i][k] - a[j][k]*factor
            b[j] = b[i] - b[j]*factor
        return a, b

def backsubstitution(a, b):
    x = [0 for _ in range(len(b))] # Jeder Variable wird erst 0 zugewiesen.
    x[len(b)-1] = b[len(b)-1] / a[len(b)-1][len(b)-1] # Variable unten rechts im LGS wird gelöst
    for i in range(len(b)-2, -1, -1): # iteriert von unten nach oben über restliche Gleichungen
    sum_ax = sum([a[i][j] * x[j] for j in range(i+1, len(b))]) 
    x[i] = (b[i] - sum_ax) / a[i][i]
    return x
"""
)
