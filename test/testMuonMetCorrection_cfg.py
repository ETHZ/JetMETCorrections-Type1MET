import FWCore.ParameterSet.Config as cms

process = cms.Process("OWNPARTICLES")

process.load("FWCore.MessageService.MessageLogger_cfi")
## configure geometry
process.load("Configuration.StandardSequences.Geometry_cff")
## configure B field
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("TrackingTools.TrackAssociator.DetIdAssociatorESProducer_cff")


process.load("JetMETCorrections.Type1MET.MuonMETValueMapProducer_cff")
process.load("JetMETCorrections.Type1MET.MetMuonCorrections_cff")


process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
    '/store/relval/CMSSW_3_1_0_pre4/RelValZMM/GEN-SIM-RECO/STARTUP_30X_v1/0003/5C786CEA-D415-DE11-9F1D-000423D6B358.root')
)

process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('myOutputFileAll.root')
)

  
process.p = cms.Path(process.muonMETValueMapProducer*process.corMetGlobalMuons)

process.e = cms.EndPath(process.out)
