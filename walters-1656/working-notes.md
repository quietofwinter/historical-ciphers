# Walters cipher (Thurloe State Papers vol. 5) - working notes, 2026-11-19

## Target
Two "intercepted" letters printed in Thurloe State Papers vol. 5 with raw cipher numbers (never deciphered in the 1742 edition):
- 22 Aug 1656, signed "Jo. Waddall", to "Mons. Vanyeare marchant ... en Bruges" (vol. xli p. 642)  BHO vol5/pp333-350
- 29 Aug 1656, signed "Jo. Weddall", indorsed "Walters" (vol. xli p. 842)                          BHO vol5/pp351-368
Same hand, spelling and cipher. Writer = John Walters, who also writes to Thurloe in clear on 1 July 1656 (vol5/pp173-186, "Jno. Walters"),
same phonetic spelling (consarning, busenesse, myty). So he is Thurloe's informant corresponding with royalists at Bruges.
Only these two letters in vols 4-6 use this cipher (searched for the "50 14" digraph and the names). 122 cipher tokens, 49 distinct.
Text with cipher groups: letters.txt

## System (working view)
Numbers under 100 = letters with homophones AND some syllables; 200+ = code words (210,211,212,226,242,243).

## Values held with some confidence
50=t 14=h 11=e  ("the", "-moth", "Thom", "Thurl")
46=r 18=s        ("the strats" = the Straits; "Thurl")
38=m 40=o 86=o   ("Plemoth", "Tom", "Thom")
19=c             ("[75]tch" = Ritch = Col. Rich, sent prisoner to Windsor Aug 1656)
Probable: 48=s, 17=a, 79=s, 7=a, 43=p, 27=l, 15=u, 51=l(o), 49="ail"/"hips" (thirty/twelve s-49 = sail/ships), 226=men.

## Readings so far
- "half of them are gone to the Strats" (Blake's squadron into the Straits, summer 1656)
- "thirty sail at Jemica; twelve sail at [13 27 e s]" (Cales/Cadiz?)
- "sent to lie near Plemoth"
- "Tom is strictly looked to"; "[43 37 e 56] Thom is so far out of favour now that Thurl[oe] told me he had a greater mind to .. him than .."
- "Thurl[oe] hath promist me that he shall be able to do no more against me"
- "[Ritch] is sent prisoner to Winsor"
- "one whom the s-a-[men] love extremely had a guard set over him, was four days waiting before he could speak with the ..."

## Unresolved / conflicts
- W1 "7 74 30 54 29 50": "a fleet" (letters) vs "a re-gi-m-en-t" (syllables); W2 "39 46 48": "?rs" (ho-r-s = horse?)
- W4 "17 38 63 60 11 48" = a m ? ? e s : no reading yet
- "90 50 48 46" = ? t s r (master?) conflicts with 48=s
- Identity of the man the seamen love (48 54 81 39) - Lawson expected historically, does not fit letter-for-letter
- 122 tokens is too little for the statistical solver; this needs context work or more text in the same cipher.

## Not yet done
- Prior-art check (Underdown, Royalist Conspiracy; Aubrey, Mr Secretary Thurloe; any decipherment of Walters letters)
- Look for further Walters letters in the Rawlinson MSS / other Thurloe volumes (1, 2, 3, 7)

# Update (second pass, same day)

## Breakthrough: the cipher is a SYLLABARY
Numbers under 100 stand for single letters AND consonant+vowel syllables. This explains the low repeat rate.
The writer's own clear text has "a regement of horse", and the cipher group 7 74 30 54 29 50 + 39 46 48 reads
a-re-ge-me-n-t of ho-r-s with one value per number, all consistent elsewhere.

## Current key (number = value)
7=a  10=d  11=e  13=ca/c  14=h  15=u  16=co  17=a(ea/ai)  18=s  19=c  25=f  26=fo  27=l(al)  29=n  30=ge  35=hi  37=l?
38=m  39=ho  40=o  43=p/f  46=r  48=s  49=ail  50=t  51=lo  52=w(ou)  53=u?  54=me  58=i  59=in  60=ni  63=pa
74=re  75=ri  78=s  79=se  86=o  89=land  90=ma?   226=men (code word)
Probable print/copy slips: G4 first number printed 17, should be 16 ("co-m-pa-ni-e-s"); "90 50 48 46" = ma-t-s-r for "mastr".

## Readings
L1 (22 Aug 1656): "There is a regement of hors sent to lie near P/F-l-emoth [Plymouth or Falmouth], and six companies of [243] men
are sent to strengthen Hu-l(?) [Hull?], and [F/P ? e ? t-h-o-m] is so far out of favour now, that Thurlo told me he had a
greater mind to [33 ho 13] him than [33 l s e]."
L2 (29 Aug 1656): "...concerning the Iland, no man better; he is a mastr to it. He tells me there is thirty sail at Jemica;
twelve sail at Cales, but them are divided, half of them are gone to the Strats; and hereupon the last of [210 211] and [212].
Here is forti sail; [s-me-?-ho], one who the seamen love extremely, had a guard set over him, was four days waiting before he
could get to speak with the Cownsel, which he took very ill; Ritch is sent prisoner to Winsor, and every day one or other
confined. My friend's name is Mr. [W-u-s?] ... Tom is strictly looked to; Thurlo hath promist me ..."

## Still open
- G7 name "43 37 11 56 50 14 86 38" (?-l-e-?-t-h-o-m); G9/G10 "33 39 13" / "33 37 48 11"; G18 name "48 54 81 39";
  G24 "Mr. 52 15 48"; G6 "14 53 37" (Hull? him?); code words 210, 211, 212, 242, 243.
- Historical check: a Thurloe letter of intelligence of Aug 1656 says the government was proceeding against
  "Okey, Lawson, Rich, Ludlowe" - fits "Ritch ... prisoner" and "every day one or other confined". The man the seamen love
  ought to be Lawson, but 48 54 81 39 does not spell Lawson under the current key.
- Prior art: web search found no decipherment of the Waddall/Weddall (John Walters) letters.

# Update 3: Underdown, Royalist Conspiracy in England (pages supplied by Jason)
- p.174-75: John Walters, brother of the Yorkshire agent Robert Walters, entered Thurloe's service c.1655. April 1656 delivered a
  letter from the King to Sir Henry Slingsby after letting Thurloe's officer copy it; went to Antwerp with messages for exiles;
  wrote a full account to Thurloe. "Thurloe's employment of Walters evidently came to an end in August 1656."
- n.30: "There are some obscure letters from Walters, under the pseudonym 'Weddall,' in TSP, 5, 337, 364-65, and Rawl. MS A 41,
  pp. 498, 556." -> Underdown did not read them. Rawl. A 41 = Thurloe vol. xli. The pp. 498/556 may be two FURTHER letters
  (TSP prints xli pp. 642 and 842) or the same two under another pagination - to check at the Bodleian.
- p.319: of the paid spies only Priestman and John Walters were never unmasked.
- App. F "Cipher with John Cooper" (Cl. MS 94 fol. 13): jargon names incl. "Thompson, Mr = James [John?] Walters";
  endorsement gives C o o p e r = 9 39 40 44 14 49. Tested: Walters letters do NOT fit an alphabetical block cipher of that type
  (blocks.py; anchors never matched, no readable text). Different cipher.
- Context for names: northern Action party - Tynemouth, Hull, York; Fairfax ("Black Tom"), Slingsby, Armorer, Darcy, Mauleverer,
  Paulden, Carnaby, Gilby, Savile. Lead (unproven): "Tom"/"Thom" in both letters = Fairfax.
