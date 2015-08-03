# passphrase_generator
This passphrase generator uses WordNet to generate phrases with approximately 114 bits of
entropy.
The form of each phrase in the current version is
`no. adjective noun adverb verb adjective noun end-of-sentence`
This provides approximately 79 bits of entropy with the tested WordNet database.
Each word in the phrase is lowercase, UPPERCASE, Capitalised, or dECAPITALISED; this adds 14 bits of entropy. Additionally, up to two symbols may be randomly inserted into the passphrase adding 21 more bits of entropy.

Example passphrases include
 * `396 eXTRAORDINARY [Chic#kens Presumably PRESCRIBE sINISTER vAPORS!`
 * `821 pol{ite CURSES iRRITABLY bin alternative DOO[RS?`
 * `72 HONEST Children Quietly fERTILIZE cONTRA!CTUAL STAN$DARDS...`
