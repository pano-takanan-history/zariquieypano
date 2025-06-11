# R version 4.3.1 (2023-06-16) -- "Beagle Scouts"
library(readr) # v2.1.4
library(dplyr) # v1.1.3
library(ggplot2) # v3.4.3
library(ggrepel) # v0.9.3
library(rnaturalearth) # v0.3.2
library(rnaturalearthdata) # v0.1.0
library(viridisLite) # v0.4.2
library(viridis) # v0.6.3
library(ggbeeswarm)

# Loading the data
lex <- read_csv('../../cldf/languages.csv') %>% mutate(ID=as.character(1:nrow(.)))
sites <- read_csv('archaeological_sites.csv') %>% arrange(Tradition)
colors <- c("#1f77b4", "#ff7f0e", "#2ca02c")


# Downloading the map
spdf_sa <- ne_countries(continent=c("south america"), scale="medium", returnclass="sf")
rivers <- ne_download(scale=50, type='rivers_lake_centerlines', category='physical', returnclass="sf")

colors_sc <- c('#0c71ff', '#ca2800', '#ff28ba', '#86e300')

langs <- c('Kakataibo', 'Kaxarari', 'Matses', 'Yaminawa', 'Chakobo', 'Shipibo-Konibo')
labels <- lex %>% filter(Name %in% langs)
subgroups <- unique(lex$SubGroup)

# Plotting the language points and labels on the map
map_lex <- ggplot(data=lex) +
  geom_sf(data=spdf_sa) +
  geom_sf(data=rivers) +
  coord_sf(ylim=c(-16, 1), xlim= c(-81, -55)) +
  geom_point(aes(x=Longitude,y=Latitude, shape=SubGroup, fill=SubGroup), size=10) +
  geom_label_repel(data=labels, aes(label=Name, x=Longitude,y=Latitude), color="black",
                   box.padding=unit(0.9, "lines"), size=6) +
  scale_shape_manual(values=c(21, 22, 23, 24)) +
  scale_fill_manual(values=colors_sc) +
  theme_bw() +
  theme(legend.position="bottom",
        axis.title=element_text(size=rel(1.3)),
        axis.text=element_text(size=rel(1.3)),
        legend.text=element_text(size=rel(1.5)),
        legend.spacing.y=unit(0.5, 'cm'),
        legend.spacing.x=unit(0.2, 'cm'),
        legend.title=element_text(size=rel(0)))

map_lex
ggsave('fig_lex.pdf', map_lex, dpi=300)



map_sites <- ggplot(data=sites) +
  geom_sf(data=spdf_sa) +
  geom_sf(data=rivers) +
  coord_sf(ylim=c(-11, -7), xlim= c(-77, -70)) +
  # Archaeological sites
  geom_jitter(aes(x=Longitude, y=Latitude, shape=Tradition, fill=Tradition), 
             size=12, alpha=0.8, width=0.3, height=0.3) +  # Adjust size and alpha for better visualization
  scale_shape_manual(values=c(21, 22, 23, 24, 25, 26, 27, 28)) +  # Shapes for archaeological traditions
  scale_fill_manual(values=c(colors[2], colors[3], colors[1])) +  # Colors for traditions
  theme_bw() +
  theme(legend.position="bottom",
        axis.title=element_text(size=rel(1.3)),
        axis.text=element_text(size=rel(1.3)),
        legend.text=element_text(size=rel(1.5)),
        legend.spacing.y=unit(0.5, 'cm'),
        legend.spacing.x=unit(0.2, 'cm'),
        legend.title=element_text(size=rel(0)))

map_sites
ggsave('fig_sites.pdf', map_sites, dpi=500, width=14, height=8)

##############################################
# Sites
combined_data <- sites %>%
  group_by(Tradition) %>%
  summarise(
    Oldest_C14Age=max(C14Age),  # Use the oldest C14Age for each Tradition
    Min_C14Age=min(C14Age),     # Minimum C14Age for the interval
    Max_C14Age=max(C14Age),     # Maximum C14Age for the interval
    Mean_SD=mean(SD),           # Mean SD (standard deviation)
    .groups='drop'
  ) %>%
  mutate(
    SD_Interval=2 * Mean_SD,     # 2 * SD for the interval (widest range)
    Min_Interval=Min_C14Age - SD_Interval,  # Lower bound of the interval
    Max_Interval=Max_C14Age + SD_Interval,  # Upper bound of the interval
    C14Age_lower=Oldest_C14Age - Mean_SD,  # Lower bound of the C14 range (Oldest C14 - 1*SD)
    C14Age_upper=Oldest_C14Age + Mean_SD  # Upper bound of the C14 range (Oldest C14 + 1*SD)
  )

# Colors for the plot

timeline <- ggplot(combined_data, aes(x=Oldest_C14Age, y=Tradition)) +
  geom_rect(aes(xmin=C14Age_lower, xmax=C14Age_upper, ymin=as.numeric(factor(Tradition)) - 0.3, 
                ymax=as.numeric(factor(Tradition)) + 0.3, fill=Tradition), 
            color="black", alpha=0.6) +  # Box with black border and transparent fill
  geom_errorbarh(aes(xmin=Min_Interval, xmax=Max_Interval), height=0.5) +  # Add the error bars (widest interval)
  scale_x_reverse() +  # Reverse the X-axis
  scale_color_manual(values=colors) +  # Apply the pastel colors
  labs(
    x="C14 Age (Years BP)",
    y="",
  ) +
  theme_grey() +  # Use a clean theme
  theme(
    legend.position="none",  # Remove the legend if it's not needed
    axis.text.y=element_blank(),  # Increase axis text size
    axis.text.x=element_text(size=20),  # Increase axis text size
    axis.title=element_text(size=22),  # Increase axis title size
    axis.ticks=element_blank()  # Make axis ticks thicker
  )

timeline
ggsave('fig_timeline.pdf', timeline, dpi=300)
