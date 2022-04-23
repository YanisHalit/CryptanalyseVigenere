# Sorbonne Université 3I024 2021-2022
# TME 2 : Cryptanalyse du chiffre de Vigenere
#
# Etudiant.e 1 : NOM ET NUMERO D'ETUDIANT
# Etudiant.e 2 : NOM ET NUMERO D'ETUDIANT

import sys, getopt, string, math

# Alphabet français
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Fréquence moyenne des lettres en français en considérant le text Germinal de Zola.
freq_FR = [0.09213414037491088, 0.010354463742221126, 0.030178915678726964, 0.03753683726285317, 0.17174710607479665, 0.010939030914707838, 0.01061497737343803, 0.010717912027723734, 0.07507240372750529, 0.003832727374391129, 6.989390105819367e-05, 0.061368115927295096, 0.026498684088462805, 0.07030818127173859, 0.049140495636714375, 0.023697844853330825, 0.010160031617459242, 0.06609294363882899, 0.07816806814528274, 0.07374314880919855, 0.06356151362232132, 0.01645048271269667, 1.14371838095226e-05, 0.004071637436190045, 0.0023001447439151006, 0.0012263202640210343]

# Calcul fréquences sur un long texte français

################   Réponses_aux_questions   ################

#   CryptAnalyse V1 :
#       18 textes ont pu être correctement déchiffré.
#       Echec survenant pour des textes ayant une longueur de clef importante.
#
#   CryptAnalyse V2 :
#       43 textes ont pu être correctmeent déchiffrés.
#       Echec survenant pour des textes trop courts avec une longueur de clef importante.
#
#   CrypAnalayse V3 :
#       84 textes ont pu être correctement déchiffrés.
#       Echec survenant pour des texte courts.







# Chiffrement César
def chiffre_cesar(txt, key):
    """
    Réalise le décalage en chiffrement des caractères du texte passé en argument de fonction écrit en majuscule sans accents et sans espaces,selon la clé.
    """
    res = ""
    if key == 0 : 
        return txt
    if key < 1  or key > 26 : 
        print("erreur clé")
        return txt

    for t in txt :
        asc = ord(t)
        count = 0
        while count < key:
            if asc+1 <= ord('Z'):
                asc = asc+1
                count = count + 1
            else : 
                asc = ord('A')
                count = count + 1
        res = res + chr(asc)
    txt = res
    return txt

# Déchiffrement César
def dechiffre_cesar(txt, key):
    """
    Réalise le décalage en déchiffrement des caractères du texte passé en argument de fonction, écrit en majuscule sans accents et espaces, selon la clé
    qui est un entier.
    """
    res = ""
    if key == 0 : 
        return txt
    if key < 1  or key > 26 : 
        print("erreur clé")
        return txt
    for t in txt :
        asc = ord(t)
        count = 0
        while count < key:
            if asc-1 >= ord('A'):
                asc = asc-1
                count = count + 1
            else : 
                asc = ord('Z')
                count = count + 1
        res = res + chr(asc)
    txt = res
    return txt

# Chiffrement Vigenere
def chiffre_vigenere(txt, key):
    """
    Fonction effectuant un chiffrement de vigenere du text passé en argument écrit en majuscule et sans espaces ni accents, selon la clef qui est un tabeau d'entier.
    """
    res = []
    len_k = len(key) - 1 # longueur de la clé
    txt_rang = []    # tableau contenant le rang de chaque lettre du txt
    for t in txt : 
        txt_rang.append(alphabet.index(t))
    cpt = 0          # afin d'avancer bloc par bloc en "superposant" la clé au text
    for tr in txt_rang : 
        if cpt > len_k : 
            cpt = 0
        stock = tr + key[cpt]
        if stock > len(alphabet)-1 :
            stock = stock % len(alphabet)
        res.append( stock )
        cpt = cpt + 1

    txt_return = ""
    for r in res : 
        txt_return = txt_return + alphabet[r]
    return txt_return

# Déchiffrement Vigenere
def dechiffre_vigenere(txt, key):
    """
    Fonction effectuant un déchiffrement de vigenere du texte passé en argument écrit en majuscule et sans espaces ni accents, selon la clef qui est un tabeau d'entier.
    """
    res = []
    len_k = len(key) - 1 # longueur de la clé
    txt_rang = []    # tableau contenant le rang de chaque lettre du txt

    for t in txt :
        txt_rang.append(ord(t) - ord('A'))

    cpt = 0          # afin d'avancer bloc par bloc en "superposant" la clé au text
    for tr in txt_rang :
        if cpt > len_k :
            cpt = 0
        stock = tr - key[cpt]
        if stock < 0 :
            stock = stock % len(alphabet)
        res.append( stock )
        cpt = cpt + 1
    txt_return = ""
    for r in res :
        txt_return = txt_return + alphabet[r]
    return txt_return

# Analyse de fréquences
def freq(txt):
    """
    renvoie un tableau avec le nombre d’occurences de chaque lettre de l’alphabet à partir du texte passé en parametre de fonction.
    """
    hist=[0]*len(alphabet)
    for t in txt : 
        hist[alphabet.index(t)] = hist[alphabet.index(t)] + 1

    return hist

# Renvoie l'indice dans l'alphabet
# de la lettre la plus fréquente d'un texte
def lettre_freq_max(txt):
    """
    Renvoie la position dans l’alphabet de la lettre qui apparaît le plus grand nombre de fois dans le texte passé en argument.
    """
    tab = freq(txt)
    res = 0
    val = tab[0]

    for i in range(0, len(tab)) :
        if tab[i] == val and i < res :
            res = i
        if tab[i] > val:
            val = tab[i]
            res = i
    return res

# indice de coïncidence
def indice_coincidence(hist):
    """
    prend en entrée un tableau qui correspond aux fréquences des lettres d’un texte
    et renvoie l’indice de coïncidence.
    """
    n = sum(hist)
    res = 0.0
    for ni in hist :
        res = res + ( (ni*(ni-1)) / (n*(n-1)) )
    return res

# Recherche la longueur de la clé
def longueur_clef(cipher):
    """
    Calcule la taille de la clef. On testera toutes les tailles de clef possibles
    (on suppose que la clef cherchée est au plus de longueur 20)
    """
    ic = []      # Tableau contenant les moyennes des IC de chaque clef traitée
    ic_count = 0 # IC calculé (somme des IC) pour chacun des longueur de clef
    for taille in range(1,21):
        for i in range(0, taille):
            ic_count += indice_coincidence( freq(cipher[i:len(cipher):taille]) )
        ic.append(ic_count / taille) # calcul moyenne ic pour cette chaque longueur de clef et ajout dans ic
        ic_count = 0

    for i in ic:
        if i > 0.06:
            return ic.index(i) + 1 # +1 car notre liste commence à 0
    return 0


# Renvoie le tableau des décalages probables étant
# donné la longueur de la clé
# en utilisant la lettre la plus fréquente
# de chaque colonne
def clef_par_decalages(cipher, key_length):
    """
    Réordonne le text en colonnes allant de 0 à key_length(colonnes)
    cherche la lettre la plus frequente à chaque fois à lequelle on soustrait l'indice de la lettre la plus frequente en alphabet
    """
    decalages=[0]*key_length
    for k in range(0, key_length):
        tmp = lettre_freq_max(cipher[k:len(cipher):key_length]) - freq_FR.index(max(freq_FR))
        decalages[k] = tmp % 26
    return decalages

# Cryptanalyse V1 avec décalages par frequence max
def cryptanalyse_v1(cipher):
    """
    Renvoie le texte dechiffré après avoir trouvé la longueur de la clef 
    """
    key = clef_par_decalages(cipher, longueur_clef(cipher))
    dechiffre = dechiffre_vigenere(cipher, key)
    return dechiffre



################################################################


### Les fonctions suivantes sont utiles uniquement
### pour la cryptanalyse V2.

# Indice de coincidence mutuelle avec décalage
def indice_coincidence_mutuelle(h1,h2,d):
    """
        Renvoie l'indice de concidence mutuelle de h1 et h2 avec un décallage de d
    """
    # On applique le décalage de d positions sur les deux tableaux de frequence
    h2_decale = [h2[ (i+d) % len(h2) ] for i in range(0, len(h2))]
    s = 0
    for i in range(0, len(h2)):
        s += h1[i] * h2_decale[i]

    return s / (sum(h1) * sum(h2))

# Renvoie le tableau des décalages probables étant
# donné la longueur de la clé
# en comparant l'indice de décalage mutuel par rapport
# à la première colonne
def tableau_decalages_ICM(cipher, key_length):
    """
        Renvoie le tableau des décalages probables étant donné la longueur de la clé
    en comparant l'indice de décalage mutuel par rapport à la première colonne
    """
    tab_icm = []
    decalages = [0] * key_length
    colonne_1 = freq(cipher[0: len(cipher): key_length]) # premiere colonne de chaque bloc de longueur key-length

    for i in range(0, key_length):
        colonne_i = freq(cipher[i: len(cipher): key_length])
        for j in range(0, len(alphabet)):
            icm_tmp = indice_coincidence_mutuelle(colonne_1, colonne_i, j)
            tab_icm.append(icm_tmp)
        decalages[i] = tab_icm.index( max(tab_icm) ) # on recupere le d qui maximise l'ICM
        tab_icm = []
    return decalages

# Cryptanalyse V2 avec décalages par ICM
def cryptanalyse_v2(cipher):
    """
    Permet une deuxième forme de cryptanalyse
    -déduction longueur de clef avec IC
    -calcul du décalages de chaque colonne par rapport à la premiere colonne avec ICM
    -décalage de chaque colonne pou raligner avec le première colonne
    -application du dechiffrement avec César
    """
    key_len = longueur_clef(cipher)
    key = tableau_decalages_ICM(cipher, key_len)
    txt_tmp = dechiffre_vigenere(cipher, key)
    freq_max = lettre_freq_max(txt_tmp)
    key = (freq_FR.index(max(freq_FR)) - freq_max) % 26
    return chiffre_cesar(txt_tmp, key)


################################################################


### Les fonctions suivantes sont utiles uniquement
### pour la cryptanalyse V3.
def Var(L1):
    """
        Calcule la varience d'une variable aléatoire passé en parametre
    """
    somme = sum(L1)
    moyenne = somme / len(L1)
    var = 0
    for e in L1:
        var += ( e - moyenne ) **2
    return var / (len(L1) - 1)

def Cov(L1, L2):
    """
        Calcule la covarience des deux variables aléatoires passées en parametre
    """
    sommeL1 = sum(L1)
    sommeL2 = sum(L2)
    moyenneL1 = sommeL1 / len(L1)
    moyenneL2 = sommeL2 / len(L2)
    cov = 0
    for l1, l2 in zip(L1, L2):
        cov += ( l1 - moyenneL1) * ( l2 - moyenneL2 )
    return cov / (len(L1) - 1)

# Prend deux listes de même taille et
# calcule la correlation lineaire de Pearson
def correlation(L1,L2):
    """
        retourne la correlation: cor(L1,Y) = Cov(L1,Y)/sqrt(Var(L1))*sqrt(Var(Y))
    """
    cor = Cov(L1, L2) / (math.sqrt(Var(L1)) * math.sqrt(Var(L2)))
    return cor

# Renvoie la meilleur clé possible par correlation
# étant donné une longueur de clé fixée
def clef_correlations(cipher, key_length):
    """
    Renvoie la moyenne des correlations maximale entre freq_FR et i-eme colonne (i allant
    de 0 à key_length), la clef
    """
    key = []
    cor = []
    score = 0.0
    i = 0
    for i in range(0, key_length):
        liste = []
        for j in range(0, len(alphabet)):
            liste.append(correlation(freq_FR, freq(dechiffre_cesar(cipher[i::key_length],j))))
        cor.append(max(liste))
        key.append(liste.index(max(liste)))

    score = sum(cor) / key_length
    return (score, key)

# Cryptanalyse V3 avec correlations
def cryptanalyse_v3(cipher):
    """
        Renvoie le text cipher déchiffré
    """
    key_len = longueur_clef(cipher)
    score, key= clef_correlations(cipher, key_len)
    text = dechiffre_vigenere(cipher, key)
    return text


################################################################
# NE PAS MODIFIER LES FONCTIONS SUIVANTES
# ELLES SONT UTILES POUR LES TEST D'EVALUATION
################################################################


# Lit un fichier et renvoie la chaine de caracteres
def read(fichier):
    f=open(fichier,"r")
    txt=(f.readlines())[0].rstrip('\n')
    f.close()
    return txt

# Execute la fonction cryptanalyse_vN où N est la version
def cryptanalyse(fichier, version):
    cipher = read(fichier)
    if version == 1:
        return cryptanalyse_v1(cipher)
    elif version == 2:
        return cryptanalyse_v2(cipher)
    elif version == 3:
        return cryptanalyse_v3(cipher)

def usage():
    print ("Usage: python3 cryptanalyse_vigenere.py -v <1,2,3> -f <FichierACryptanalyser>", file=sys.stderr)
    sys.exit(1)

def main(argv):
    size = -1
    version = 0
    fichier = ''
    try:
        opts, args = getopt.getopt(argv,"hv:f:")
    except getopt.GetoptError:
        usage()
    for opt, arg in opts:
        if opt == '-h':
            usage()
        elif opt in ("-v"):
            version = int(arg)
        elif opt in ("-f"):
            fichier = arg
    if fichier=='':
        usage()
    if not(version==1 or version==2 or version==3):
        usage()

    print("Cryptanalyse version "+str(version)+" du fichier "+fichier+" :")
    print(cryptanalyse(fichier, version))

if __name__ == "__main__":
   main(sys.argv[1:])
