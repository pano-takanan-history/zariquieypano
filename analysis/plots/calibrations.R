library(lachesis)
library(patchwork)
library(xml2)


# Matis and Matses as an independent branch at least by 1600
# - want start of distr at 400y, peak around 500y, and tail by 900 y
# - gives about 500 year window,
np <- beauti(distribution(calibration('Gamma(3, 200, 200)')), title='Northern Pano')

# Kakataibo as an independent language/branch by 1700
##??

# Shipibo and Kapanawa as different languages in the same branch by 1700
# - want start of distr at 300y, peak around 100y earlier, and tail by 700 y
cu <- beauti(distribution(calibration('Gamma(2, 120, 200)')), title='Central Ucayali')

# Chakobo and Pacahuara as closely related languages
# - want start of distr at 300y, peak around 100y earlier, and tail by 700 y
cp <- beauti(distribution(calibration('Gamma(2, 120, 200)')), title='Chacobo-Pacaguara')

ka <- beauti(distribution(calibration('Normal(80, 5)')), title="Kashinawa")

(np / cu / cp / ka) & xlim(0, 1750)

ggsave("~/Desktop/panoan-old.pdf", width=12, height=18)






# Matis and Matses as an independent branch at least by 1600
# - want start of distr at 400y, peak around 500y, and tail by 900y
# - gives about 500 year window,
cal <- calibration('lognormal(173, 0.7, 366, realspace=true)')
np <- beauti(distribution(cal), title=sprintf('Northern Pano: %s', format(cal)))

# Kakataibo as an independent language/branch by 1700
# - want start of distr at 300y, peak around 100y earlier, and tail by 700y + ORIGINATE
cal <- calibration('lognormal(163, 0.6, 258, realspace=true)')
kk <- beauti(distribution(cal), title=sprintf('Kakataibo: %s', format(cal)))

# Shipibo and Kapanawa as different languages in the same branch by 1700
# - want start of distr at 300y, peak around 100y earlier, and tail by 700y
cal <- calibration('lognormal(163, 0.6, 258, realspace=true)')
cu <- beauti(distribution(cal), title=sprintf('Central Ucayali: %s', format(cal)))

# Chakobo and Pacahuara as closely related languages
# - want start of distr at 300y, peak around 100y earlier, and tail by 700y
cal <- calibration('lognormal(163, 0.6, 258, realspace=true)')
cp <- beauti(distribution(cal), title=sprintf('Chacobo-Pacaguara: %s', format(cal)))

#
cal <- calibration('Normal(80, 5)')
ka <- beauti(distribution(cal), title=sprintf("Kashinawa: %s", format(cal)))

(np / cu / cp / ka / kk) & xlim(0, 1750)

ggsave("~/Desktop/panoan-new.pdf", width=12, height=18)
