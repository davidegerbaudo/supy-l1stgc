from supy.defaults import *

def mainTree() :
    return ('/','NSWL1SimulationTree')

def leavesToBlackList() :
    #return ['L1triggered', 'triggered', 'DCSBits']
    return []

def cppROOTDictionariesToGenerate() :
    return [
        #("vector<ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<float> > >", "vector;Math/LorentzVector.h"),
        #ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > etc. is addressed in linkdef.cxx
        ("ROOT::Math::Cartesian3D<float>", "Math/Point3D.h"),
        ("ROOT::Math::DisplacementVector3D<ROOT::Math::Cartesian3D<float>,ROOT::Math::DefaultCoordinateSystemTag>", "Math/Vector3D.h"),
        ("vector<ROOT::Math::DisplacementVector3D<ROOT::Math::Cartesian3D<float>,ROOT::Math::DefaultCoordinateSystemTag> >", "vector;Math/Vector3D.h"),
        ("ROOT::Math::PositionVector3D<ROOT::Math::Cartesian3D<float>,ROOT::Math::DefaultCoordinateSystemTag>", "Math/Point3D.h"),
        # for now we don't have any vec<vec< >>
        ]

def cppFiles() :
    return [
            "cpp/linkdef.cxx",
            ]

def LorentzVectorType() : return ('PtEtaPhiM4D','float')
def PositionVectorType() : return ('Cartesian3D','float')
