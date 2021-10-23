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