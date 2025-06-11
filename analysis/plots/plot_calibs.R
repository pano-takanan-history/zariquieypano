library(dplyr)
library(ggplot2)
library(ggdist)
library(patchwork)

n <- 1e5

kashinawa <- rnorm(n, mean=80, sd=5) %>% 
  tibble() %>% 
  mutate(group = 'Kashinawa%~% normal(80, 5)') %>% 
  ggplot(aes(x=.)) + 
  geom_density(aes(alpha=0.7, fill='#0c71ff')) +
  scale_y_continuous(breaks = NULL, name = "Density of values") +
  scale_x_continuous(name='Years BP') +
  theme(legend.position = "none", plot.title = element_text(size = 14)) +  
  labs(title = "Kashinawa ~ normal(80, 5)")

# Given values
mean_real <- 163
sdlog <- 0.6
offset <- 258

# Calculate meanlog
meanlog <- log(mean_real) - (sdlog^2) / 2

# Simulate
data <- rlnorm(n, meanlog = meanlog, sdlog = sdlog) + offset 

bolivian <- data %>% 
  tibble() %>% 
  mutate(group = 'Chakobo and Pacahuara: logn(163, 0.6) + 258') %>% 
  ggplot(aes(x=.)) + 
  geom_density(aes(alpha=0.7, fill='#0c71ff')) +
  scale_y_continuous(breaks = NULL, name = "Density of values") +
  scale_x_continuous(name='Years BP') +
  theme(legend.position = "none", plot.title = element_text(size = 14)) +  
  labs(title = "Chakobo + Pacahuara: logn(163, 0.6) + 258")


all_priors <- (kashinawa + bolivian)
ggsave("calibration_examples.png", all_priors, scale=1, width=3000, height=1200, units='px')
