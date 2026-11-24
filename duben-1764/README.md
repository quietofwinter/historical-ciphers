# Swedish envoy at St Petersburg to "Mon cher Comte", early 1764 (cipher letter "96.70.171…")

**Status: first known partial solution.** About 91% of the 1,657 cipher groups have a value. The text reads in gist, and this page gives a summary, not a full translation.

## The document

Riksarkivet (Swedish National Archives), Kungliga arkiv, Drottning Lovisa Ulrika, Utgångna skrivelser, SE/RA/710003/02/008/b/K 259. The letter is on images 90 right to 93 left, in the folder headed "Chiffer n:o 1". It is all numbers: 3-digit groups separated by dots, with heavy slashes marking word divisions. It opens 96.70.171 and closes …36.96.743.

No contemporary decipherment is filed with it. The clear letter of 30 January on images 94–95 is a different text. The cyphersolver catalogue (no. 450) listed this letter as "not transcribed".

Scans (public domain, Riksarkivet IIIF):
- [image 90](https://sok.riksarkivet.se/bildvisning/A0073297_00090)
- [image 91](https://sok.riksarkivet.se/bildvisning/A0073297_00091)
- [image 92](https://sok.riksarkivet.se/bildvisning/A0073297_00092)
- [image 93](https://sok.riksarkivet.se/bildvisning/A0073297_00093)

## What the letter says

The writer is the Swedish envoy at the Russian court. He writes in French to "Mon cher Comte" and defends himself against suspicions at the Swedish court.

- **His defence.** "Il seroit difficile, [mon] cher Comte, de vous exprimer" (it would be hard, my dear Count, to express to you) the pain "que m'a causé" (that has been caused him by) what he has just received. It would be hard to express his pain at what he has just received. Nothing could hurt more than being doubted in his zeal for the service of Their Majesties, after doing everything in the world to prove his attachment, only to see how useless his efforts have been.
- **The Empress.** He carried the King's assurances to the Empress and "n'ai rien négligé" (neglected nothing) to press her to make good on them. He did everything humanly possible to fulfil his task. If the unhappy turn of affairs kept him from succeeding, it is assuredly not his fault. The promises the Empress had made came to nothing.
- **Panin and the Polish election.** Count Panin showed more and more doubts about Swedish sincerity, "alléguant le peu de confiance que cette [Princesse] témoignoit à ses anciens serviteurs" (citing the little confidence that this Princess showed her old servants) and her visible preference for "le parti [de] France" (the French party). After what happened at the election of the marshal (of the Polish Diet), every other step became useless. He notes the political system the Empress follows in concert with the King of Prussia.
- **No access.** Since the beginning he has had hardly any access to her. She has spoken to him only a few times, and he barely gets to pay his respects.
- **His innocence.** On one side he has neglected nothing in his duty. On the other, he detests, as he always has, "tout ce qui s'appelle persécution" (all that is called persecution), and his way of thinking on this is invariable. He has sacrificed his rest, his health and the little he owns. He counts on Their Majesties' kindness and justice and asks the Comte to plead his cause.
- **Close.** He wishes that the measures taken "en une conjoncture aussi délicate" (in so delicate a conjuncture) may "contribuer solidement à leur bonheur" (contribute solidly to their happiness), and ends with protestations of devotion.

## How it was read

1. **Transcription.** All four pages were transcribed from the full-resolution scans: one pass, 1,657 groups (`transcription/`). The 5 and 8, and the 3 and 5, are sometimes hard to tell apart.
2. **Base key.** `key/key_c01_base.json` is the system A key rebuilt by Brice Dudout from a sibling letter in the same volume and its contemporary decipherment (cyphersolver project, `targets/duben1764/dudout/system_a`, CC BY 4.0). It was never applied to this letter. On its own it gives a value to 78% of the groups.
3. **Corrections.** The code is a one-part, alphabetical, syllabic codebook (e.g. 505 pe, 507 po, 510 pu), so each unknown group's neighbours narrow down its value. `key/corrections.json` holds the values corrected or added here from context:
   - Groups below 100 are nulls.
   - Examples: 507 po (*j'ai porté*), 305 ge (*négligé*), 675 voir (*recevoir*, *devoirs*), 304 ga (*engagements*), 247 ec (*élection*), 629 tri / 151 bu (*contribuer*), 542 qui, 575 sur, 346 ja (*jamais*), 678 vous / 241 e / 689 x (*vous exprimer*), 533 princesse, 300 france, 308 gu / 127 ant (*alléguant*), 355 ig (*témoignoit*), 416 li (*politique*), 334 hu (*humainement*).
4. **Decode.** `decipherment/decode.txt` is the output of `python3 scripts/decode.py transcription/p9*.txt`. Unknown groups are shown in brackets.

## Second pass (23 Nov 2026)

- **Spot check:** line 1 of image 90 was re-read at twice native size. One misreading was corrected: 613 is 618 (*cher Comte*). Enlarging past the scan's native resolution adds no detail, so this pass mostly filled gaps from context and from the alphabetical order of the codebook.
- **Coverage:** groups with a value went from 78% (base key) to 91% (97 values corrected or added).
- **Not yet done:** a full group-by-group re-reading of all four pages against the scans.

## Limits

- **Transcription:** one reader and one pass. A second reading against the scans is still to do.
- **Key:** about 9% of groups still have no value, and many corrections are inferences from context rather than values confirmed elsewhere.
- **Not tested:** no held-out control test has been run.
- **Open questions:** the opening groups (171, 732, 727, 710) and the signature groups (742, 743) are not identified. The writer's name and the exact date are not fixed. The content and the volume point to C. W. von Düben's St Petersburg correspondence of early 1764.
