# Notes for workflow

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
