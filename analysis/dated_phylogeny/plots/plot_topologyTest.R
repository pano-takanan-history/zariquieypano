# This code is based on the following article: 
# King, B., Greenhill, S. J., Reid, L. A., Ross, M., Walworth, M., & Gray, R.
# (2023, March 31). Bayesian phylogenetic analysis of Philippine languages
# supports a rapid migration of Malayo-Polynesian languages. 
# https://doi.org/10.31235/osf.io/re8m6

setwd(dirname(rstudioapi::getSourceEditorContext()$path))


library(devtools)
library(XML)

# load functions from github
source_url("https://raw.githubusercontent.com/king-ben/beast_asr/main/asr_functions.R")

tt <- topology_test("../beast/pano_covarion_relaxed.sites.log", #path to output topology hypothesis 1 
                    "../beast/pano_covarion_relaxed_constrained.sites.log", #path to output topology hypothesis 2 
                    "unconstrained",#label for plot topology 1
                    "constrained",#label for plot topology 2
                    burnin=0.2,#how much burnin to remove
                    hpd.level = 0.3,#which hpd distribution needs to be not overlapping to consider a cognate significant, lower numbers return more cognates
                    colors = c("#89a0bf","#87230d")
                    )

tt$plot
ggsave('fig_topologyTest.png', tt$plot, width=8, height=5)
