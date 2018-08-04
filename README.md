# passphrase_generator
This passphrase generator uses WordNet to generate phrases with approximately 114 bits of
entropy.
The form of each phrase in the current version is

`no. adjective noun adverb verb adjective noun end-of-sentence`

The number, chosen from 2 through 999, provides just under 10 bits of entropy.
The verb can be conjugated in one of two ways, providing an additional bit of entropy.
While there are roughly 8000 words available to the passphrase generator to choose from at the time of writing, there aren't 77 bits of entropy since only a subset of the word list match the grammatical restrictions imposed; instead, about 68 bits of entropy are introduced.
Each word in the phrase is lowercase, UPPERCASE, Capitalised, or dECAPITALISED; this adds 12 bits of entropy (two bits per word). Additionally, up to two symbols may be randomly inserted into the passphrase adding 23 more bits of entropy.

This passphrase generator supports the use of entropy sources such as dice. Run the passphrase generator using `./passer.py 6` and enter the values obtained from dice minus 1 (i.e., 0 through 5 rather than 1 through 6). This will require approximately 220 die rolls (while 220 die rolls provides almost 570 bits of entropy, extra entropy is required to approximate a uniform distribution; consider what happens when you try to choose a number from 1 to 3 using coin flips and want to guarantee you don't keep flipping forever).

Example passphrases include
 * `396 eXTRAORDINARY [Chic#kens Presumably PRESCRIBE sINISTER vAPORS!`
 * `821 pol{ite CURSES iRRITABLY bin alternative DOO[RS?`
 * `72 HONEST Children Quietly fERTILIZE cONTRA!CTUAL STAN$DARDS...`

If you decide that the passphrase as-generated is too hard to remember, you still get 78 bits of entropy if you just keep the number and words like this:
 * `396 extraordinary chickens presumably prescribe sinister vapors`
 * `821 polite curses irritably bin alternative doors`
 * `72 honest children quietly fertilize contractual standards`
