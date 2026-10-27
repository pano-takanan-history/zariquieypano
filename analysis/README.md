# Notes for workflow

## Oxcal code

The folder `oxcal_code` contains the OxCal models used in the paper: the Ucayali ceramic sequence alone (ucayali_) and the full corpus with Shahuaya and Granja de Sivia added as separate unordered groups (full_). Each has two versions that differ by the prior on the scale of the Charcoal outlier model. That model allows wood charcoal dates to be older than the event they date by an exponentially distributed old-wood offset, whose scale is 10^U(0,2) (1-100 years) in the _U02 models, and 10^U(0,3) (1-1000 years) in the _U03 versions.

## Topology test

`git clone https://github.com/king-ben/beast_asr`

Nexus file:

```nexus
begin assumptions;
charset all = 1-1042
END;
```

Check that tree likelihood has the same name!

```xml
<logger id="Sitelikelihoods" fileName="site_likelihoods.txt" logEvery="10000" mode="tree">
  <log id="sitelik.all" spec="babel.util.SiteLikelihoodLogger" likelihood="@treeLikelihood.all" value="_ascertainment I all all ..."/>
</logger>
```
