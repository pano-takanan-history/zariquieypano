#!/usr/bin/env python
import os
import re
import sys
import unittest
import subprocess
import xml.etree.ElementTree as ElementTree
from collections import Counter

VERSION = '2024-04-02'


#---------------------------------------------------------------------------#
# base

class IncorrectlyConfigured(Exception):
    pass



class BeastTest(object):
    """Tests a BEAST Analysis"""
    filename = None         # XML Filename
    xml = None              # XML content
    ntaxa = 0               # Number of Taxa
    nchar = 0               # Number of Characters
    ngenerations = 0        # Number of Generations/chainLength
    logEvery = 0            # Log every N generations
    
    # override these if you have specific log file naming
    # that doesn't match filename{.trees,.log}
    tracelog = None
    treelog = None
    
    # validate XML using beast2? 
    validate = False        # do not by default
    beast2 = 'beast2'       # path to beast2
    
    others = {}
    
    @classmethod
    def setUpClass(cls):
        cls.xml = ElementTree.parse(cls.filename)
        
    # helpers
    def get_matching_children(self, entity, pattern, key='id'):
        """
        Searches through children of `entity` returning any that
        have a `key` (default=id) matching the regex in `pattern`.
        """
        pattern = re.compile(pattern)
        # remove entities that don't have this `key` first or we'll try to
        # match pattern on None.
        entities = [e for e in entity if e.get(key) is not None]
        # now match things to pattern
        entities = [e for e in entities if pattern.match(e.get(key))]
        if len(entities) == 0:
            raise IndexError('Unable to find entity match')
        return entities
    
    def _is_in(self, elements, pattern, key='idref'):
        rpattern = re.compile(pattern)
        children = [el.get(key) for el in elements if el.get(key) is not None]
        if len([child for child in children if rpattern.match(child)]):
            return True
        else:
            raise AssertionError("Can't find %s=%s" % (key, pattern))
         
    def is_in_tracelog(self, pattern, key='idref'):
        """Tests that `pattern` is in the tracelog"""
        #tracelog = self.xml.find('run/logger[@id="tracelog"]').getchildren()
        tracelog = self.xml.find('run/logger[@id="tracelog"]')
        return self._is_in(tracelog, pattern, key)
    
    def is_in_operators(self, pattern, key="id"):
        operators = self.xml.findall('.//operator')
        return self._is_in(operators, pattern, key)
    
    def is_in_state(self, pattern, key="id"):
        """Tests that `key`=`pattern` is in the state"""
        state = self.xml.find('./run/state')
        return self._is_in(state, pattern, key)
           
    def is_in_prior(self, pattern, key="id"):
        """Tests that `key`=`pattern` is in the state"""
        prior = self.xml.find('./run/distribution/distribution/[@id="prior"]')
        return self._is_in(prior, pattern, key)
    
    # generic tests
    def test_configuration(self):
        """Tests that the BeastTest test case is set up correctly"""
        if not os.path.isfile(self.filename):
            raise IncorrectlyConfigured("Filename does not exist")
        
        try:
            int(self.ntaxa)
        except ValueError:
            raise IncorrectlyConfigured("ntaxa should be an integer")
        
        try:
            int(self.nchar)
        except ValueError:
            raise IncorrectlyConfigured("nchar should be an integer")
        
        try:
            int(self.ngenerations)
        except ValueError:
            raise IncorrectlyConfigured("ngenerations should be an integer")

        try:
            int(self.logEvery)
        except ValueError:
            raise IncorrectlyConfigured("logEvery should be an integer")
    
    def test_for_improper_priors(self):
        for prior in self.xml.find('./run/distribution/distribution/[@id="prior"]'):
            for p in prior:
                for a in p.attrib:
                    assert p.attrib[a] not in ('Infinity', 'Inf', '-Inf', 'nan', 'NaN'), \
                    "%s/%s/%s is improper" % (prior.attrib.get('id', '?'), p.tag, a)
    
    def test_others(self):
        for key in sorted(self.others):
            log = self.xml.find('.//*[@id="%s"]' % key)
            assert log is not None, "Cannot find %s" % key
            for attr, expected in self.others[key].items():
                if attr == "_value":
                    assert log.findtext('.') == expected, "%s/%s is not %s" % (
                        key, attr, expected
                    ) 
                else:
                    assert log.get(attr) == expected, "%s/%s is not %s" % (
                        key, attr, expected
                    ) 
    
    def test_ntaxa(self):
        """Tests the number of taxa"""
        taxa = len(self.xml.findall('./data/sequence'))
        if taxa != self.ntaxa:
            e = "Taxa count incorrect (%d != %d)" % (len(taxa), self.ntaxa)
            raise AssertionError(e)
        
    def test_nchar(self):
        """Tests the number of characters"""
        for seq in self.xml.findall('./data/sequence'):
            if len(seq.get('value')) != self.nchar:
                e = "Character Count on %s is not %d" % (
                    seq.get('id'), self.nchar
                )
                raise AssertionError(e)
    
    def test_ngenerations(self):
        """Tests the number of MCMC Generations/ChainLength"""
        gens = int(self.xml.find('run').get('chainLength'))
        if gens != self.ngenerations:
            raise AssertionError("Number of Generations is incorrect")
    
    def test_treelog(self):
        """
        Tests the tree log is named correctly:
            i.e. if filename = x.xml, then x.trees
        """
        if self.treelog is not None:
            expected = self.treelog
        else:
            expected = "%s.trees" % os.path.splitext(self.filename)[0]
        
        treelogs = self.xml.findall('run/logger')
        if expected not in [f.get('fileName') for f in treelogs]:
            raise AssertionError("Expected Tree log to be %s" % expected)

    def test_tracelog(self):
        """
        Tests the trace log is named correctly:
            i.e. if filename = x.xml, then x.log
        """
        if self.tracelog is not None:
            expected = self.tracelog
        else:
            expected = "%s.log" % os.path.splitext(self.filename)[0]
        
        log = self.xml.find('run/logger[@id="tracelog"]')
        
        if log is None:
            raise AssertionError("No tracelog defined")
        if log.get('fileName') != expected:
            raise AssertionError("Expected Trace log to be %s" % expected)
    
    def test_logEvery_tracelog(self):
        log = self.xml.find('run/logger[@id="tracelog"]')
        if int(log.get('logEvery')) != self.logEvery:
            raise AssertionError(
                "Tracelog is not logging every %d" % self.logEvery
            )

    def test_logEvery_treelog(self):
        loggers = self.xml.findall('run/logger')
        loggers = [l for l in loggers if l.get('mode') == 'tree']
        for log in loggers:
            if int(log.get('logEvery')) != self.logEvery:
                raise AssertionError(
                    "Treelog is not logging every %d" % self.logEvery
                )
    
    def test_for_duplicate_ids(self):
        idlist = Counter([x.get('id') for x in self.xml.iter() if x.get('id')])
        duplicates = [i for i in idlist if idlist[i] > 1]
        if len(duplicates):
            raise ValueError("Duplicate IDs in XML: %r" % duplicates)
    
    # helper for testing calibrations
    def check_calibration(self, clade, members, log=True, monophyletic=True):
        
        if log:  # check logging
            self.is_in_tracelog(clade)
        
        # check in prior
        prior = self.xml.find('./run/distribution/distribution/[@id="prior"]')
        try:
            cal = self.get_matching_children(prior, clade)[0]
        except IndexError:
            raise IndexError("Unable to find %s in prior" % clade)
        
        # check monophyletic
        if monophyletic:
            assert cal.get('monophyletic') == 'true'
        else:
            assert cal.get('monophyletic') in ('false', None)
        
        taxa = []
        for t in cal[0].findall('.//taxon'):
            if t.get('id'):
                taxa.append(t.get('id'))
            else:
                taxa.append(t.get('idref'))
        self.assertEqual(sorted(members), sorted(taxa))
    
    def test_xml(self):
        if not self.validate:
            return
            
        try:
            with open(os.devnull, 'w') as null:
                rv = subprocess.check_call(
                    [self.beast2, '-validate', self.filename],
                    stdout=null, stderr=subprocess.STDOUT
                )
        except subprocess.CalledProcessError:
            raise ValueError("beast couldn't validate the XML")
    

#---------------------------------------------------------------------------#
# Models
class ModelCTMC(object):
    """Tests CTMC Analyses"""
    def test_userdatatype_ctmc(self):
        """Test CTMC userDataType"""
        udt = self.xml.find('./data/userDataType')
        assert udt.get('spec') == "beast.base.evolution.datatype.StandardData"
        assert udt.get('ambiguities') == ""
        assert int(udt.get('nrOfStates')) == 2
    
    def test_userdatatype_in_treelikelihood_ctmc(self):
        udt = self.xml.find('.//distribution[@id="likelihood"]/distribution/data/userDataType')
        assert udt.get('spec') == "beast.base.evolution.datatype.Binary"
    
    def test_siteModel_is_GeneralSubstitutionModel(self):
        """
        siteModel should have a substModel of class GeneralSubstitutionModel
        """
        substModel = self.xml.find('.//substModel')
        if substModel is None:
            raise IndexError("substModel not found")
        assert substModel.get('spec') == 'GeneralSubstitutionModel'
    
    def test_substModel_rates(self):
        """substModel should have a rates parameter"""
        substModel = self.xml.find('.//substModel')
        rates = self.get_matching_children(substModel, r"rates\.s:.*")
        assert len(rates) == 1, "Unable to find rates parameter"
        assert int(rates[0].get('dimension')) == 2
    
    def test_substModel_frequency(self):
        """
        Tests that substModel has a frequencies parameter
        """
        substModel = self.xml.find('.//substModel')
        freqs = self.get_matching_children(
            substModel, "Frequencies", key="spec"
        )
        assert len(freqs) == 1, 'Unable to Find Frequencies Parameter'
    
    def test_frequencies_estimated(self):
        """Frequencies are estimated"""
        # fragile?
        assert self.is_in_operators(r"frequenciesDelta\.s:.*")
        

class ModelCovarion(object):
    """Tests Covarion Analyses"""
    def test_state_bcov_alpha(self):
        """bcov_alpha should be in the state"""
        assert self.is_in_state(r'bcov_alpha\.s:.*')
    
    def test_state_bcov_s(self):
        """bcov_s should be in the state"""
        assert self.is_in_state(r'bcov_s\.s:.*')
    
    def test_substModel(self):
        substModel = self.xml.find('.//substModel')
        if substModel is None:
            raise IndexError("substModel not found")
        assert substModel.get('spec') == 'BinaryCovarion'
        assert substModel.get('alpha').startswith('@bcov_alpha.s')
        assert substModel.get('vfrequencies').startswith('@frequencies.s')
        assert substModel.get('switchRate').startswith('@bcov_s.s')
    
    def test_userdatatype_in_treelikelihood_covarion(self):
        udt = self.xml.find('.//distribution[@id="likelihood"]/distribution/data/userDataType')
        assert udt.get('spec') == "beast.base.evolution.datatype.TwoStateCovarion"
    
    def test_useAmbiguities_is_true(self):
        """Covarion needs ambiguity in the likelihood"""
        lh = self.xml.find('.//distribution[@id="likelihood"]')
        treelh = self.get_matching_children(lh, r'treeLikelihood\..*')
        if treelh[0].get('useAmbiguities') != 'true':
            raise AssertionError('Covarion needs ambiguity')
    
    def test_prior_bcov_alpha(self):
        assert self.is_in_prior(r'bcov_alpha_prior\.s:.*')
    
    def test_prior_bcov_s(self):
        assert self.is_in_prior(r'bcov_s_prior\.s:.*')
    
    def test_frequencies_estimated(self):
        """Frequencies are estimated"""
        # fragile?
        assert self.is_in_operators(r"frequenciesDelta\.s:.*")
    
    def test_operator_bcovAlphaScaler(self):
        assert self.is_in_operators(r"bcovAlphaScaler\.s:.*")
    
    def test_operator_bcovSwitchParamScaler(self):
        assert self.is_in_operators(r"bcovSwitchParamScaler\.s:.*")
    
    def test_tracelog_bcov_alpha(self):
        assert self.is_in_tracelog(r'bcov_alpha\.s:.*')
    
    def test_tracelog_bcov_s(self):
        assert self.is_in_tracelog(r'bcov_s\.s:.*')
    
    def test_tracelog_frequencies(self):
        assert self.is_in_tracelog(r'frequencies\.s:.*')


class ModelGamma(object):
    """Tests Models with Gamma Distributed Rate Heterogeneity"""
    def test_state_gammaShape(self):
        """gammaShape should be in state"""
        assert self.is_in_state(r'gammaShape\.s')
    
    def test_prior_gammaShape(self):
        assert self.is_in_prior(r'GammaShapePrior\.s:.*')
    
    def test_siteModel_gammaCategoryCount_gt_1(self):
        """Site model should have GammaCategoryCount > 1"""
        siteModel = self.xml.find('.//siteModel')
        try:
            gammaCategoryCount = int(siteModel.get('gammaCategoryCount'))
        except TypeError:
            raise TypeError("No gammaCategoryCount on siteModel")
        
        if gammaCategoryCount <= 1:
            raise ValueError("GammaCategoryCount is %d" % gammaCategoryCount)
    
    def test_siteModel_has_gammaShape(self):
        siteModel = self.xml.find('.//siteModel')
        assert siteModel.get('shape') is not None, "No gammaShape on siteModel"
    
    def test_operator_gammaShapeScaler(self):
        """gammaShapeScaler should be in operators"""
        assert self.is_in_operators(r"gammaShapeScaler\..*")
    
    def test_tracelog_gammaShape(self):
        assert self.is_in_tracelog(r'gammaShape\.*')
     
        
class ModelDollo(object):
    """Tests Dollo Analyses"""
    
    # data
    def test_userdatatype_not_in_data(self):
        assert self.xml.find('./data/userDataType') is None
    
    def test_userdatatype(self):
        """Test Dollo userDataType"""
        udt = self.xml.find('.//userDataType')
        assert udt.get('spec') == "beast.evolution.datatype.UserDataType"
        assert udt.get('codeMap') is not None
        assert int(udt.get('states')) == 4
        assert int(udt.get('codelength')) == 1
    
    # state
    def test_state_clockRate(self):
        assert self.is_in_state(r"cognateDeathRate\.s:.*", key='idref')
    
    # substModel
    def test_substModel_is_MutationDeathModel(self):
        substModel = self.xml.find('.//substModel')
        if substModel is None:
            raise IndexError("substModel not found")
        assert substModel.get('spec') == 'MutationDeathModel'
    
    def test_substModel_frequency(self):
        """
        Tests that substModel has a frequencies parameter
        """
        substModel = self.xml.find('.//substModel')
        freqs = self.get_matching_children(
            substModel, "Frequencies", key="spec"
        )
        assert len(freqs) == 1, 'Unable to Find Frequencies Parameter'
    
    def test_substModel_deathprob(self):
        """
        Tests that substModel has a deathprob parameter
        """
        substModel = self.xml.find('.//substModel')
        params = self.get_matching_children(
            substModel, "cognateDeathRate", key="id"
        )
        assert len(params) == 1, 'Unable to find deathprob'
    
    # operators
    def test_operator_cognateDeathRateOperator(self):
        assert self.is_in_operators(r"cognateDeathRateOperator\.s.*")
    
    # logging
    def test_tracelog_cognateDeathRate(self):
        assert self.is_in_tracelog(r'cognateDeathRate\.s:.*')
    
        




#---------------------------------------------------------------------------#
# CLOCKS
class StrictClock(object):
    """Mixin to test clock model"""
    def test_treelikelihood_has_strict_BranchRateModel(self):
        spec = "beast.base.evolution.branchratemodel.StrictClockModel"
        lh = self.xml.find('.//distribution[@id="likelihood"]')
        treelh = self.get_matching_children(lh, r'treeLikelihood\..*')[0]
        brm = treelh.find("branchRateModel")
        assert brm is not None, "No branchRateModel in treeLikelihood"
        assert brm.get('id').startswith('StrictClock.c')
        assert brm.get('spec') == spec, 'spec mismatch'
    
    # state
    def test_state_clockRate(self):
        assert self.is_in_state(r"clockRate\.c:.*")
    
    # priors
    def test_prior_ClockPrior(self):
        assert self.is_in_prior(r'ClockPrior\.c:.*')
    
    # operators
    def test_operator_StrictClockRateScaler(self):
        assert self.is_in_operators(r"StrictClockRateScaler\.c.*")
    
    def test_operator_strictClockUpDownOperator(self):
        assert self.is_in_operators(r"strictClockUpDownOperator\.c.*")
    
    # logging
    def test_tracelog_ucldMean(self):
        assert self.is_in_tracelog(r'clockRate\.c:.*')
    
    def test_tree_has_correct_branchrates(self):
        treelogs = self.xml.findall('run/logger[@mode="tree"]')
        for treelog in treelogs:
            brm = treelog.find('log').get('branchratemodel')
            # is this correct?
            assert brm is None, 'check the branchratemodel'
        


class RelaxedClock(object):
    """Mixin to test clock model"""
    def test_treelikelihood_has_relaxed_BranchRateModel(self):
        spec = "beast.evolution.branchratemodel.UCRelaxedClockModel"
        lh = self.xml.find('.//distribution[@id="likelihood"]')
        treelh = self.get_matching_children(lh, r'treeLikelihood\..*')[0]
        brm = treelh.find("branchRateModel")
        assert brm is not None, "No branchRateModel in treeLikelihood"
        assert brm.get('id').startswith('RelaxedClock.c')
        assert brm.get('spec') == spec, 'spec mismatch'
    
    # state
    def test_state_ucldStdev(self):
        assert self.is_in_state(r"ucldStdev\.c:.*")
    
    def test_state_ucldMean(self):
        assert self.is_in_state(r"ucldMean\.c:.*")
    
    def test_state_rateCategories(self):
        assert self.is_in_state(r"rateCategories\.c:.*")
    
    def test_state_rateCategories_dimension(self):
        """
        Checks that the number of dimensions in the rateCategories is equal to:
            (2 * ntaxa) - 2
        """
        p = re.compile(r"""rateCategories\.c:.*""")
        state = self.xml.find('./run/state')
        children = [
            s for s in state if p.match(s.get('id', 'No'))
        ]
        if len(children) == 0:
            raise AssertionError("Unable to find rateCategories.c in state")
        elif len(children) > 1:
            raise AssertionError("Multiple rateCategories.c in state")
        
        dimension = int(children[0].get('dimension'))
        expected = (self.ntaxa * 2) - 2
        if dimension != expected:
            raise AssertionError(
                'Dimension is %d not %d' % (expected, dimension)
            )
    
    # priors
    def test_prior_ucldStdevPrior(self):
        assert self.is_in_prior(r'ucldStdevPrior\.c:.*')
        
    # operators
    def test_operator_ucldMeanScaler(self):
        assert self.is_in_operators(r"ucldMeanScaler\.c.*")
    
    def test_operator_ucldStdevScaler(self):
        assert self.is_in_operators(r"ucldStdevScaler\.c.*")
    
    def test_operator_CategoriesRandomWalk(self):
        assert self.is_in_operators(r"CategoriesRandomWalk\.c.*")
    
    def test_operator_CategoriesSwapOperator(self):
        assert self.is_in_operators(r"CategoriesSwapOperator\.c.*")
    
    def test_operator_CategoriesUniform(self):
        assert self.is_in_operators(r"CategoriesUniform\.c.*")
    
    def test_operator_relaxedUpDownOperator(self):
        assert self.is_in_operators(r"relaxedUpDownOperator\.c.*")
    
    # logging
    def test_tracelog_ucldMean(self):
        assert self.is_in_tracelog(r'ucldMean\.c:.*')
    
    def test_tracelog_ucldStdev(self):
        assert self.is_in_tracelog(r'ucldStdev\.c:.*')
 
    def test_tracelog_rate_c(self):
        assert self.is_in_tracelog(r'rate\.c:.*', key='id')
    
    def test_tree_has_correct_branchrates(self):
        treelogs = self.xml.findall('run/logger[@mode="tree"]')
        for treelog in treelogs:
            brm = treelog.find('log').get('branchratemodel')
            if brm is None:
                raise AssertionError("Expected a branchratemodel")
                assert brm.startswith("@RelaxedClock.c"), "Expected a RelaxedClock branchratemodel"


class OptimisedRelaxedClock(object):
    """Mixin to test clock model"""
    def test_treelikelihood_has_relaxed_BranchRateModel(self):
        spec = "beast.base.evolution.branchratemodel.UCRelaxedClockModel"
        lh = self.xml.find('.//distribution[@id="likelihood"]')
        treelh = self.get_matching_children(lh, r'treeLikelihood\..*')[0]
        brm = treelh.find("branchRateModel")
        assert brm is not None, "No branchRateModel in treeLikelihood"
        assert brm.get('id').startswith('OptimisedRelaxedClock.c')
        assert brm.get('spec') == spec, 'spec mismatch'
    
    # state
    def test_state_ORCsigma(self):
        assert self.is_in_state(r"ORCsigma\.c:.*")
    
    def test_state_ORCRates(self):
        assert self.is_in_state(r"ORCRates\.c:.*")
    
    def test_state_ORCRates_dimension(self):
        """
        Checks that the number of dimensions in the rateCategories is equal to:
            (2 * ntaxa) - 2
        """
        p = re.compile(r"""ORCRates\.c:.*""")
        state = self.xml.find('./run/state')
        children = [
            s for s in state if p.match(s.get('id', 'No'))
        ]
        if len(children) == 0:
            raise AssertionError("Unable to find ORCRates.c in state")
        elif len(children) > 1:
            raise AssertionError("Multiple ORCRates.c in state")
        
        dimension = int(children[0].get('dimension'))
        expected = (self.ntaxa * 2) - 2
        if dimension != expected:
            raise AssertionError(
                'Dimension is %d not %d' % (expected, dimension)
            )
    
    # priors
    def test_prior_ucldStdevPrior(self):
        assert self.is_in_prior(r'ORCsigmaPrior\.c:.*')

    def test_prior_ORCRatePriorDistribution(self):
        assert self.is_in_prior(r'ORCRatePriorDistribution\.c:.*')
    
    # operators
    def test_operator_ORCAdaptableOperatorSampler_sigma(self):
        assert self.is_in_operators(r"ORCAdaptableOperatorSampler_sigma\.c.*")
    
    def test_operator_ORCAdaptableOperatorSampler_rates_root(self):
        assert self.is_in_operators(r"ORCAdaptableOperatorSampler_rates_root\.c.*")
    
    def test_operator_ORCAdaptableOperatorSampler_rates_internal(self):
        assert self.is_in_operators(r"ORCAdaptableOperatorSampler_rates_internal\.c.*")
    
    def test_operator_ORCAdaptableOperatorSampler_NER(self):
        assert self.is_in_operators(r"ORCAdaptableOperatorSampler_NER\.c.*")
    
    # logging
    def test_tracelog_ucldStdev(self):
        assert self.is_in_tracelog(r'ORCsigma\.c:.*')
 
    def test_tracelog_rate_c(self):
        assert self.is_in_tracelog(r'ORCRatesStat\.c:.*', key='id')
    
    def test_tree_has_correct_branchrates(self):
        treelogs = self.xml.findall('run/logger[@mode="tree"]')
        for treelog in treelogs:
            if treelog.attrib.get('spec', '') != 'Logger':
                continue
            brm = treelog.find('log').get('branchratemodel')
            if brm is None:
                raise AssertionError("Expected a branchratemodel")
            assert brm.startswith("@OptimisedRelaxedClock.c"), "Expected a OptimisedRelaxedClock branchratemodel"
    
  
  
#---------------------------------------------------------------------------#
# Misc.
class AscertainmentBias(object):
    """Mixin to test for Ascertainment Bias"""
    def test_ascertainment_character(self):
        for seq in self.xml.findall('./data/sequence'):
            site_zero = seq.get('value')[0]
            if site_zero != '0':
                raise AssertionError(
                    "Expected site zero to be 0 for ascertainment"
                )
    
    def test_treeLikelihood_corrects_for_ascertainment(self):
        data = self.xml.find('.//distribution[@id="likelihood"]//data')
        assert data.get('ascertained') == 'true'
        
    def test_treeLikelihood_has_exclude_set_correctly(self):
        data = self.xml.find('.//distribution[@id="likelihood"]//data')
        assert data.get('excludeto') == '1'  # not inclusive.
      


class BayesianSkylineTreePrior(object):
    
    def test_BSP_state_bPopSizes(self):
        assert self.is_in_state(r'bPopSizes\.t:.*')

    def test_BSP_state_bGroupSizes(self):
        assert self.is_in_state(r'bGroupSizes\.t:.*')
    
    def test_BSP_prior_MarkovChainedPopSizes(self):
        assert self.is_in_prior(r'MarkovChainedPopSizes\.t:.*')
    
    def test_BSP_prior_BayesianSkyline(self):
        assert self.is_in_prior(r'BayesianSkyline\.t:.*')

    def test_BSP_operators(self):
        assert self.is_in_operators(r"BayesianSkylineTreeScaler\.t:.*")
        assert self.is_in_operators(r"BayesianSkylineTreeRootScaler\.t:.*")
        assert self.is_in_operators(r"BayesianSkylineUniformOperator\.t:.*")
        assert self.is_in_operators(r"BayesianSkylineSubtreeSlide\.t:.*")
        assert self.is_in_operators(r"BayesianSkylineNarrow\.t:.*")
        assert self.is_in_operators(r"BayesianSkylineWide\.t:.*")
        assert self.is_in_operators(r"BayesianSkylineWilsonBalding\.t:.*")
        assert self.is_in_operators(r"popSizesScaler\.t:.*")
        assert self.is_in_operators(r"groupSizesDelta\.t:.*")
    
    def test_BSP_logging(self):
        assert self.is_in_tracelog(r"BayesianSkyline\.t:.*")
        assert self.is_in_tracelog(r"bPopSizes\.t:.*")
        assert self.is_in_tracelog(r"bGroupSizes\.t:.*")
        

class BirthDeathSkylineSerialTreePrior(object):
    
    def test_BDSS_state_origin(self):
        assert self.is_in_state(r"origin\.t:.*")
    
    def test_BDSS_state_rho(self):
        assert self.is_in_state(r"rho\.t:.*")
    
    def test_BDSS_state_becomeUninfectiousRate(self):
        assert self.is_in_state(r"becomeUninfectiousRate\.t:.*")
    
    def test_BDSS_state_R0(self):
        assert self.is_in_state(r"R0")
    
    def test_BDSS_prior_BirthDeathSkySerial(self):
        assert self.is_in_prior(r'BirthDeathSkySerial\.t:.*')
        
    def test_BDSS_prior_becomeUninfectiousRatePrior(self):
        assert self.is_in_prior('becomeUninfectiousRatePrior\.t:.*')

    def test_BDSS_prior_originPrior(self):
        assert self.is_in_prior(r'originPrior\.t:.*')

    def test_BDSS_prior_rhoPrior(self):
        assert self.is_in_prior(r'rhoPrior\.t:.*')

    def test_BDSS_prior_R0_Prior(self):
        assert self.is_in_prior(r'R0_Prior')
    
    def test_BDSS_operators(self):
        assert self.is_in_operators(r"becomeUninfectiousRateScaler\.t:.*")
        assert self.is_in_operators(r"rhoScaler\.t:.*")
        assert self.is_in_operators(r"origScaler\.t:.*")
        assert self.is_in_operators(r'R0_scaler')
        assert self.is_in_operators(r"BDSKY_serial_treeScaler\.t:.*")
        assert self.is_in_operators(r"BDSKY_serial_treeRootScaler\.t:.*")
        assert self.is_in_operators(r"BDSKY_serial_UniformOperator\.t:.*")
        assert self.is_in_operators(r"BDSKY_serial_SubtreeSlide\.t:.*")
        assert self.is_in_operators(r"BDSKY_serial_narrow\.t:.*")
        assert self.is_in_operators(r"BDSKY_serial_wide\.t:.*")
        assert self.is_in_operators(r"BDSKY_serial_WilsonBalding\.t:.*")
        
    def test_BDSS_logging(self):
        assert self.is_in_tracelog(r"BirthDeathSkySerial\.t:.*")
        assert self.is_in_tracelog(r"origin\.t:.*")
        assert self.is_in_tracelog(r"rho\.t:.*")
        assert self.is_in_tracelog(r"becomeUninfectiousRate\.t:.*")
        assert self.is_in_tracelog(r"R0")



class BirthDeathSkylineContemporaryTreePrior(object):
    
    def test_BDSS_state_rho(self):
        assert self.is_in_state(r"rho_BDSKY_Contemp\.t:.*")
    
    def test_BDSS_state_becomeUninfectiousRate(self):
        assert self.is_in_state(r"becomeUninfectiousRate_BDSKY_Contemp\.t:.*")
    
    def test_BDSS_state_R0(self):
        assert self.is_in_state(r"reproductiveNumber_BDSKY_Contemp\.t:.*")
    
    def test_BDSS_state_R0(self):
        assert self.is_in_state(r"origin_BDSKY_Contemp\.t:.*")
    
    def test_BDSS_prior_becomeUninfectiousRatePrior(self):
        assert self.is_in_prior(r'becomeUninfectiousRatePrior_BDSKY_Contemp\.t:.*')

    def test_BDSS_prior_rhoPrior(self):
        assert self.is_in_prior(r'rhoPrior_BDSKY_Contemp\.t:.*')

    def test_BDSS_prior_R0_Prior(self):
        assert self.is_in_prior(r'reproductiveNumberPrior_BDSKY_Contemp\.t:.*')

    def test_BDSS_prior_origin_Prior(self):
        assert self.is_in_prior(r'originPrior_BDSKY_Contemp\.t:.*')
    
    def test_BDSS_operators_origin(self):
        assert self.is_in_operators(r"origScaler_BDSKY_Contemp\.t:.*")

    def test_BDSS_operators_rho(self):
        assert self.is_in_operators(r"rhoScaler_BDSKY_Contemp\.t:.*")

    def test_BDSS_operators_becomeUninfectious(self):
        assert self.is_in_operators(r"becomeUninfectiousRateScaler_BDSKY_Contemp\.t:.*")

    def test_BDSS_operators_reproductiveNumberScaler(self):
        assert self.is_in_operators(r'reproductiveNumberScaler_BDSKY_Contemp\.t:.*')

    def test_BDSS_operators(self):
        assert self.is_in_operators(r"BDSKY_ContempTreeScaler\.t:.*")
        assert self.is_in_operators(r"BDSKY_ContempTreeRootScaler\.t:.*")
        assert self.is_in_operators(r"BDSKY_ContempUniformOperator\.t:.*")
        assert self.is_in_operators(r"BDSKY_ContempSubtreeSlide\.t:.*")
        assert self.is_in_operators(r"BDSKY_ContempNarrow\.t:.*")
        assert self.is_in_operators(r"BDSKY_ContempWide\.t:.*")
        assert self.is_in_operators(r"BDSKY_ContempWilsonBalding\.t:.*")
        
    def test_BDSS_logging(self):
        assert self.is_in_tracelog(r"BDSKY_Contemp\.t:.*")
        assert self.is_in_tracelog(r"origin_BDSKY_Contemp\.t:.*")
        assert self.is_in_tracelog(r"rho_BDSKY_Contemp\.t:.*")
        assert self.is_in_tracelog(r"becomeUninfectiousRate_BDSKY_Contemp\.t:.*")
        assert self.is_in_tracelog(r"reproductiveNumber_BDSKY_Contemp\.t:.*")


class BirthDeathSkylineContemporaryBDSParamTreePrior(object):
    # state
    def test_BDSS_state_rho(self):
        assert self.is_in_state(r"rhoBDS\.t:.*")

    def test_BDSS_state_birthRateBDS(self):
        assert self.is_in_state(r"birthRateBDS\.t:.*")

    def test_BDSS_state_deathRateBDS(self):
        assert self.is_in_state(r"deathRateBDS\.t:.*")
    
    # prior
    def test_BDSS_prior_BirthDeathSkyContemporaryBDSParam(self):
        assert self.is_in_prior(r'BirthDeathSkyContemporaryBDSParam\.t:.*')

    def test_BDSS_prior_birthRatePriorContempBDS(self):
        assert self.is_in_prior(r'birthRatePriorContempBDS\.t:.*')

    def test_BDSS_prior_deathRatePriorContempBDS(self):
        assert self.is_in_prior(r'deathRatePriorContempBDS\.t:.*')

    def test_BDSS_prior_rhoPriorContempBDS(self):
        assert self.is_in_prior(r'rhoPriorContempBDS\.t:.*')

    def test_rhoPriorContempBDS(self):
        assert self.is_in_prior(r'rhoPriorContempBDS\.t:.*')
        
    def test_BDSS_operators(self):
        assert self.is_in_operators(r"BDSKY_contemp_bds_treeScaler\.t:.*")
        assert self.is_in_operators(r"BDSKY_contemp_bds_treeRootScaler\.t:.*")
        assert self.is_in_operators(r"BDSKY_contemp_bds_UniformOperator\.t:.*")
        assert self.is_in_operators(r'BDSKY_contemp_bds_SubtreeSlide\.t:.*')
        assert self.is_in_operators(r"BDSKY_contemp_bds_narrow\.t:.*")
        assert self.is_in_operators(r"BDSKY_contemp_bds_wide\.t:.*")
        assert self.is_in_operators(r"BDSKY_contemp_bds_WilsonBalding\.t:.*")
        assert self.is_in_operators(r"BDSKY_contemp_bds_birthRateScaler\.t:.*")
        assert self.is_in_operators(r"BDSKY_contemp_bds_deathRateScaler\.t:.*")
        assert self.is_in_operators(r"BDSKY_contemp_bds_rhoScaler\.t:.*")
        assert self.is_in_operators(r"BDSKY_contemp_bds_updownBD\.t:.*")
        
    def test_BDSS_logging(self):
        assert self.is_in_tracelog(r"BirthDeathSkyContemporaryBDSParam\.t:.*")
        assert self.is_in_tracelog(r"birthRateBDS\.t:.*")
        assert self.is_in_tracelog(r"deathRateBDS\.t:.*")
        assert self.is_in_tracelog(r"rhoBDS\.t:.*")



class Analysis(AscertainmentBias, BirthDeathSkylineContemporaryBDSParamTreePrior, BeastTest):
    ntaxa = 26
    nchar = 1084
    ngenerations = 20000000
    logEvery = 10000
    
    sampling_proportion_alpha = 26.0
    sampling_proportion_beta = 4.0
    
    others = {}
    
    def test_rho_value(self):
        prior = self.xml.find('./run/distribution/distribution/[@id="prior"]')
        rho = self.get_matching_children(prior, r"rhoPriorContempBDS\.t:.*")[0]

        b = rho.find('./Beta')
        assert b.tag == 'Beta'

        alpha = b.find('./parameter/[@name="alpha"]').text
        beta = b.find('./parameter/[@name="beta"]').text
        assert float(alpha) == self.sampling_proportion_alpha, "%r != expected alpha %r" % (alpha, self.sampling_proportion_alpha)
        assert float(beta) == self.sampling_proportion_beta, "%r != expected beta %r" % (beta, self.sampling_proportion_beta)


# ANALYSES
class TestCTMCStrict(Analysis, ModelCTMC, StrictClock, unittest.TestCase):
    filename = 'pano_ctmc_strict.xml'


class TestCTMCRelaxed(Analysis, ModelCTMC, OptimisedRelaxedClock, unittest.TestCase):
    filename = 'pano_ctmc_relaxed.xml'


class TestCTMCGammaStrict(Analysis, ModelCTMC, ModelGamma, StrictClock, unittest.TestCase):
    filename = 'pano_ctmc_gamma4_strict.xml'


class TestCTMCGammaRelaxed(Analysis, ModelCTMC, ModelGamma, OptimisedRelaxedClock, unittest.TestCase):
    filename = 'pano_ctmc_gamma4_relaxed.xml'


class TestCovarionStrict(Analysis, ModelCovarion, StrictClock, unittest.TestCase):
    filename = 'pano_covarion_strict.xml'


class TestCovarionRelaxed(Analysis, ModelCovarion, OptimisedRelaxedClock, unittest.TestCase):
    filename = 'pano_covarion_relaxed.xml'



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="BeastCheck v. %s" % VERSION)
    parser.add_argument("-v", '--validate', help='use BEAST validator (slow)', default=False)
    args = parser.parse_args()

    print("BeastCheck v%s" % VERSION)
    if args.validate:
        del sys.argv[1:]
        Analysis.validate = True
    unittest.main()
