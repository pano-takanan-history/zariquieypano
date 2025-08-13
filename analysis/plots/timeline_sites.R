# R version 4.3.1 (2023-06-16) -- "Beagle Scouts"
library(readr) # v2.1.4
library(dplyr) # v1.1.3
library(ggplot2) # v3.4.3
library(ggrepel) # v0.9.3
library(rnaturalearth) # v0.3.2
library(rnaturalearthdata) # v0.1.0
library(ggbeeswarm)

# Loading the data
sites <- read_csv('archaeological_sites.csv') %>% arrange(Tradition)
colors <- c('#A1CAF1', '#2ca02c', '#ff7f0e')

##############################################
# Sites
combined_data <- sites %>%
  arrange('Oldest_C14Age') %>% 
  group_by(Tradition) %>%
  summarise(
    Oldest_C14Age=max(C14Age),  # Use the oldest C14Age for each Tradition
    Min_C14Age=min(C14Age),     # Minimum C14Age for the interval
    Max_C14Age=max(C14Age),     # Maximum C14Age for the interval
    Mean_SD=mean(SD),           # Mean SD (standard deviation)
    .groups='drop'
  ) %>%
  mutate(
    SD_Interval=1 * Mean_SD,     # 2 * SD for the interval (widest range)
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
  scale_fill_manual(values=colors) + # Apply the pastel colors
  labs(
    x="C14 Age (Years BP)",
    y="",
  ) +
  theme_grey() +  # Use a clean theme
  theme(
    legend.position="none",  # Remove the legend if it's not needed
    #axis.text.y=element_blank(),  # Increase axis text size
    axis.text.x=element_text(size=20),  # Increase axis text size
    axis.title=element_text(size=22),  # Increase axis title size
    axis.ticks=element_blank()  # Make axis ticks thicker
  )

timeline
ggsave('fig_timeline.pdf', timeline, dpi=300)
