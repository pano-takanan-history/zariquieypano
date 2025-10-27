library(treeio)
library(ggplot2)
library(ggtree)


trees <- treeio::read.beast("../beast/pano_covarion_relaxed_words.trees") # slow ...

# remove burn-in
trees.subsample <- trees[2001:3001]
# sample a small number
# Note -- too many makes this messy. Play around with it
trees.subsample <- sample(trees.subsample, 300)

# add OTU info so we can color branches
trees.subsample <- lapply(1:length(trees.subsample), function(x) groupOTU(trees.subsample[[x]], clades, overlap="origin", connect=FALSE))


add_clade <- function(p, tree, clade, members, color, offset=450) {
    if (length(members) == 1) {
        # handle singletons
        m <- which(tree$tip.label == clades[[clade]])
    } else {
        m <- ape::getMRCA(tree, members)
    }
    p <- p + geom_cladelabel(
        node=m, label=clade, color=color,
        offset=offset,
        offset.text=50,
        extend=0.4,
        barsize=5,
        fontsize=10
    )
    p
}

clades <- list(
    "Headwaters" = c(
        "Sharanawa", "Marinawa", "Chaninawa", "Mastanawa", "Nawa",
        "Yaminawa", "Yawanawa", "Shanenawa", "Arara",
        "KashinawaB", "KashinawaP", "Amawaka"
    ),
    "Poyanawa" = c("Poyanawa", "Iskonawa", "Nukini"),
    "Marubo" = c("Marubo", "Kanamari", "Katukina"),
    "Ucayali" = c("ShipiboKonibo", "Kapanawa"),
    "Bolivian" = c("Pakawara", "Chakobo"),
    "Kaxarari" = c("Kaxarari"),
    "Kakataibo" = c("Kakataibo"),
    "Northern" = c( "Matis", "Matses")
)

colors <- c(
    "Bolivian" = "#a8c9df",
    "Headwaters" = "#1a3268",
    "Kaxarari" = "#3d7741",
    "Kakataibo" = "#4E964F",
    "Marubo" = "#3a6fb0",
    "Northern" = "#d55f2b",
    "Poyanawa" = "#4069a6",
    "Ucayali" = "#5790c1"
)

p <- ggdensitree(trees.subsample, aes(color=group), alpha=0.2) +
    geom_tiplab(color="#333333", size=9) +
    scale_x_continuous(
        breaks = seq(-2000, 0, by = 500),
        limits = c(-2100.0, 700.0)
    ) +
    theme_tree2(axis.text.x = element_text(size=26) ) +
    scale_color_manual(values=colors) +
    guides(color="none")


for (clade in names(clades)) {
    # hopefully the number of the mrca doesn't change or this won't work :)
    p <- add_clade(p, trees.subsample[[1]]@phylo, clade, clades[[clade]], colors[[clade]])
}

ggsave('fig_densitree.pdf', p, width=20, height=20, dpi=500)
