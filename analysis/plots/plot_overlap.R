#!/usr/bin/env Rscript

library(ggplot2)
library(dplyr)
library(treeio)
library(lachesis)

# How small is "a small part of the posterior" “A “small part of the posterior”
# fits with “a split prior to the development of Pacacocha”.
# Can you please quantify “small”? Perhaps I'm not reading Fig3 correctly here,
# but it looks to me as if about half the HPDI precedes the actual evidence for
# Pacacocha, starting around 1400BP."


pac <- readr::read_csv('posterior_start_pacacocha.csv', show_col_types=FALSE)
pac$parameter <- 'Pacachocha'

trees <- treeio::read.beast('../beast/models/pano_covarion_relaxed_p5.trees')
# remove burnin
trees <- trees[1002:2001]

# Pacacocha is root
trees[[1]]@data


est <- as.data.frame(sapply(trees, get_rootheight, simplify=TRUE, USE.NAMES=FALSE))
rownames(est) <- NULL
colnames(est) <- c("age")

est$cal_BP <- est$age - 50  # convert to BP standard (1950)
est$parameter <- 'Phylogeny'

df <- rbind(est[c('parameter', 'cal_BP')], pac[c('parameter', 'cal_BP')])

ggplot(df, aes(x=cal_BP, group=parameter, fill=parameter)) + geom_density(alpha=0.7) +
    theme_classic() + scale_fill_manual(values=c("steelblue", "tomato"))


# Convert estimated (phylogenetic) data onto same grid.
# common 5-year grid spanning both
grid <- seq(min(c(pac$cal_BP, est$cal_BP)) - 100,
            max(c(pac$cal_BP, est$cal_BP)) + 100, by = 5)

# KDE of phylogenetic samples on that grid
d <- density(est$cal_BP, from = min(grid), to = max(grid), n = length(grid))
est_d <- tibble(parameter = "Phylogeny", cal_BP = d$x, density = d$y)

# normalise pac so both integrate to 1
pac_d <- pac |>
    select(parameter, cal_BP, density) |>
    mutate(density = density / sum(density * 5))

both <- bind_rows(pac_d, est_d)

ggplot(both, aes(cal_BP, density, fill = parameter)) +
    geom_area(alpha = 0.5, position = "identity") +
    labs(x = "cal BP", y = "Density") +
    theme_classic() +
    scale_fill_manual(values=c("steelblue", "tomato"))
ggsave('fig_overlap.pdf', dpi=500)

p1 <- approx(pac_d$cal_BP, pac_d$density, xout = grid, yleft = 0, yright = 0)$y
p2 <- approx(est_d$cal_BP, est_d$density, xout = grid, yleft = 0, yright = 0)$y

ovl <- sum(pmin(p1, p2)) * 5    # 5 = 5 year grid

###############################
# try another approach with bayestestR
library(bayestestR)

n <- 1e5
s_pac <- sample(pac_d$cal_BP, n, replace=TRUE, prob=pac_d$density)
s_pac <- s_pac + runif(n, -2.5, 2.5)   # jitter within the 5-yr bins

overlap(est$cal_BP, s_pac)
