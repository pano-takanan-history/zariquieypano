library(ape)

xml_template = '
<distribution id="monophyly.%s" spec="beast.base.evolution.tree.MRCAPrior" monophyletic="true" tree="@Tree.t:tree">
    <taxonset id="taxonset.%s" spec="TaxonSet">
%s
    </taxonset>
</distribution>
'
taxon_template_id = '        <taxon id="%s" spec="Taxon"/>'
taxon_template_idref = '        <taxon idref="%s"/>'


tree <- read.tree(text="((Matses,Matis),(Kaxarari,(Kakataibo,((KashinawaB,KashinawaP),(Pakawara,Chakobo),(ShipiboKonibo,Kapanawa),Amawaka,Arara,Chaninawa,Iskonawa,Kanamari,Katukina,Marinawa,Marubo,Mastanawa,Nawa,Nukini,Poyanawa,Shanenawa,Sharanawa,Yaminawa,Yawanawa))));")

id <- 1
for (s in subtrees(tree)) {
    # first tree is the complete tree
    if (length(s$tip.label) == length(tree$tip.label)) {
        taxa <- sapply(s$tip.label, sprintf, fmt=taxon_template_id, USE.NAMES=FALSE)
    } else {
        taxa <- sapply(s$tip.label, sprintf, fmt=taxon_template_idref, USE.NAMES=FALSE)
    }
    cat(sprintf(xml_template, id, id, paste(taxa, collapse="\n")))
    cat("\n")
    id <- id + 1
}
