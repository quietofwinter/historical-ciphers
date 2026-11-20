# Scripts

- `build_ngram.py` builds a letter 5-gram table from plain-text corpora (public-domain Project Gutenberg texts were used).
- `hsolve.c` is a simulated-annealing solver for homophonic substitution, scored with that table. Clear words around the
  cipher groups can be fixed so they act as context.

`render_letters.py` draws `images/letter1-deciphered.png` and `letter2-deciphered.png` from `../letters-annotated.txt`.

The solver files were used for the first passes. With only 122 cipher numbers in two letters, the solver alone could not finish the job;
the syllable structure and most readings came from working the groups against the surrounding clear text by hand.
