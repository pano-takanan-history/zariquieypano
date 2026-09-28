# Setup renv
library(renv)
# renv::init()
# renv::snapshot()
renv::activate()
# renv::restore()

# Load packages
library(treeio)
library(ggplot2)
library(ape)

# library(remotes)
#remotes::install_github("YuLab-SMU/ggtree")
library(ggtree)


# root height = distance from root to the furthest tip
# (replaces lachesis::get_rootheight)
get_rootheight <- function(tree) {
    if (inherits(tree, "treedata")) tree <- tree@phylo
    max(ape::node.depth.edgelength(tree))
}


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

transitions <- data.frame(
    parameter = c("Start Yarinacocha", "Start of post-Yarinacocha period",
                  "Start Cumancaya", "Start Caimito"),
    label = c("Yarinacocha", "Pacacocha", "Cumancaya", "Caimito"),
    color = c("#b4b4b4", "#fa73bf", "#a1e573", "#ffa300"),
    label_x = c(-1550, NA, NA, NA)
)

add_transitions <- function(p, file, transitions, height=1, scale=750, spacing=1.5,
                            overlap=6, label.x=-2600, bp_offset=50) {
    post <- read.csv(file)
    resolution <- diff(sort(unique(post$cal_BP)))[1]
    bottom <- max(p$data$y, na.rm = TRUE) - overlap
    for (i in seq_len(nrow(transitions))) {
        d <- subset(post, parameter == transitions$parameter[i])
        if (nrow(d) == 0) stop("no posterior for ", transitions$parameter[i])
        d$x <- -(d$cal_BP + bp_offset)
        d$base <- bottom + spacing * (i - 1)
        if (is.na(height)) {
            d$y <- d$base + d$density / resolution * scale
        } else {
            d$y <- d$base + d$density / max(d$density) * height
        }
        lx <- transitions$label_x[i]
        if (is.null(lx) || is.na(lx)) lx <- label.x
        p <- p +
            geom_ribbon(
                data = d, aes(x = x, ymin = base, ymax = y), inherit.aes = FALSE,
                fill = transitions$color[i], color = "#333333",
                linewidth = 0.2, alpha = 0.8
            ) +
            annotate("text", x = lx, y = d$base[1] + 0.8,
                     label = transitions$label[i], hjust = 0, color = "#333333")
    }
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
    "Kakataibo" = c("Kakataibo"),
    "Kaxarari" = c("Kaxarari"),
    "Northern" = c( "Matis", "Matses")
)

colors <- c(
    "Headwaters" = "#f8d56a",
    "Poyanawa" = "#e0a23f",
    "Marubo" = "#f1864e",
    "Ucayali" = "#d1803f",
    "Bolivian" = "#b08258",
    "Kakataibo" = "#4e964f",
    "Kaxarari" = "#3d7741",
    "Northern" = "#e000db"
)


trees <- treeio::read.beast("../beast/models/pano_covarion_relaxed.trees.gz")

# remove burn-in
trees.subsample <- trees[1701:2001]
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
        breaks = seq(-2500, 0, by = 500),
        limits = c(-2700.0, 1000.0)
    ) +
    theme_tree2() +
    scale_color_manual(values=colors) +
    guides(color="none", fill="none")


for (clade in names(clades)) {
    # hopefully the number of the mrca doesn't change or this won't work
    p <- add_clade(p, trees.subsample[[1]]@phylo, clade, clades[[clade]], colors[[clade]])
}


ages <- data.frame(Root=sapply(trees.subsample, get_rootheight))

p <- p + geom_density(
    data = ages, aes(-Root, y=after_stat(density) * 750), group = 1,
    inherit.aes = FALSE,
    color = "#333333",
    fill = "#666666",
    linewidth = 0.2,
    alpha = 0.5
)

p <- add_transitions(p, "posteriors_primary.csv", transitions)

p
ggsave('fig_densitree.pdf', p, width=9, height=10, dpi=500)
