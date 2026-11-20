"""Data for the Louis XIV - Chaulnes letter of 10 July 1690: the letter, word by word, with the value read for every cipher group.
Writes ../letter-annotated.txt, ../ciphertext.txt and ../key.md, and checks that the groups below reproduce the transcription.

usage: python3 build_entry.py
"""
import collections, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); UP = os.path.join(HERE, "..")
NULL = "[-]"

# Each cipher word: (kind, reading, "number=value number=value ...").  kind: d = read, t = tentative or one figure off.
# Clear text is given as plain strings (French, after the transcription on the Traces Ecrites page, checked against the photographs).
LETTER = [
"Mon Cousin, J'ay receu tant par l'ordinaire de Rome que par celuy de Venise les originaux et duplicata de vos lettres des 8, 12 et 17 juin qui m'informent de toutes les diligences que vous avez faites pour",
("d", NULL, "201=-"), ("d", "porter", "459=po 170=r 523=te 172=r"), ("d", "le", "381=le"), ("d", "Pape", "477=pape"), ("d", NULL, "201=-"),
("d", "à", "10=a"), ("d", "se", "508=se"), ("d", "contenter", "141=co 140=n 527=ten 523=te 172=r"), ("d", "d'une", "309=du 433=ne"),
("d", "lettre", "386=lettre"), ("d", "de", "306=de"), ("d", "ma", "407=ma"), ("d", NULL, "201=- 203=-"), ("d", "main", "407=ma 30=i 142=n"),
("t", "et", "12=a"), ("d", "d'une", "309=du 433=ne"), ("t", "autre", "27=autre"), ("d", "signée", "509=si 102=g 433=ne 22=e"),
("d", "des", "306=de 180=s"), ("d", NULL, "209=- 201=-"),
"Evesques qui ont assisté à l'assemblée du clergé de 1682",
("d", "suivant", "513=su 32=i 97=va 446=nt"), ("d", "les", "396=les"), ("t", "projets", "150=p 491=ro 77=je 170=r 180=s"), ("d", "que", "481=que"),
("d", "je", "77=je"), ("d", "vous", "107=vous"), ("d", "ay", "12=a 32=y"), ("d", "envoyés.", "51=envoy 22=e 180=s"),
("d", "Quant", "479=qua 446=nt"), ("d", "au", "23=au"), ("d", "premier,", "150=p 488=re 409=mi 22=e 170=r"),
"Il est bien raisonnable que la Cour de Rome demandant que lesd. Evesques déclarent par leurs lettres qu'ils n'ont point prétendu par les quatre articles que l'assemblée a publiés sur la puissance ecclésiastique faire une décision de foy, encore moins d'établir un dogme, elle doit aussy souffrir qu'ils adjoutent que cette assemblée a seulement voulu faire une simple déclaration de ses sentiments qui ont toujours esté ceux de l'Eglise de France, et c'est aussy l'expédient que vous m'avez écrit par votre lettre du 25e avril",
("d", NULL, "5=( 47=* 53=* 6=)"), ("d", "avoir", "10=a 106=voir"), ("d", "proposé", "473=propos 20=e"), ("d", "au", "23=au"), ("d", "Cardinal", "138=cardinal"),
("d", "Albani", "12=a 122=l 118=ba 434=ni"), ("d", NULL, "207=-"),
", qui estoit de mettre après la profession de foy exprimée dans led. projet, que lesd. Evesques avoient toujours esté dans les mesmes sentimens, et ne s'en estoient jamais séparés, dont mesme vous me mandiez qu'",
("d", "il", "65=il"), ("d", "avoit", "23=au 89=oit"), ("d", "paru", "456=pa 493=ru"), ("d", "satisfait", "507=sa 524=ti 180=s 325=fait"),
"et que vous croyez",
("d", "l'avoir", "370=la 106=voir"), ("d", "persuadé.", "457=pe 170=r 513=su 10=a 306=de"), ("d", NULL, "201=-"), ("d", "Si", "509=si"), ("t", "[néanmoins?]", "443=?"),
("d", "vous", "107=vous"), ("d", "jugez", "83=jug 356=ge 310=z"), ("d", "que", "481=que"), ("d", "pour", "469=pour"), ("d", "terminer", "523=te 170=r 409=mi 433=ne 172=r"),
("d", "ce", "137=ce"), ("d", "différent", "313=diff 20=e 488=re 446=nt"), ("d", "et", "22=e 190=t"), ("d", "obtenir", "42=o 62=b 523=te 434=ni 170=r"),
("d", "du", "309=du"), ("d", "Pape", "477=pape"), ("d", "la", "379=la"), ("t", "promte", "152=p 491=ro 172=r 523=te"), ("d", "expédition", "20=e 300=x 457=pe 307=di 535=tion"),
("d", "des", "306=de 180=s"), ("d", "bulles", "124=bu 122=l 396=les"), ("d", "il", "65=il"), ("d", "faille", "327=fa 65=il 381=le"),
("t", "retrancher", "488=re 172=r 487=ra 142=n 70=c 371=he 170=r"), ("d", NULL, "201=-"), ("d", "cette", "168=cette"), ("t", "[addi?]tion,", "48=? 47=? 535=tion"), ("d", NULL, "200=-"),
("d", "vous", "107=vous"), ("d", "m'envoyerez", "130=m 51=envoy 488=re 310=z"), ("d", "la", "370=la"),
("d", "⟨cancelled: dernière copie⟩", "2=( 306=de 172=r 434=ni 22=e 488=re 141=co 458=pi 22=e 3=)"),
("t", "copie", "141=co 485=pi 22=e"), ("d", "des", "306=de 180=s"), ("d", "derniers", "306=de 170=r 434=ni 22=e 170=r 180=s"), ("d", "projets", "152=p 491=ro 77=je 190=t 182=s"),
("t", "dont", "196=dont"), ("d", "vous", "107=vous"), ("d", "serez", "508=se 488=re 312=z"), ("d", "convenu,", "141=co 142=n 98=ve 436=nu"), ("d", "avant", "23=au 10=a 446=nt"),
("d", "que", "481=que"), ("d", "de", "306=de"), ("d", "m'engager", "408=me 140=n 355=ga 356=ge 172=r"), ("d", "positivement", "459=po 509=si 524=ti 98=ve 404=ment"),
("d", "à", "12=a"), ("d", "y", "32=y"), ("d", "consentir,", "141=co 140=n 506=sen 524=ti 172=r"), ("d", "et", "20=e 190=t"),
"ceux qui ont assisté à l'assemblée de 1682 et qui sont nommés aux Archeveschés et Eveschés",
("d", NULL, "2=( 47=* 49=* 3=)"), ("d", "à", "12=a"), ("d", "le", "381=le"), ("d", "signer.", "509=si 102=g 433=ne 170=r"),
"Quoyque j'aye toujours cru que l'affaire de la Régale ne recevroit aucune difficulté, quand vous vous en expliquez de la manière que je vous l'ay écrit, neantmoins comme vous avés jugé plus à propos jusqu'à présent de",
("d", "remettre", "488=re 408=me 190=t 192=t 488=re"), ("d", "cette", "168=cette"), ("d", "affaire", "10=a 92=f 341=faire"), ("d", "aprez", "10=a 152=p 488=re 310=z"),
("d", "que", "481=que"), ("d", "celle", "70=c 58=elle"), ("d", "des", "306=de 180=s"), ("d", "bulles", "124=bu 120=l 396=les"), ("d", "seroit", "508=se 170=r 89=oit"),
("d", "terminées,", "523=te 172=r 409=mi 433=ne 22=e 182=s"),
"vous devez d'autant moins changer de conduite dans l'estat présent des affaires qu'",
("d", "elle", "58=elle"), ("d", "pourroit", "469=pour 170=r 89=oit"), ("d", "donner", "314=donne 172=r"), ("d", "lieu", "383=li 22=e 50=u"), ("d", "à", "10=a"), ("d", "de", "306=de"),
("d", "nouveaux", "439=nou 98=ve 23=au 302=x"), ("d", NULL, "201=-"), ("d", "retardemens", "488=re 521=ta 170=r 306=de 404=ment 180=s"), ("d", "qui", "483=qui"), ("d", NULL, "207=-"),
"ne conviennent point à mes intérests, et c'est aussy ce qui me fait approuver les pressantes instances que vous avés faites",
("d", "par", "456=pa 170=r"), ("d", "la", "379=la"), ("d", "voie", "101=vo 30=i 22=e"), ("d", "des", "306=de 180=s"), ("d", "Cardinaux", "138=cardinal 52=u 300=x"),
("t", "[Ottoboni?]", "96=?"), ("d", "et", "22=e 190=t"), ("d", "Albani", "12=a 122=l 118=ba 434=ni"),
"et préconiser au plutôt les Eveschés indifféremment, avec protestation de sortir de vos engagemens et de retirer tous les projets de lettres que vous avés donnés.",
"\n",
"Il y a cependant bien de l'apparence que l'assemblée du clergé sera finie avant que vous ayés terminé toutes ces difficultés et qu'ainsy elle ne sera plus en estat d'écrire au Pape en la manière que je vous l'avois fait espérer.",
"\n",
"Il faut qu'on n'ait pas esté curieux jusqu'à présent à la Cour où vous estes de lire toutes les impertinences que quelques François des plus emportés contre notre Religion se donnent la liberté de faire imprimer dans leurs gazettes qu'ils appellent lardons, pour s'estonner de ce que contient celuy que vous m'avez envoyé qui est du mesme style que tous les autres et qui doit faire voir au Pape que les ennemis de la Religion Catholique croyent qu'ils ne leur manque plus rien pour la détruire que de mettre la division entre le Pape et moy et que la Maison d'Autriche unie avec eux leur donnera moyen de faire triompher l'hérésie par toute l'Europe, mais la victoire qu'il a plu à Dieu donner à mes armes confondra tous les projets, et je m'assure que le Pape leur fera bientost perdre toute l'espérance qu'ils ont eue de luy inspirer les mesmes sentimens qu'à son prédecesseur.",
"\n",
"Je vous envoye un mémoire concernant l'estat présent des Religieuses de Ste Claire de Rheims, et je désire que pour les raisons qu'il contient, vous demandiés au Pape un Bref pour la continuation de la supériorité en faveur de soeur Agnès Colbert, pareil à celuy que le feu Pape accorda pour le mesme sujet, et dont je vous envoye coppie.",
"\n",
"J'envoye aussy au Sr Ratabon le passeport que vous avez demandé pour le Cardl Durazzo, quoyqu'il n'en ait besoin que pour se rendre à son evesché de Carpentras.",
"\n",
"Je suis averty que les ministres d'Espagne ne laissent rien d'intenté pour rétablir ceux de la R.P.R. dans les provinces de Dauphiné et de Provence, et qu'ils veulent porter leurs alliés à joindre aux Vaudois et François Calvinistes un corps de trouppes Protestantes assez considérable, non seulement pour appuyer et fomenter les desseins des séditieux hérétiques, mais aussy pour passer en Italie souz le prétexte de secourir le duc de Savoye, et quoy que les forces que je leur opposeray pourront bien confondre leurs projets, neantmoins il est bon d'en informer le Pape, affin qu'il prenne les mesures qu'il croira les plus convenables au bien de notre Religion. Sur ce je prie Dieu qu'il vous ait, Mon Cousin, en sa Ste et digne garde. Ecrit à Versailles le 10e juillet 1690.",
"\n",
"Louis. [countersigned] Colbert",
]

# The whole letter in English. [[...]] = words that were in cipher; <<...>> = cipher words that are tentative or have one figure off.
ENGLISH = [
"My Cousin, I have received, both by the ordinary post from Rome and by that from Venice, the originals and duplicates of your letters of 8, 12 and 17 June, which inform me of all the efforts you have made [[to bring the Pope to content himself with a letter in my own hand]] <<and another>> [[signed by the]] bishops who attended the Assembly of the Clergy of 1682, [[following the]] <<drafts>> [[I sent you. As to the first,]] it is quite reasonable that, since the Court of Rome asks the said bishops to declare by their letters that they did not intend, by the four articles which the Assembly published on ecclesiastical power, to make a decision of faith, still less to establish a dogma, it should also allow them to add that this Assembly wished only to make a simple declaration of its sentiments, which have always been those of the Church of France; and this is also the expedient which you wrote to me, in your letter of 25 April, [[that you had proposed to Cardinal Albani,]] which was to put, after the profession of faith expressed in the said draft, that the said bishops had always been of the same sentiments and had never departed from them; you even told me that [[he had appeared satisfied]] and that you believe [[you have persuaded him. If]] <<[nevertheless?]>> [[you judge that, to end this dispute and obtain from the Pope the]] <<prompt>> [[dispatch of the bulls, it is necessary to]] <<cut out>> [[this]] <<[addition?],>> [[you will send me the]] <<copy>> [[of the latest drafts]] <<on which>> [[you have agreed, before I commit myself positively to consenting to it, and]] those who attended the Assembly of 1682 and who are named to archbishoprics and bishoprics [[to signing it.]]",
"Although I have always believed that the matter of the R\u00e9gale would meet with no difficulty once you explained yourself on it in the manner I wrote to you, nevertheless, as you have so far judged it better to [[put that matter off until the matter of the bulls is finished,]] you should change your conduct all the less in the present state of affairs since [[it could give rise to new delays which]] do not suit my interests; and this is also what makes me approve the pressing requests you have made [[through Cardinals]] <<[Ottoboni?]>> [[and Albani]] and to have the bishoprics preconized as soon as possible without distinction, with a formal declaration that you would withdraw from your undertakings and take back all the draft letters you have given.",
"There is, however, every appearance that the Assembly of the Clergy will be over before you have ended all these difficulties, and that it will thus no longer be in a position to write to the Pope in the manner I had led you to hope.",
"People at the Court where you are must not until now have been curious to read all the impertinences which some Frenchmen, among the most violent against our religion, take the liberty of having printed in their gazettes, which they call lardons, if they are astonished at the contents of the one you sent me, which is in the same style as all the others, and which ought to show the Pope that the enemies of the Catholic religion believe they need nothing more to destroy it than to set division between the Pope and me, and that the House of Austria, united with them, will give them the means to make heresy triumph throughout Europe; but the victory which it has pleased God to give to my arms will confound all their projects, and I am confident that the Pope will soon make them lose all the hope they have had of inspiring in him the same sentiments as in his predecessor.",
"I am sending you a memorandum on the present state of the nuns of Sainte-Claire of Reims, and I desire that, for the reasons it contains, you ask the Pope for a brief continuing Sister Agn\u00e8s Colbert as superior, like the one which the late Pope granted for the same purpose, of which I send you a copy.",
"I am also sending the sieur Ratabon the passport you asked for Cardinal Durazzo, although he needs it only to go to his bishopric of Carpentras.",
"I am informed that the ministers of Spain leave nothing untried to re-establish those of the so-called Reformed religion in the provinces of Dauphin\u00e9 and Provence, and that they wish to induce their allies to join to the Vaudois and the French Calvinists a body of Protestant troops considerable enough not only to support and foment the designs of the seditious heretics, but also to pass into Italy on the pretext of helping the Duke of Savoy; and although the forces I shall oppose to them may well confound their projects, it is nevertheless good to inform the Pope of it, so that he may take the measures he thinks most fitting for the good of our religion. With this I pray God to have you, my Cousin, in his holy and worthy keeping. Written at Versailles, 10 July 1690.",
"Louis. [countersigned] Colbert",
]

def english_markup(par):
    def rep(kind):
        return lambda m: " ".join("{%s|%s}" % (kind, w) for w in m.group(1).split())
    par = re.sub(r"\[\[(.*?)\]\]", rep("d"), par)
    return re.sub(r"<<(.*?)>>", rep("t"), par)

def main():
    out = ["# Louis XIV to the duc de Chaulnes, Versailles, 10 July 1690. Clear text after the transcription published by Traces Ecrites,",
           "# checked against the photographs. Markup: {d|reading|cipher} deciphered; {t|reading|cipher} tentative, or one figure differs from the key.",
           "# [-] = groups without meaning (nulls, and the bracket pairs 2...3 and 5...6 with what they enclose).", "",
           "=== Louis XIV to the duc de Chaulnes, ambassador in Rome. Versailles, 10 July 1690. (Signed letter, 5 pp.; sold by Traces Ecrites, ref. 11273)"]
    par, groups, vals = [], [], collections.defaultdict(list)
    for item in LETTER:
        if item == "\n":
            out.append(" ".join(par)); par = []
        elif isinstance(item, str):
            par.append(item)
        else:
            kind, reading, spec = item
            nums = []
            for pair in spec.split():
                n, v = pair.split("="); nums.append(n); groups.append(int(n)); vals[int(n)].append((v, reading, kind))
            punct = ""
            m = re.fullmatch(r"(.*?)([.,]+)", reading)
            if m and reading != NULL: reading, punct = m.group(1), m.group(2)
            par.append("{%s|%s|%s}%s" % (kind, reading, " ".join(nums), punct))
    out.append(" ".join(par))
    out += ["", "=== The letter in English. (Translation of the whole letter; the words that were in cipher are in colour)"] + [english_markup(p) for p in ENGLISH]
    open(os.path.join(UP, "letter-annotated.txt"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    open(os.path.join(UP, "ciphertext.txt"), "w").write(
        "# The 301 cipher groups of the letter in order, read from the photographs (see README for the corrected readings).\n" + " ".join(map(str, groups)) + "\n")
    # key table
    rows = ["# Key: every number used in the letter", "",
            "Confidence: **A** = the value is fixed by the layout rule and/or by two or more different words; **B** = one word, but it fits the alphabetical order;",
            "**C** = tentative. \"-\" = no meaning (null); \"(\" and \")\" = brackets round groups to be ignored.", "",
            "| Number | Value | Times | Words | Confidence |", "|---|---|---|---|---|"]
    for n in sorted(vals):
        vs = list(dict.fromkeys(x[0] for x in vals[n]))
        if "?" in vs and "*" in vs: vs.remove("*")
        v = "/".join(vs).replace("*", "filler inside brackets, not read"); words = []
        for _, w, k in vals[n]:
            w = w.strip(".,")
            if w not in words and NULL not in w: words.append(w)
        tent = v == "?" or v.startswith("filler") or all(k == "t" for _, _, k in vals[n])
        letter = (n < 200 and n % 10 in (0, 2)) or n in (300, 302, 310, 312)
        conf = "C" if tent else ("A" if (letter or len(words) >= 2 or v in "-()") else "B")
        rows.append("| %d | %s | %d | %s | %s |" % (n, v, len(vals[n]), ", ".join(words[:4]), conf))
    open(os.path.join(UP, "key.md"), "w", encoding="utf-8").write("\n".join(rows) + "\n")
    return groups

if __name__ == "__main__":
    g = main(); print(len(g), "groups,", len(set(g)), "distinct")
