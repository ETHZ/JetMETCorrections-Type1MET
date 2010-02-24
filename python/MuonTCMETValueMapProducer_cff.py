import FWCore.ParameterSet.Config as cms

muonTCMETValueMapProducer = cms.EDProducer("MuonTCMETValueMapProducer",
     muonInputTag     = cms.InputTag("muons"),
     beamSpotInputTag = cms.InputTag("offlineBeamSpot"),
     rf_type          = cms.int32(1),                                           
     pt_min           = cms.double(1.),
     pt_max           = cms.double(100.),
     eta_max          = cms.double(2.65),
     chi2_max         = cms.double(5),
     nhits_min        = cms.double(6),
     d0_max           = cms.double(0.1),
     ptErr_max        = cms.double(0.2),
     track_quality    = cms.vint32(2),
     track_algos      = cms.vint32(),                                           
     d0_muon          = cms.double(0.2),
     pt_muon          = cms.double(10),
     eta_muon         = cms.double(2.4),
     chi2_muon        = cms.double(10),
     nhits_muon       = cms.double(11),
     global_muon      = cms.bool(True),
     tracker_muon     = cms.bool(True),
     deltaR_muon      = cms.double(0.05),
     useCaloMuons     = cms.bool(False),
     muonMinValidStaHits = cms.int32(1)
)
