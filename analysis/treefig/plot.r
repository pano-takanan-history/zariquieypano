library(ape)
library(treeio)
library(ggplot2)
library(ggtree)
library(dplyr)
library(tidyr)

ggplot2::theme_set(theme_classic(base_size=18))

tree <- treeio::read.beast('pano_covarion_relaxed.mcct.trees')

data <- read.delim("data.tsv", sep="\t", check.names=FALSE, header=TRUE, strip.white=TRUE, row.names=1, na.strings="?")
data2 <- read.delim("data2.tsv", sep="\t", check.names=FALSE, header=TRUE, strip.white=TRUE, row.names=1, na.strings="?")

# set up long data
data.long <- data %>%
    mutate(Language = rownames(.)) %>%
    pivot_longer(
        cols = !Language,
        names_to = "Variable",
        values_to = "State"
    ) %>%
    mutate(Subset="Phonology and Lexicon")
data.long2 <- data2 %>%
    mutate(Language = rownames(.)) %>%
    pivot_longer(
        cols = !Language,
        names_to = "Variable",
        values_to = "State"
    ) %>%
    mutate(Subset="Grammar")

data.long <- rbind(data.long, data.long2)

# Identify gains and losses from Proto-Panoan
data.long$Change <- NA
pp <- data.long %>% filter(Language=='Proto-Pano')
for (i in 1:nrow(data.long)) {
    if (data.long[i, 'Language'] == 'Proto-Pano') {
        if (is.na(data.long[i, 'State'])) {
            data.long[i, 'Change'] <- 'Absence'
        } else if (data.long[i, 'State'] == 1) {
            data.long[i, 'Change'] <- 'Retention'
        } else {
            data.long[i, 'Change'] <- 'Absence'
        }
    } else {
        # get pp state
        ppstate <- pp %>% filter(Variable==data.long[[i, 'Variable']]) %>% pull(State)
        states <- sprintf(
            "%s%s",
            ifelse(is.na(ppstate), 0, ppstate),
            ifelse(is.na(data.long[[i, 'State']]), 0, data.long[[i, 'State']])
        )

        if (states == "01") {
            data.long[i, 'Change'] <- 'Gain'
        } else if (states == "00") {
            data.long[i, 'Change'] <- 'Absence'
        } else if (states == "10") {
            data.long[i, 'Change'] <- 'Loss'
        } else if (states == "11") {
            data.long[i, 'Change'] <- 'Retention'
        } else {
            print(data.long[i, ])
            stop(paste("BAD STATE:", states))
        }

        if (data.long[i, 'Language'] == 'Kakataibo') {
            cat(c(states, ':', data.long[[i, 'Change']], '->', data.long[[i, 'Variable']]), "\n")
        }
    }

}

# fix level order so the colors stay the same
data.long$Change <- factor(data.long$Change, levels=c("Retention", "Absence", "Gain", "Loss"))




#data.long$Label <- factor(data.long$Label, levels=c(
#    "loss of proto kw",
#    "huniki > hono 'peccari'",
#
#    "matses 'human'",
#    "kueste 'stick'",
#    "abu 'sky'",
#
#    "final vowel drop in uxa 'sleep'",
#    "riru > riri 'might monkey'",
#    "kuka > kuku 'father in law'",
#    "wispa 'star'",
#    "jame > ime 'night'",
#
#    "kwe 'big'",
#
#    "wasin 'grass'",
#    "uinti 'heart'",
#    "bari 'sun'",
#    "ia 'louse'"
#))

data.long$Language <- factor(data.long$Language, levels=c(
    "Proto-Pano", "Kakataibo", "Matses", "Matis", "Kaxarari", "Yaminawa",
    "Sharanawa", "Amawaka", "ShipiboKonibo", "Kapanawa", "Chakobo",
    "Iskonawa", "Poyanawa", "KashinawaB", "Mastanawa"
))


p <- ggplot(data.long, aes(x=Language, y=Variable, color=factor(State))) +
    geom_point(size=11, shape=15, color="#333333") +
    geom_point(size=10, shape=15) +
    ylab(NULL) +
    xlab(NULL) +
    scale_x_discrete(position = "top") +
    facet_grid(Subset~., drop=TRUE, scales="free_y", space="free_y") +
    theme(
        legend.position="top",
        axis.text.x = element_text(angle = 60, vjust = 1, hjust=0)
    ) +
    scale_color_manual(values=c("aliceblue", "dodgerblue4"), na.value="white") +
    guides(color="none")

ggsave("dotplot.pdf", p)


p <- ggplot(data.long, aes(x=Language, y=Variable, color=Change)) +
    geom_point(size=9, shape=15, color="#333333") +
    geom_point(size=8, shape=15) +
    ylab(NULL) +
    xlab(NULL) +
    scale_x_discrete(position = "top") +
    facet_grid(Subset~., drop=TRUE, scales="free_y", space="free_y") +
    theme(
        legend.position="top",
        axis.text.x = element_text(angle = 60, vjust = 1, hjust=0)
    ) +
    scale_color_manual(values=c(
        "#26a69a", # Proto-Panoan
        "#f5f5f5", # Absence
        "#ffca28", # Gain
        "#42a5f5" # Loss
    ), na.value="white")


ggsave("dotplot-changes.pdf", p)





tips_to_remove <- tree@phylo$tip.label[tree@phylo$tip.label %in% unique(data.long$Language) == FALSE]
for (t in tips_to_remove) {
    cat(paste("REMOVING TIP WITH NO DATA: ", t, "\n"))
}

tree <- drop.tip(tree, tips_to_remove)
tree@data['rposterior'] <- sprintf("%0.2f", as.numeric(tree@data[['posterior']]))
tree@data['rposterior'][tree@data['rposterior'] == 'NA',] <- NA

#put this back to wide

data.wide <- data.long %>%
    select(Language, Variable, State) %>%
    mutate(State=factor(State)) %>%
    pivot_wider(names_from = Variable, values_from = State) %>%
    tibble::column_to_rownames(var="Language")



p1 <- ggtree(tree, size=1.2, layout='slanted') +
    geom_tiplab(align=TRUE, linesize=0, offset=1370, hjust=0, angle=90) +
    geom_label(
        aes(label=rposterior), label.size=0.3, na.rm=TRUE, size=2,
        nudge_x=-0.4, nudge_y=0
    ) +
    scale_x_continuous(limits = c(-1500, 1600)) +
    scale_y_continuous(limits = c(-10, 20)) +
    theme_tree() +
    coord_flip()

p1 <- revts(p1)

p1 <- gheatmap(
        p1,
        data.wide,
        width=1,
        hjust=1,
        offset=10,
        colnames=TRUE,
        font.size=5,
        colnames_position="bottom"
    ) +
    scale_fill_manual(values=c("#C6E2FF", "dodgerblue4"), na.value="#7A8B8B") +
    theme(legend.position="top")

ggsave('treefigure.png', p1, width=10, height=12)


data.wide <- data.long %>%
    select(Language, Variable, Change) %>%
    mutate(Change=factor(Change)) %>%
    pivot_wider(names_from = Variable, values_from = Change) %>%
    tibble::column_to_rownames(var="Language")

p1 <- ggtree(tree, size=1.2, layout='slanted') +
    geom_tiplab(align=TRUE, linesize=0, offset=1370, hjust=0, angle=90) +
    geom_label(
        aes(label=rposterior), label.size=0.3, na.rm=TRUE, size=2,
        nudge_x=-0.4, nudge_y=0
    ) +
    scale_x_continuous(limits = c(-1500, 1600)) +
    scale_y_continuous(limits = c(-10, 20)) +
    theme_tree() +
    coord_flip()

p1 <- revts(p1)

p1 <- gheatmap(
    p1,
    data.wide,
    width=1,
    hjust=1,
    offset=10,
    colnames=TRUE,
    font.size=5,
    colnames_position="bottom"
) +
    scale_fill_manual(values=c(
        "#26a69a", # Proto-Panoan
        "#f5f5f5", # Absence
        "#ffca28", # Gain
        "#42a5f5" # Loss
    ), na.value="white") +
    theme(legend.position="top")

ggsave('treefigure-changes.png', p1, width=10, height=12)

## QUESTION:
# - No Mastanawa data for Grammar ?
# - "kashinawa" is this B or P? or both?
#   have set it to KashinawaB for now
# - going to tree plot loses tips without data (n=12):
#    [1] "Arara"      "Chaninawa"  "Kanamari"   "KashinawaP" "Katukina"   "Marinawa"
     [7] "Marubo"     "Nawa"       "Nukini"     "Pakawara"   "Shanenawa"  "Yawanawa"
