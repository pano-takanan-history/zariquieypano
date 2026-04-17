library(ggplot2)

# ---- Data ----
# Archaeological phases
arch <- data.frame(
  phase = c("Yarinacocha", "Pacacocha", "Cumancaya", "Caimito"),
  xmin  = c(2200, 1800, 1300, 600),
  xmax  = c(1800, 1300, 600, 0),
  y     = c(2, 3, 4, 5)
)

# Diversification of Pano
pano <- data.frame(
  phase = c("Early origin", "Recent origin"),
  xmin  = c(3000, 1300),
  xmax  = c(2000, 800),
  y     = c(-2, -1)
)

# Combine
df <- rbind(arch, pano)

# ---- Plot ----
ggplot(df) +
  geom_rect(aes(xmin = xmin, xmax = xmax,
                ymin = y - 0.45, ymax = y + 0.45,
                fill = phase),
            color = "black", size = 1) +
  
  # Labels on y-axis
  scale_y_continuous(
    breaks = c(arch$y, pano$y),
    labels = c(arch$phase, pano$phase)
  ) +
  
  # Reverse x-axis (Years BP)
  scale_x_reverse(name = "Years BP", limits = c(3100, -50)) +
  
  # Colors (approximate to your figure)
  scale_fill_manual(values = c(
    "Yarinacocha" = "#6666B3",
    "Pacacocha"   = "#E06AB7",
    "Cumancaya"   = "#D9775F",
    "Caimito"     = "#5FA0D9",
    "Early origin"= "#7A9997",
    "Recent origin"="#A6D95A"
  )) +
  
  # Clean theme
  theme_classic(base_size = 16) +
  theme(
    legend.position = "none",
    axis.title.y = element_blank()
  ) +
  
  # Horizontal divider
  geom_hline(yintercept = 0.5, size = 1.5) +
  
  # Section labels
  annotate("rect", xmin = 3100, xmax = 2300, ymin = 5, ymax = 6,
           fill = "white", color = "black", linewidth = 1) +
  annotate("text", x = 2700, y = 5.5, label = "Archaeological phases", size = 6) +
  
  annotate("rect", xmin = 3100, xmax = 2300, ymin = -1, ymax = 0,
           fill = "white", color = "black", linewidth = 1) +
  annotate("text", x = 2700, y = -0.5, label = "Diversification of Pano", size = 6)

ggsave("schema.png", dpi = 500)
