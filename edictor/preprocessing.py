from lingpy import *

def run(wordlist):

    concepts = [
            'hand', 'ear', 'eye', 'nose', 'hair', 'head', 'tongue',
            'tooth', 'neck', 'belly', 'back [of body]', 'skin [of person]',
            'tail', 'leg', 'foot', 'wing', 'hand', 'feather [large]', 'heart',
            'guts', 'liver', 'bone', 'meat (flesh)', 'fat (grease)', 'blood']

    D = {0: wordlist.columns}
    count = 1
    for idx, doculect, concept, tokens, morphemes in wordlist.iter_rows(
            'doculect', 'concept', 'tokens', 'morphemes'):
        if concept in concepts:
            tk = basictypes.lists(tokens)
            mp = basictypes.strings(morphemes)
            wordlist[idx, 'tokens'] = tk
            D[idx] = wordlist[idx]
    
    wl = Wordlist(D)
    wl.add_entries('body', 'cogid', lambda x: 0)
    for idx in wl:
        if len(morphemes) > 1:
            morphs = [m for m in wl[idx, 'morphemes'] if m.startswith('_')]
            if morphs:
                morph = morphs[0]
            else:
                morph = str(morphemes)
        else:
            morph = str(wl[idx, 'morphemes'])
        wl[idx, 'body'] = morph
    wl.renumber('body')
    return wl

