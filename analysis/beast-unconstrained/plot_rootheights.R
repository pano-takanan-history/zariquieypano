#!/usr/bin/env Rscript
suppressPackageStartupMessages(require(readr, quietly=TRUE))
suppressPackageStartupMessages(require(ggplot2, quietly=TRUE))
suppressPackageStartupMessages(require(gghalves, quietly=TRUE))
suppressPackageStartupMessages(require(ggridges, quietly=TRUE))


ggplot2::theme_set(theme_classic(base_size=18))


results <- NULL
for (logfile in list.files('.', pattern="^[a-zA-Z0-9_]+\\.log$")) {
    results <- rbind(
        results,
        readr::read_delim(logfile, id="filename", comment="#", col_select=c('Sample', 'posterior', 'Tree.t:tree.height', 'Tree.t:tree.treeLength'))
    )
}

# remove 10% as burn-in
results <- results[results$Sample > max(results$Sample, na.rm=TRUE) / 10,]

results$Label <- gsub("^pano_", "", tools::file_path_sans_ext(results$filename))

o <- ggplot(results, aes(x=`Tree.t:tree.height`, y=Label, fill=Label, alpha=0.2)) +
    geom_density_ridges2(rel_min_height=0.001, scale=1.5) +
    guides(fill="none", alpha="none") +
    xlab('Root height (years)') +
    ylab(NULL) +
    xlim(0, 2500) +
    scale_fill_brewer(palette='Dark2')

ggsave('rootheights.pdf')
