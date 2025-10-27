# This plot is based on a script that was provided along the 
# Sagart et al. (2019) analysis of Sino-Tibetan for their plots:
# Sagart, L., Jacques, G., Lai, Y., Ryder, R. J., Thouzeau, V., Greenhill, S. J., 
# & List, J. M. (2019). Dated language phylogenies shed light on the ancestry of 
# Sino-Tibetan. Proceedings of the National Academy of Sciences, 116(21), 
# 10317-10322. https://doi.org/10.1073/pnas.1817972116

library('ggplot2')
library('ggtree')
library('treeio')
library('RColorBrewer')
library('dplyr')
library('readr')

# Tree
tree <- read.beast('../beast/pano_covarion_relaxed_words.MCC.tree')
langs <- read_csv('../../cldf/languages.csv') %>%
  select(ID) %>% arrange(ID) %>% as.vector()

tree@data['rposterior'] <- sprintf('%0.2f', as.numeric(tree@data[['posterior']]))
tree@data['rposterior'][tree@data['rposterior'] == 'NA',] <- NA


cls <- list(
  'Northern' = c('Matses', 'Matis'),
  'Kaxarari' = c('Kaxarari'),
  'Kakataibo' = c('Kakataibo'),
  'Bolivian' = c('Chakobo', 'Pakawara'),
  'Ucayali' = c('ShipiboKonibo', 'Kapanawa'),
  'Marubo' = c('Marubo', 'Katukina', 'Kanamari'),
  'Poyanawa' = c('Iskonawa', 'Poyanawa', 'Nukini'),
  'Headwaters' = c('Amawaka', 'Arara', 'Chaninawa', 'KashinawaB',
                   'KashinawaP', 'Marinawa', 'Mastanawa', 'Nawa', 'Shanenawa',
                   'Sharanawa', 'Yaminawa', 'Yawanawa')
  )

tree <- groupOTU(tree, cls, overlap='origin', connect=FALSE)

print(levels(attr(tree@phylo, 'group')))

colors <- c(
  '#333333', # 0  - i.e. non colored branches.
  "#a8c9df", # Bolivian
  "#1a3268", # Headwaters
  "#87c27e", # Kakataibo
  "#3d7741", # Kaxarari
  "#3a6fb0", # Marubo
  "#d55f2b", # Northern
  "#4069a6", # Poyanawa
  "#5790c1"  # Ucayali
)


p <- ggtree(tree, aes(color=group), ladderize=TRUE, size=3) %>% 
  revts() + 
  geom_tiplab(align=TRUE, size=9) +
  geom_label(
    aes(label=rposterior), 
    na.rm=TRUE, nudge_x=-20, nudge_y=0, size=9
  ) +
  theme_tree2(axis.text.x = element_text(size=20) ) +
  scale_color_manual(values=colors) +
  scale_x_continuous(breaks = c(-1500, -1000, -500, 0), limits=c(-1500, 450)) + 
  theme(legend.position='none')

col_idx = 2
for (clade in levels(attr(tree@phylo, 'group'))) {
  if (is.null(cls[[clade]])) next
  m <- MRCA(tree, cls[[clade]])
  if (!is.null(m)) {
    cat(paste(clade, m, col_idx, colors[col_idx]), '\n')
    p <- p + geom_cladelabel(
      node=m, label=clade, color = colors[col_idx],
      extend=0.45, # extending the bars up/down
      
      offset=300,  # bars from node?
      offset.text=15, # offset of text from labels
      
      # General
      barsize=2.5,
      fontsize=9
    )
  }
  col_idx <- col_idx + 1
}
p

ggsave('fig_tree.pdf', p, width=20, height=20, dpi=500)
