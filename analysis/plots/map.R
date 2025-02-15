# R version 4.3.1 (2023-06-16) -- "Beagle Scouts"
library(readr) # v2.1.4
library(dplyr) # v1.1.3
library(ggplot2) # v3.4.3
library(ggrepel) # v0.9.3
library(rnaturalearth) # v0.3.2
library(rnaturalearthdata) # v0.1.0
library(viridisLite) # v0.4.2
library(viridis) # v0.6.3

# Loading the data
lex <- read_csv('../../cldf/languages.csv') %>% 
  mutate(Subgroup = SubGroup)

# Downloading the map
spdf_sa <- ne_countries(continent=c("south america"),
                        scale="medium", 
                        returnclass="sf")

# Plotting the language points and labels on the map
map_lex <- ggplot(data=lex) +
  geom_sf(data = spdf_sa) +
  coord_sf(ylim=c(-16, 1), xlim= c(-81, -55)) +
  geom_point(aes(x=Longitude,y=Latitude, shape=Subgroup, fill=Subgroup), size=10) +
  # geom_label_repel(box.padding=0.75, point.padding=0.5,
  #                  data=lex, aes(Longitude, Latitude, label=Name),
  #                  min.segment.length=unit(0.1, 'lines'),
  #                  size=6, max.overlaps=99) +
  # geom_label_repel(aes(label=Name, x=Longitude,y=Latitude), data = lex[lex$Name %in% c("Shipibo-Konibo"),],
  #                  # max.overlaps=10, min.segment.length=unit(0, 'lines'), color="black",
  #                  # box.padding = unit(1.5, "lines"), size=6) +
  scale_shape_manual(values=c(21, 22, 23, 24)) +
  scale_fill_viridis_d(guide="legend", option="D") +
  #labs(caption = "Data: Glottolog") +
  theme_bw() +
  theme(legend.position="bottom",
        axis.title = element_text(size = rel(1.3)),
        axis.text = element_text(size = rel(1.3)),
        legend.text = element_text(size = rel(1.5)),
        legend.spacing.y = unit(0.5, 'cm'),
        legend.spacing.x = unit(0.2, 'cm'),
        legend.title = element_text(size = rel(0)))

map_lex
ggsave('fig_map.png', map_lex, units="px", width=5000, height=3000)
