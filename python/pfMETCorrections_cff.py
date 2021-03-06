import FWCore.ParameterSet.Config as cms
# $Id: pfMETCorrections_cff.py,v 1.14 2013/05/14 23:18:39 sakuma Exp $

##____________________________________________________________________________||
from JetMETCorrections.Configuration.JetCorrectionServices_cff import *

##____________________________________________________________________________||
# select PFCandidates ("unclustered energy") not within jets
# for Type 2 MET correction
from CommonTools.ParticleFlow.TopProjectors.pfNoJet_cfi import pfNoJet
# the new TopProjectors now work with Ptrs
# a conversion is needed if objects are not available
# add them upfront of the sequence
ak5PFJetsPtrs = cms.EDProducer("PFJetFwdPtrProducer",
   src = cms.InputTag("ak5PFJets")
)
# this one is needed only if the input file doesn't have it
# solved automatically with unscheduled execution
from RecoParticleFlow.PFProducer.pfLinker_cff import particleFlowPtrs
# particleFlowPtrs = cms.EDProducer("PFCandidateFwdPtrProducer",
#    src = cms.InputTag("particleFlow")
# )
# FIXME: THIS IS A WASTE, BUT NOT CLEAR HOW TO FIX IT CLEANLY: the module
# downstream operates with View<reco::Candidate>, I wish one could read
# it from std::vector<PFCandidateFwdPtr> directly
pfCandsNotInJetPtrs = pfNoJet.clone(
    topCollection = cms.InputTag('ak5PFJetsPtrs'),
    bottomCollection = cms.InputTag('particleFlowPtrs')
)
pfCandsNotInJet = cms.EDProducer("PFCandidateFromFwdPtrProducer",
    src = cms.InputTag("pfCandsNotInJetPtrs")
)

##____________________________________________________________________________||
pfJetMETcorr = cms.EDProducer("PFJetMETcorrInputProducer",
    src = cms.InputTag('ak5PFJets'),
    offsetCorrLabel = cms.string("ak5PFL1Fastjet"),
    jetCorrLabel = cms.string("ak5PFL1FastL2L3"), # NOTE: use "ak5PFL1FastL2L3" for MC / "ak5PFL1FastL2L3Residual" for Data
    jetCorrEtaMax = cms.double(9.9),
    type1JetPtThreshold = cms.double(10.0),
    type2ResidualCorrLabel = cms.string(""),
    type2ResidualCorrEtaMax = cms.double(9.9),
    type2ResidualCorrOffset = cms.double(0.),
    isMC = cms.bool(False), # CV: only used to decide whether to apply "unclustered energy" calibration to MC or Data                               
    skipEM = cms.bool(True),
    skipEMfractionThreshold = cms.double(0.90),
    skipMuons = cms.bool(True),
    skipMuonSelection = cms.string("isGlobalMuon | isStandAloneMuon")
)                                         

##____________________________________________________________________________||
pfCandMETcorr = cms.EDProducer("PFCandMETcorrInputProducer",
    src = cms.InputTag('pfCandsNotInJet'),
    residualCorrLabel = cms.string(""),
    residualCorrEtaMax = cms.double(9.9),
    residualCorrOffset = cms.double(0.),
    isMC = cms.bool(False) # CV: only used to decide whether to apply "unclustered energy" calibration to MC or Data
)   

##____________________________________________________________________________||
pfchsMETcorr = cms.EDProducer("PFchsMETcorrInputProducer",
    src = cms.InputTag('offlinePrimaryVertices'),
    goodVtxNdof = cms.uint32(4),
    goodVtxZ = cms.double(24)
)   

##____________________________________________________________________________||
pfType1CorrectedMet = cms.EDProducer("CorrectedPFMETProducer",
    src = cms.InputTag('pfMet'),
    applyType0Corrections = cms.bool(False),
    srcCHSSums = cms.VInputTag(
        cms.InputTag('pfchsMETcorr', 'type0')
    ),
    type0Rsoft = cms.double(0.6),
    applyType1Corrections = cms.bool(True),
    srcType1Corrections = cms.VInputTag(
        cms.InputTag('pfJetMETcorr', 'type1')
    ),
    applyType2Corrections = cms.bool(False)
)   

##____________________________________________________________________________||
pfType1p2CorrectedMet = cms.EDProducer("CorrectedPFMETProducer",
    src = cms.InputTag('pfMet'),
    applyType0Corrections = cms.bool(False),
    srcCHSSums = cms.VInputTag(
        cms.InputTag('pfchsMETcorr', 'type0')
    ),
    type0Rsoft = cms.double(0.6),
    applyType1Corrections = cms.bool(True),
    srcType1Corrections = cms.VInputTag(
        cms.InputTag('pfJetMETcorr', 'type1')
    ),
    applyType2Corrections = cms.bool(True),
    srcUnclEnergySums = cms.VInputTag(
        cms.InputTag('pfJetMETcorr', 'type2'),
        cms.InputTag('pfJetMETcorr', 'offset'),
        cms.InputTag('pfCandMETcorr')                                    
    ),                              
    type2CorrFormula = cms.string("A"),
    type2CorrParameter = cms.PSet(
        A = cms.double(1.4)
    )
)   

##____________________________________________________________________________||
producePFMETCorrections = cms.Sequence(
    ak5PFJetsPtrs
   * particleFlowPtrs 
   * pfCandsNotInJetPtrs
   * pfCandsNotInJet
   * pfJetMETcorr
   * pfCandMETcorr
   * pfchsMETcorr
   * pfType1CorrectedMet
   * pfType1p2CorrectedMet
)

##____________________________________________________________________________||
