import FWCore.ParameterSet.Config as cms

process = cms.Process("R")
# Magnetic field now needs to be in the high-level py
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Geometry.CommonDetUnit.globalTrackingGeometry_cfi")
process.load("Geometry.CommonDetUnit.bareGlobalTrackingGeometry_cfi")
process.GlobalTag.globaltag="IDEAL_V5::All"
process.load("JetMETCorrections.Type1MET.MetMuonCorrections_cff")
process.load("TrackingTools.TrackAssociator.default_cfi")
process.load("TrackingTools.TrackAssociator.DetIdAssociatorESProducer_cff")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10)
)
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:0AC27F01-D260-DD11-8207-0018F3D096EE.root')
)

#process.goodMuonsforMETCorrection = cms.EDFilter("MuonSelector",
#    src = cms.InputTag("muons"),
#    cut = cms.string('isGlobalMuon=1 & pt > 10.0 & abs(eta)<2.5 & innerTrack.numberOfValidHits>5 & combinedMuon.qoverpError< 0.5')
#)

process.RECO = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('muonmet.root')
)

##process.p4 = cms.Path(process.goodMuonsforMETCorrection*process.MetMuonCorrections)
process.p4 = cms.Path(process.MetMuonCorrections)
process.outpath = cms.EndPath(process.RECO)

