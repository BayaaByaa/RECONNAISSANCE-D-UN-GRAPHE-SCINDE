import streamlit as st
import pandas as pd
from graphviz import Graph

st.write("<center><h1>Algorithme de reconnaissance du graphe scindé</h1></center>", unsafe_allow_html=True)

##########AFFICHAGE DU GRAPHE 
def afficher_graphe(matrice_adjacence):
    n = len(matrice_adjacence)
    dot = Graph()  # Use Graph() instead of Digraph()

    # Ajouter tous les sommets au graphe
    for i in range(n):
        dot.node(str(i))

    # Ajouter toutes les arêtes au graphe
    for i in range(n):
        for j in range(i+1, n):  # Iterate only over upper triangle of the adjacency matrix
            if matrice_adjacence[i][j] == 1:
                # Add edge from i to j
                dot.edge(str(i), str(j))

    return dot
############################### THM 1 ############################################
def contient_C4_induit(matriceadj):
    n = len(matriceadj)
    i=0
    print(matriceadj)
    for i in range(n):
        excluded_values = [i]
        for j in[x for x in range(n) if x not in excluded_values]:
            if matriceadj[i][j] == 1:
                excluded_values.append(j)
                for k in[x for x in range(n) if x not in excluded_values]:
                    if matriceadj[j][k] == 1:
                        excluded_values.append(k)
                        for l in[x for x in range(n) if x not in excluded_values]:
                            if matriceadj[i][l] == 1 and matriceadj[k][l] == 1:
                               if matriceadj[i][k] == 0 and matriceadj[j][l] == 0:
                                   return True

    return False
        
    
def contient_C5_induit(matriceadj):
    n = len(matriceadj)
    i=0
    for i in range(n):
        excluded_values = [i]
        for j in [x for x in range(n) if x not in excluded_values]:
            if matriceadj[i][j] == 1:
                excluded_values.append(j)
                for k in[x for x in range(n) if x not in excluded_values]:
                    if matriceadj[j][k] == 1:
                        excluded_values.append(k)
                        for l in[x for x in range(n) if x not in excluded_values]:
                            if matriceadj[k][l] == 1:
                                excluded_values.append(l)
                                for h in[x for x in range(n) if x not in excluded_values]:
                                    if matriceadj[i][h] == 1 and matriceadj[l][h] == 1:
                                       if matriceadj[i][k] == 0 and matriceadj[j][l] == 0 and matriceadj[i][l] == 0 and matriceadj[j][h] == 0 and matriceadj[k][h] == 0 :
                                           return True

    return False
  
    
def complementaire(matriceadj):
    n=len(matriceadj)
    matriceComp=[[0]*n for i in range (n)]
    for i in range(n):
        for j in range(n):
            if i!=j:
                if matriceadj[i][j]==0:
                    matriceComp[i][j]=1
                else:
                    matriceComp[i][j]=0
    return matriceComp

############################### THM 2 ############################################
def supprimer_sommet(sommet, matrice_adjacence):
    
    ''' supprime un sommet et toutes ses arêtes dans la matrice d'adjacence 
    en mettant à zéro les entrées correspondantes dans la matrice.'''
    n = len(matrice_adjacence)
    for i in range(n):
        matrice_adjacence[i][sommet] = 0
        matrice_adjacence[sommet][i] = 0 # symetrie de la  matrice 
    return matrice_adjacence


def trouver_sommets_simpliciaux_et_les_supprimer(matrice_adjacence):
    # Un sommet x d’un graphe G est dit simplicial si son voisinage NG(x) est une clique.
    n = len(matrice_adjacence)
    sommets_simpliciaux = []
    for i in range(n):
     for sommet in range(n):
            # Trouver les voisins du sommet
         voisins = [voisin for voisin in range(n) if matrice_adjacence[sommet][voisin] == 1]
         if len(voisins) >= 1: # au moins un seul voisin
             # Créer une sous-matrice avec les voisins du sommet
             sous_matrice = [[matrice_adjacence[i][j] for j in voisins] for i in voisins]
             # Vérifier si la sous-matrice est une clique
             #Si c'est une clique, le sommet est ajouté à la liste des sommets simpliciaux et supprimé du graphe.
             est_clique = all(all(sous_matrice[i][j] == 1 for j in range(len(voisins)) if j != i) for i in range(len(voisins)))
             if est_clique:
                 sommets_simpliciaux.append(sommet)
                 supprimer_sommet(sommet, matrice_adjacence)
                 break

    return sommets_simpliciaux



def est_triangule(matrice_adjacence):
    """
    Vérifie si un graphe est triangulé en supprimant les sommets simpliciaux.
    """
    n = len(matrice_adjacence)
    M = [[0]*n for _ in range(n)]
    for i in range(n):
           for j in range(n):
                M[i][j] = matrice_adjacence[i][j]

               
    st.markdown('<span style="color: green;">Vérifions d\'abord si $G$ est triangulé:</span>', unsafe_allow_html=True)
    sommets_simpliciaux = trouver_sommets_simpliciaux_et_les_supprimer(matrice_adjacence)
    st.write(r"Les sommets simpliciaux de $G$ :",sommets_simpliciaux)
        
    # Vérifier si la matrice d'adjacence résultante est triangulée
    if  matrice_adjacence == [[0]*n for _ in range(n)]:
        st.write(r"$G$ est triangulé! Est ce que son complémentaire $\bar{G}$ l'est aussi?")
        st.markdown('<span style="color: green;">Vérifions alors si $\overline{G}$ est triangulé:</span>', unsafe_allow_html=True)
        # Création du complémentaire de la matrice d'adjacence
        complementaire = [[0]*n for _ in range(n)]
        for i in range(n):
           for j in range(n):
                if i != j:
                    if M[i][j] == 0:
                        complementaire[i][j] = 1
                    else:
                        complementaire[i][j] = 0
        sommets_simpliciaux2 = trouver_sommets_simpliciaux_et_les_supprimer(complementaire)
        st.write(r"Les sommets simpliciaux de $\bar{G}$ :",sommets_simpliciaux2)
        # Vérifier si le complémentaire est triangulé
        if complementaire == [[0]*n for _ in range(n)]:
            st.write(r"$\bar{G}$ est triangulé aussi!")
            st.write("<p style='color:red;'>Ainsi, Le graphe est scindé!</p>", unsafe_allow_html=True)

        else :
            st.write(r"$\bar{G}$ n'est pas triangulé.")
            st.write("<p style='color:red;'>Ainsi, Le graphe n'est pas scindé!</p>", unsafe_allow_html=True)
            
    else:
        st.write(r"$G$ n'est pas triangulé.")
        st.write("<p style='color:red;'>Ainsi, Le graphe n'est pas scindé!</p>", unsafe_allow_html=True)

############################### THM 3 ############################################
### Fonction qui calcule et trie les degres des sommets par ordre decroissant
def DEG(matrice_adjacence):
    # n est le nombre de sommets 
    n = len(matrice_adjacence)
    degres = {}
    # initialisation deg=0
    for sommet in range(n):
        degres[sommet] = 0
    # Calcule des degres, en parcourant les lignes i et les colonnes j
    for i in range(n):
        for j in range(n):
            if matrice_adjacence[i][j] == 1:
                degres[i] += 1
    # Trier les degrés par ordre decroissant
    D = sorted(degres.values(), reverse=True)
    return D

### Fonction qui affiche les degres des sommets sous forme de tableau
def afficher_tableau(matrice_adjacence):
    n = len(matrice_adjacence)
    degrees = {}

    # Calculate degrees of each vertex
    for i in range(n):
        degrees[i] = sum(matrice_adjacence[i])

    # Create a DataFrame for displaying the table
    df = pd.DataFrame({"Sommet": range(n), "Degré": [degrees[i] for i in range(n)]})

    # Sort the DataFrame by degree in descending order
    df_sorted = df.sort_values(by='Degré', ascending=False)

    df_sorted.set_index('Sommet', inplace=True)

    # Display the sorted DataFrame as a table
    st.dataframe(df_sorted.style.set_properties(**{'width': '300px'}))

### Fonction qui recherche m tq m=MAX{i|d[i]>=i+1}
def m(d):
    R = []
    for i in range(len(d)):
        if d[i] >= i:
            R.append(i + 1)
    if R:
        return max(R)
        
    else:
        return None 
    
### Fonction verifiant le theoreme
def thm3 (resultat, m):
    S1 = sum(resultat[:m]) 
    st.write(r"$\sum_{i=1}^{m} d_i=$", S1)
    S2 = sum(resultat[m:])
    X = m * (m - 1) + S2
    st.write(r"$m(m-1) + \sum_{i=m+1}^{n} d_i=$", X)
    if S1 == X:
        st.write("On a donc:",S1,r"$ = $",X)
        st.write("<p style='color:red;'>Ainsi, Le graphe est scindé!</p>", unsafe_allow_html=True)
    else:
        st.write("On a donc:",S1,r"$ \neq $",X)
        st.write("<p style='color:red;'>Ainsi, Le graphe n'est pas scindé!</p>", unsafe_allow_html=True)

  
####### MISE EN PAGE
C1 =r"Soit $G=(V, E)$ un graphe, $G$ est scindé $\iff$ $G$ ne contient pas  $2 K_2$, $C_4$ ou $C_5$ comme sous-graphe induit."
C2 = r"Soit $G=(V, E)$ un graphe, $G$ est scindé $\iff$ $G$ et $\bar{G}$ sont triangulés."
C3 = r"""
> Soit $G=(V, E)$ avec $d_1 \geq d_2 \geq \dots \geq d_n$ et $m=\max\{i|d_i \geq i-1\}$, alors:
$$
G \text{ est scindé } \iff \sum_{i=1}^{m} d_i = m(m-1) + \sum_{i=m+1}^{n} d_i
$$
"""
# Définir les options de choix
options = ["caractérisation 1", "caractérisation 2","caractérisation 3"]

# Demander à l'utilisateur de choisir une option
choix = st.sidebar.radio("Choisir:", options)

###CARACTERISATION 1 ###
if choix == "caractérisation 1":
    st.subheader('Caractérisation 1:') 
    st.markdown(f"> {C1}", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    file = st.file_uploader(':blue[IMPORTER UN FICHIER CSV]', type=['csv'])
    # Vérifier si un fichier a été téléchargé
    if file is not None:
        # Lire le fichier CSV en utilisant Pandas
        matrice_adjacence = pd.read_csv(file)
        st.write("La matrice d’adjacence importée:")
        st.write(matrice_adjacence)  # Afficher le DataFrame uniquement si un fichier est téléchargé
        # Afficher le graphe
        st.write(r"Soit $G=(V, E)$ le graphe correspondant à la matrice d'adjacence:")
        graph = afficher_graphe(matrice_adjacence.values.tolist())
        st.graphviz_chart(graph.source)
        M=matrice_adjacence.values.tolist()
        matriceComp=complementaire(M)
        
        if contient_C4_induit(M) == False:
            st.write(r"$G$ ne contient pas de $C_4$")
        else: 
            st.write(r"$G$ contient un $C_4$")

        if contient_C5_induit(M) == False:
            st.write(r"$G$ ne contient pas de $C_5$")
        else: 
            st.write(r"$G$ contient un $C_5$")

        if contient_C4_induit(matriceComp) == False:
            st.write(r"$\bar{G}$ ne contient pas de $C_4$",r"$\iff$","$G$ ne contient pas de $2 K_2$")
        else: 
            st.write(r"$\bar{G}$ contient un $C_4$",r"$\iff$","$G$ contient un $2 K_2$")

        if contient_C4_induit(M) == False and contient_C5_induit(M) == False and contient_C4_induit(matriceComp) == False:
            st.write("<p style='color:red;'>Ainsi, Le graphe est scindé!</p>", unsafe_allow_html=True)
        else:
            st.write("<p style='color:red;'>Ainsi, Le graphe n'est pas scindé!</p>", unsafe_allow_html=True)
                
    else:
        st.write("Aucun fichier CSV n'a été téléchargé.")


###CARACTERISATION 2 ###
elif choix == "caractérisation 2":
    # Titre de la page
    st.subheader("Caractérisation 2:")
    st.markdown(f"> {C2}", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    file = st.file_uploader(':blue[IMPORTER UN FICHIER CSV]', type=['csv'])
    if file is not None:
        # Lire le fichier CSV en utilisant Pandas
        matrice_adjacence = pd.read_csv(file)
        st.write("La matrice d’adjacence importée:")
        st.write(matrice_adjacence)  # Afficher le DataFrame uniquement si un fichier est téléchargé
        # Afficher le graphe
        st.write(r"Soit $G=(V, E)$ le graphe correspondant à la matrice d'adjacence:")
        graph = afficher_graphe(matrice_adjacence.values.tolist())
        st.graphviz_chart(graph.source)
        est_triangule(matrice_adjacence.values.tolist())
        
    else:
        st.write("Aucun fichier CSV n'a été téléchargé.")


###CARACTERISATION 3 ###
else:
    # Titre de la page
    st.subheader("Caractérisation 3:")
    st.markdown(C3, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    file = st.file_uploader(':blue[IMPORTER UN FICHIER CSV]', type=['csv'])
    

    if file is not None:
        # Lire le fichier CSV en utilisant Pandas
        matrice_adjacence = pd.read_csv(file)
        st.write("La matrice d’adjacence importée:")
        st.write(matrice_adjacence)  # Afficher le DataFrame uniquement si un fichier est téléchargé
        # Afficher le graphe
        st.write(r"Soit $G=(V, E)$ le graphe correspondant à la matrice d'adjacence:")
        graph = afficher_graphe(matrice_adjacence.values.tolist())
        st.graphviz_chart(graph.source)
        # Display the table
        st.write("Calcul du degré de chaque sommet, puis mise en ordre décroissante:")
        afficher_tableau(matrice_adjacence.values.tolist())

        resultat = DEG(matrice_adjacence.values.tolist())
        m_val = m(resultat)
        st.write("m = MAX{i|d[i]>=i+1}","$\Rightarrow $","m =",m_val)

        if m_val is not None:
            thm3(resultat, m_val)
        else:
            st.write("m n'a pas été trouvé, impossible de vérifier la caractérisation.")
    else:
        st.write("Aucun fichier CSV n'a été téléchargé.")

        
          
        
    









        








