# Compute the overlap beetween the transition of Pacacocha and the phylogeny
library(ggplot2)
library(dplyr)
library(treeio)
library(lachesis)
library(bayestestR)

# 95.4% 
pac <- subset(read.csv("posteriors_primary.csv"), parameter == "Start of post-Yarinacocha period")
pac <- pac[order(-pac$density), ]

# Print 95.45% HPDI
limits <- range(pac$cal_BP[cumsum(pac$density) - pac$density < 0.954])

# Read trees after burn-in
trees <- treeio::read.beast('../beast/models/pano_covarion_relaxed_p5.trees')
trees <- trees[1002:2001]

# trees[[1]]@data
est <- tibble(
  parameter="Phylogeny",
  cal_BP=sapply(trees, get_rootheight) - 50  # Convert to BP standard: 1950
)

df <- rbind(est[c('parameter', 'cal_BP')], pac[c('parameter', 'cal_BP')])

# Convert estimated (phylogenetic) data onto same grid.
# common 5-year grid spanning both
grid <- seq(min(c(pac$cal_BP, est$cal_BP)) - 100,
            max(c(pac$cal_BP, est$cal_BP)) + 100, by=5)

# KDE of phylogenetic samples on that grid
d <- density(est$cal_BP, from=min(grid), to=max(grid), n=length(grid))

est_d <- tibble(parameter="Phylogeny", cal_BP=d$x, density=d$y)

# normalise pac so both integrate to 1
pac_d <- pac |>
    select(parameter, cal_BP, density) |>
    mutate(density=density / sum(density * 5))

both <- bind_rows(pac_d, est_d)

ggplot(both, aes(cal_BP, density, fill=parameter)) +
    geom_area(alpha=0.4, position="identity", color="black", outline.type="both") +
    labs(x="cal BP", y="Density") +
    theme_classic() +
    scale_fill_manual(values=c("steelblue", "tomato"))

ggsave('fig_overlap.pdf', dpi=500)

p1 <- approx(pac_d$cal_BP, pac_d$density, xout=grid, yleft=0, yright=0)$y
p2 <- approx(est_d$cal_BP, est_d$density, xout=grid, yleft=0, yright=0)$y

ovl <- sum(pmin(p1, p2)) * 5    # 5=5 year grid
ovl

###############################
# Simpler approach with bayestestR
n <- 1e6

# Sample from density distribution
s_pac <- sample(pac_d$cal_BP, n, replace=TRUE, prob=pac_d$density)
s_pac <- s_pac + runif(n, -2.5, 2.5)   # jitter within the 5-yr bins

hdi(s_pac, prob=0.954)
mean(s_pac)

overlap(est$cal_BP, s_pac)

# Sample from the phylogeny posterior
s_phy <- sample(est_d$cal_BP, n, replace=TRUE, prob=est_d$density)
s_phy <- s_phy + runif(n, -2.5, 2.5)

hdi(s_phy, prob=0.954)
mean(s_phy)

( sum(s_phy > max(s_pac)) / length(s_phy) ) * 100

