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