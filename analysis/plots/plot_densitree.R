library(treeio)
library(ggplot2)
library(ape)

#remotes::install_github("YuLab-SMU/ggtree")
library(ggtree)


#remotes::install_github("SimonGreenhill/lachesis")
library(lachesis)   # only for get_rootheight


add_clade <- function(p, tree, clade, members, color, offset=500) {
    if (length(members) == 1) {
        # handle singletons
        m <- which(tree$tip.label == clades[[clade]])
    } else {
        m <- ape::getMRCA(tree, members)
    }
    p <- p + geom_cladelabel(
        node=m, label=clade,
        color=c(color, "#333333"),
        #color=color,
        offset=offset,
        offset.text=150,
        extend=0.4,
        barsize=2
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
    "Chama" = c("ShipiboKonibo", "Kapanawa"),
    "Bolivian" = c("Pakawara", "Chakobo"),
    "Kakataibo" = c("Kakataibo"),
    "Kaxarari" = c("Kaxarari"),
    "Northern" = c( "Matis", "Matses")
)

colors <- c(
    "Headwaters" = "#1a3268",
    "Poyanawa" = "#4069a6",
    "Marubo" = "#3a6fb0",
    "Chama" = "#5790c1",
    "Bolivian" = "#a8c9df",
    "Kakataibo" = "#87c27e",
    "Kaxarari" = "#3d7741",
    "Northern" = "#d55f2b"
)


trees <- treeio::read.beast("../beast/pano_covarion_relaxed.trees.gz")

# remove burn-in
trees.subsample <- trees[1001:2001]
# sample a small number
# Note -- too many makes this messy. Play around with it
trees.subsample <- sample(trees.subsample, 200)

# add OTU info so we can color branches
trees.subsample <- lapply(
    1:length(trees.subsample), 
    function(x) groupOTU(trees.subsample[[x]], clades, overlap="origin", connect=FALSE))


p <- ggdensitree(trees.subsample, aes(color=group), alpha=0.2) +
    geom_tiplab(color="#333333") +
    scale_x_continuous(
        breaks = seq(-2000, 0, by = 500),
        limits = c(-2000.0, 1000.0)
    ) +
    theme_tree2() +
    scale_color_manual(values=colors) +
    guides(color="none", fill="none")


for (clade in names(clades)) {
    # hopefully the number of the mrca doesn't change or this won't work
    p <- add_clade(p, trees.subsample[[1]]@phylo, clade, clades[[clade]], colors[[clade]])
}


ages <- data.frame(
    Root=sapply(trees.subsample, get_rootheight)
)

p <- p + geom_density(
    data = ages, aes(-Root, y=..density.. * 750), group = 1,
    inherit.aes = FALSE,
    color = "#333333",
    fill = "#666666",
    size = 0.1,
    alpha = 0.5
)


ggsave('fig_densitree.pdf', p, width=9, height=15)



