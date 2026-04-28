library(ggplot2)
library(dplyr)

# Archaeological traditions
arch <- tibble(
  phase=c("Yarinacocha", "Pacacocha", "Cumancaya", "Caimito"),
  xmin =c(2200, 1800, 1300, 600),
  xmax =c(1800, 1300, 600, 0),
  y    =c(2, 3, 4, 5)
)

# Diversification of Pano
pano <- tibble(
  phase=c("Early origin", "Recent origin"),
  xmin =c(3000, 1300),
  xmax =c(2000, 800),
  y    =c(-2, -1)
)

df <- rbind(arch, pano)

# Plot
ggplot(df) +
  geom_rect(aes(xmin=xmin, xmax=xmax,
                ymin=y - 0.45, ymax=y + 0.45,
                fill=phase),
            color="black", linewidth=1) +
  
  # Labels on y-axis
  scale_y_continuous(
    breaks=c(arch$y, pano$y),
    labels=c(arch$phase, pano$phase)
  ) +
  
  # Reverse x-axis (Years BP)
  scale_x_reverse(name="Years BP", limits=c(3250, -50)) +
  
  # Colors (approximate to your figure)
  scale_fill_manual(values=c(
    "Yarinacocha"="#b4b4b4",
    "Pacacocha"  ="#fa73bf",
    "Cumancaya"  ="#a1e573",
    "Caimito"    ="#ffa300",
    "Early origin"= "#7A9997",
    "Recent origin"="#B6D95F"
  )) +
  
  # Clean theme
  theme_classic(base_size=20) +
  theme(
    legend.position="none",
    axis.title.y=element_blank()
  ) +
  
  # Horizontal divider
  geom_hline(yintercept=0.5, linewidth=1.5) +
  
  # Section labels
  annotate("rect", xmin=3250, xmax=2150, ymin=5, ymax=6,
           fill="white", color="black", linewidth=1) +
  annotate("text", x=2700, y=5.5, label="Archaeological phases", size=6) +
  
  annotate("rect", xmin=3250, xmax=2150, ymin=-1, ymax=0,
           fill="white", color="black", linewidth=1) +
  annotate("text", x=2700, y=-0.5, label="Diversification of Pano", size=6)

ggsave("fig_schema.pdf", dpi=500)
