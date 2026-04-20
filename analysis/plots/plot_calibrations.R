library(patchwork)
library(xml2)
library(ggthemes)

# Library that is work in progress
#remotes::install_github("SimonGreenhill/lachesis_src")
library(lachesis)

ticking <-c(0, 200, 400, 600, 800)

# Matis and Matses as an independent branch at least by 1600
# - want start of distr at 400y, peak around 500y, and tail by 900y
# - gives about 500 year window,
cal <- calibration('lognormal(173, 0.7, 366, realspace=true)')
np <- beauti(distribution(cal), title=sprintf('Northern Pano: %s', format(cal))) +
  coord_cartesian(xlim=c(250, 800)) +  
  scale_x_continuous(breaks=ticking, labels=ticking) +
  scale_y_continuous(breaks = c(0.00, 0.005), labels = c(0.000, 0.005)) +
  theme_grey(base_size=20) +
  theme(
    axis.text = element_text(size = 22),
    axis.title = element_text(size = 24)
  )

# Shipibo and Kapanawa as different languages in the same branch by 1700
# - want start of distr at 300y, peak around 100y earlier, and tail by 700y
cal <- calibration('lognormal(163, 0.6, 258, realspace=true)')
cu <- beauti(distribution(cal), title=sprintf('Central Ucayali: %s', format(cal))) +
  coord_cartesian(xlim=c(250, 800)) +
  scale_x_continuous(breaks=ticking, labels=ticking) +
  scale_y_continuous(breaks = c(0.00, 0.005), labels = c(0.000, 0.005)) +
  theme_grey(base_size=20) +
  theme(
    axis.text = element_text(size = 22),
    axis.title = element_text(size = 24)
  )

# Chakobo and Pacahuara as closely related languages
# - want start of distr at 300y, peak around 100y earlier, and tail by 700y
#cal <- calibration('lognormal(163, 0.6, 258, realspace=true)')
cp <- beauti(distribution(cal), title=sprintf('Chacobo-Pacaguara: %s', format(cal))) +
  coord_cartesian(xlim=c(250, 800)) +
  scale_x_continuous(breaks=ticking, labels=ticking) +
  scale_y_continuous(breaks = c(0.00, 0.005), labels = c(0.000, 0.005)) +
  theme_grey(base_size=20) +
  theme(
    axis.text = element_text(size = 22),
    axis.title = element_text(size = 24)
  )


#
cal <- calibration('Normal(80, 5)')
ka <- beauti(distribution(cal), title=sprintf("Kashinawa: %s", format(cal))) +
  scale_y_continuous(breaks = c(0.00, 0.05, 0.1), labels = c(0.000, 0.05, 0.1)) +
  theme_grey(base_size=20) +
  theme(
    axis.text = element_text(size = 22),
    axis.title = element_text(size = 24)
  )


(np / cu / cp / ka)
ggsave("fig_calibrations.pdf", width=12, height=12, dpi=500)
