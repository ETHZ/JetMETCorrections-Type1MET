// -*- C++ -*-
//
// Package:    Type1MET
// Class:      Type1MET
// 
/**\class Type1MET Type1MET.cc JetMETCorrections/Type1MET/src/Type1MET.cc

 Description: <one line class summary>

 Implementation:
     <Notes on implementation>
*/
//
// Original Author:  Oct 12 08:23
//         Created:  Wed Oct 12 12:16:04 CDT 2005
// $Id: Type1MET.cc,v 1.7 2006/10/20 17:50:49 cavana Exp $
//
//


// system include files
#include <memory>

#include <string.h>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/Handle.h"
#include "JetMETCorrections/Type1MET/interface/Type1METAlgo.h"
#include "DataFormats/METReco/interface/METCollection.h"
#include "DataFormats/METReco/interface/CaloMETCollection.h"
#include "DataFormats/JetReco/interface/CaloJetCollection.h"

//using namespace std;

namespace cms 
{
  // PRODUCER CLASS DEFINITION -------------------------------------
  class Type1MET : public edm::EDProducer 
  {
  public:
    explicit Type1MET( const edm::ParameterSet& );
    explicit Type1MET();
    virtual ~Type1MET();
    virtual void produce( edm::Event&, const edm::EventSetup& );
  private:
    Type1METAlgo alg_;
    std::string metType;
    std::string inputUncorMetLabel;
    std::string inputUncorJetsLabel;
    std::string inputCorJetsLabel;
    double jetPTthreshold;
  };

  // PRODUCER CONSTRUCTORS ------------------------------------------
  Type1MET::Type1MET( const edm::ParameterSet& iConfig ) : alg_() 
  {
    metType             = iConfig.getParameter<std::string>("metType");
    
    inputUncorMetLabel  = iConfig.getParameter<std::string>("inputUncorMetLabel");
    inputUncorJetsLabel = iConfig.getParameter<std::string>("inputUncorJetsLabel");
    inputCorJetsLabel   = iConfig.getParameter<std::string>("inputCorJetsLabel");
    jetPTthreshold      = iConfig.getParameter<double>("jetPTthreshold");
    if( metType == "CaloMET" )
      produces<CaloMETCollection>();
    else
      produces<METCollection>();
  }
  Type1MET::Type1MET() : alg_() {}
  // PRODUCER DESTRUCTORS -------------------------------------------
  Type1MET::~Type1MET() {}

  // PRODUCER METHODS -----------------------------------------------
  void Type1MET::produce( edm::Event& iEvent, const edm::EventSetup& iSetup )
  {
    using namespace edm;
    Handle<CaloJetCollection> inputUncorJets;
    Handle<CaloJetCollection> inputCorJets;
    iEvent.getByLabel( inputUncorJetsLabel, inputUncorJets );
    iEvent.getByLabel( inputCorJetsLabel,   inputCorJets );
    if( metType == "CaloMET")
      {
	Handle<CaloMETCollection> inputUncorMet;                     //Define Inputs
	iEvent.getByLabel( inputUncorMetLabel,  inputUncorMet );     //Get Inputs
	std::auto_ptr<CaloMETCollection> output( new CaloMETCollection() );  //Create empty output
	alg_.run( inputUncorMet.product(), inputUncorJets.product(), 
		  inputCorJets.product(), jetPTthreshold, *output ); //Invoke the algorithm
	iEvent.put( output );                                        //Put output into Event
      }
    else
      {
	Handle<METCollection> inputUncorMet;                     //Define Inputs
	iEvent.getByLabel( inputUncorMetLabel,  inputUncorMet );     //Get Inputs
	std::auto_ptr<METCollection> output( new METCollection() );  //Create empty output
	alg_.run( inputUncorMet.product(), inputUncorJets.product(), 
		  inputCorJets.product(), jetPTthreshold, *output ); //Invoke the algorithm
	iEvent.put( output );                                        //Put output into Event
      }
  }

  DEFINE_FWK_MODULE(Type1MET);  //define this as a plug-in

}//end namespace cms

