import FWCore.ParameterSet.Config as cms

process = cms.Process("R")
# initialize MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

# Magnetic field now needs to be in the high-level py
process.load("Configuration.StandardSequences.MagneticField_cff")

process.load("JetMETCorrections.Type1MET.MetMuonCorrections_cff")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10)
)
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:jet15_20.root')
)

process.RECO = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('muonmet.root')
)

process.p4 = cms.Path(process.MetMuonCorrections)
process.outpath = cms.EndPath(process.RECO)
process.PoolSource.fileNames = ['file:/scratch3/terashi/cmssw-160/fevt_RelVal145Z_MM_2E273E2F-685B-DC11-996E-000423D98F98.root']

