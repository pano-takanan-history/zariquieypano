from lingpy import *

def run(wordlist):

    concepts = [
            'hand', 'ear', 'eye', 'nose', 
            'hair', # ? 
            'head', 'tongue',
            'tooth', 'neck', 'belly', 'back [of body]', 'skin [of person]',
            'tail', 'leg', 'foot', 'wing', 'hand', 'feather [large]', 'heart',
            'guts', 'liver', 
            #'bone', 
            'meat (flesh)', 
            #'fat (grease)', 
            #'blood'
            ]

    D = {0: wordlist.columns}
    count = 1
    for idx, doculect, concept, tokens, morphemes, cogs in wordlist.iter_rows(
            'doculect', 'concept', 'tokens', 'morphemes', "cogs"):
        if concept in concepts:
            tk = basictypes.lists(tokens)
            mp = basictypes.strings(morphemes)
            if str(cogs).strip():
                cogs = basictypes.ints(cogs)
                wordlist[idx, "cogs"] = cogs
            wordlist[idx, 'tokens'] = tk
            wordlist[idx, "morphemes"] = mp
            D[idx] = wordlist[idx]
    
    wl = Wordlist(D)
    C, A = {}, {}
    best = 1
    for idx, concept, morphemes, cogs in wl.iter_rows("concept", "morphemes", "cogs"
            ):
        if len(morphemes) != len(cogs):
            print(idx, concept, wl[idx, "doculect"], morphemes, cogs)
        else:
            valid = [i for i in range(len(morphemes)) if
                    morphemes[i].startswith("_")]
            valid_string = "{0}-{1}".format(
                    concept, "--".join([morphemes[i] for i in valid]))
            if valid_string in C:
                cogid = C[valid_string]
            else:
                cogid = best
                best += 1
                C[valid_string] = cogid
            A[idx] = (cogid, valid_string)
    wl.add_entries("body", A, lambda x: x[1])
    wl.add_entries("bodyid", A, lambda x: x[0])

    


    #wl.add_entries('body', 'cogid', lambda x: 0)
    #for idx in wl:
    #    if len(morphemes) > 1:
    #        morphs = [m for m in wl[idx, 'morphemes'] if m.startswith('_')]
    #        if morphs:
    #            morph = morphs[0]
    #        else:
    #            morph = str(morphemes)
    #    else:
    #        morph = str(wl[idx, 'morphemes'])
    #    wl[idx, 'body'] = morph
    #wl.renumber('body')
    return wl

