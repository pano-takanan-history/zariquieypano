from lingpy import *

def run(wordlist):

    concepts = [
            'hand', 'ear', 'eye', 'nose', 
            #'hair', # ? 
            "root", # !
            'head', 
            'tongue',
            'tooth', 'neck', 'belly', 'back [of body]', 'skin [of person]',
            'tail', 'leg', 'foot', 'wing', 'hand', 'feather [large]', 'heart',
            'guts', 'liver', 
            "tooth [front]", # !
            "mouth", # !
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
    C, A, T, C2 = {}, {}, {}, {}
    best = 1
    best2 = 1
    for idx, concept, tokens, morphemes, cogs in wl.iter_rows("concept", "tokens", "morphemes", "cogs"
            ):
        if len(morphemes) != len(tokens.n):
            print("!", idx, concept, wl[idx, "doculect"], morphemes, tokens)
        if len(morphemes) != len(cogs):
            print(idx, concept, wl[idx, "doculect"], morphemes, cogs)
        else:
            valid = [i for i in range(len(morphemes)) if
                    morphemes[i]]
            valid_string = "{0}-{1}".format(
                    concept, "--".join([morphemes[i] for i in valid]))
            if valid_string in C:
                cogid = C[valid_string]
            else:
                cogid = best
                best += 1
                C[valid_string] = cogid
            A[idx] = (cogid, valid_string)
            
            tok = ["".join(tokens2class([x.split("/")[1] if "/" in x else x for x in
                tokens.n[i]], "sca")) for i in valid]
            tok_string = "{0}-{1}".format(
                        concept,
                        "/".join(tok))
            if tok_string in C2:
                cogid2 = C2[tok_string]
            else:
                cogid2 = best2
                best2 += 1
                C2[tok_string] = cogid2
            T[idx] = cogid2 
    wl.add_entries("body", A, lambda x: x[1])
    wl.add_entries("bodyid", A, lambda x: x[0])
    wl.add_entries("bodytid", T, lambda x: x)

    


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

