
# definitions from
# https://svnweb.cern.ch/trac/atlasusr/browser/ataffard/UpgradeNSW/TrigT1sTGC/trunk/TrigT1sTGC/sTGCgeometry.h?rev=140867

PAD_PHI_SUBDIVISION = 1.5      # Module 1 wrt Modules 2 and 3
PAD_PHI_DIVISION    = 0.130900 # Modules 2 and 3 in radians (7.50 deg in parameter book)
#___________________________________________________________
PHIPAD_SHIFT = {
    'PIVOT'    : (  0.00, -0.50,  0.00, -0.50 ),
    'CONFIRM'  : ( -0.25, -0.75, -0.25, -0.75 ),
    }
#___________________________________________________________
INDEX_LEFTMOST_COL = {
    'SMALL_PIVOT' : {
        'D0' : ( -1, -1, -1, -1 ),
        'D1' : ( -1, -1, -1, -1 ),
        'D2' : ( -1,  0, -1,  0 ),
        'D3' : ( -1,  0, -1,  0 ),
        },
    'SMALL_CONFIRM' : {
        'D0' : ( -1, -1, -1, -1),
        'D1' : ( -1, -1, -1, -1),
        'D2' : ( -1,  0, -1,  0),
        'D3' : ( -1,  0, -1,  0),
        },
    'LARGE_PIVOT' : {
        'D0' : ( -2, -1, -2, -1),
        'D1' : ( -2, -1, -2, -1),
        'D2' : ( -1,  0, -1,  0),
        'D3' : ( -1,  0, -1,  0),
        },
    'LARGE_CONFIRM' : {
        'D0' : ( -2, -1, -2, -1),
        'D1' : ( -2, -1, -2, -1),
        'D2' : ( -1,  0, -1,  0),
        'D3' : ( -1,  0, -1,  0),
        }
    }
#___________________________________________________________
INDEX_RIGHTMOST_COL = {
    'SMALL_PIVOT' : {
        'D0' : ( 1, 2, 1, 2),
        'D1' : ( 1, 2, 1, 2),
        'D2' : ( 1, 1, 1, 1),
        'D3' : ( 1, 1, 1, 1),
        },
    'SMALL_CONFIRM' : {
        'D0' : ( 1, 2, 1, 2),
        'D1' : ( 1, 2, 1, 2),
        'D2' : ( 1, 1, 1, 1),
        'D3' : ( 1, 1, 1, 1),
        },
    'LARGE_PIVOT' : {
        'D0' : ( 2, 2, 2, 2),
        'D1' : ( 2, 2, 2, 2),
        'D2' : ( 1, 1, 1, 1),
        'D3' : ( 1, 1, 1, 1),
        },
    'LARGE_CONFIRM' : {
        'D0' : (2, 2, 2, 2),
        'D1' : (2, 2, 2, 2),
        'D2' : (1, 1, 1, 1),
        'D3' : (1, 1, 1, 1),
        },
    }
#___________________________________________________________
H_PAD_ROW_0 = {
    'SMALL_PIVOT' : {
        'D0' : ( 922.5, 883.8, 920.3, 881.5),
        'D1' : ( 922.5, 883.8, 920.3, 881.5),
        'D2' : ( 922.5, 883.8, 920.3, 881.5),
        'D3' : ( 922.5, 883.8, 920.3, 881.5),
        },
    'SMALL_CONFIRM' : {
        'D0' : ( 861.1, 824.2, 859.0, 822.1),
        'D1' : ( 861.1, 824.2, 859.0, 822.1),
        'D2' : ( 861.1, 824.2, 859.0, 822.1),
        'D3' : ( 861.1, 824.2, 859.0, 822.1),
        },
    'LARGE_PIVOT' : {
        'D0' : ( 930.0, 891.0, 927.7, 888.6),
        'D1' : ( 930.0, 891.0, 927.7, 888.6),
        'D2' : ( 930.0, 891.0, 927.7, 888.6),
        'D3' : ( 930.0, 891.0, 927.7, 888.6),
        },
    'LARGE_CONFIRM' : {
        'D0' : ( 930.0, 891.0, 927.7, 888.6),
        'D1' : ( 930.0, 891.0, 927.7, 888.6),
        'D2' : ( 930.0, 891.0, 927.7, 888.6),
        'D3' : ( 930.0, 891.0, 927.7, 888.6),
        }
    }
#___________________________________________________________
PAD_HEIGHT = {
    'SMALL_PIVOT' : {
        'D0' : ( 80.0, 80.1, 80.2, 80.4),
        'D1' : ( 80.0, 80.1, 80.2, 80.4),
        'D2' : ( 80.0, 80.1, 80.2, 80.4),
        'D3' : ( 80.0, 80.1, 80.2, 80.4),
        },
    'SMALL_CONFIRM' : {
        'D0' : ( 76.3, 76.5, 76.6, 76.7),
        'D1' : ( 76.3, 76.5, 76.6, 76.7),
        'D2' : ( 76.3, 76.5, 76.6, 76.7),
        'D3' : ( 76.3, 76.5, 76.6, 76.7),
        },
    'LARGE_PIVOT' : {
        'D0' : ( 80.6, 80.8, 80.9, 81.0),
        'D1' : ( 80.6, 80.8, 80.9, 81.0),
        'D2' : ( 80.6, 80.8, 80.9, 81.0),
        'D3' : ( 80.6, 80.8, 80.9, 81.0),
        },
    'LARGE_CONFIRM' : {
        'D0' : ( 80.6, 80.8, 80.9, 81.0),
        'D1' : ( 80.6, 80.8, 80.9, 81.0),
        'D2' : ( 80.6, 80.8, 80.9, 81.0),
        'D3' : ( 80.6, 80.8, 80.9, 81.0),
        }
    }
#___________________________________________________________
PAD_ROWS = {
    'SMALL_PIVOT' : {
        'D0' : (  9,  8,  8,  7),
        'D1' : ( 11, 12, 11, 12),
        'D2' : ( 12, 12, 12, 11),
        'D3' : ( 12, 12, 12, 12),
        },
    'SMALL_CONFIRM' : {
        'D0' : (  9,  9,  8,  8),
        'D1' : ( 11, 11, 12, 12),
        'D2' : ( 12, 13, 12, 13),
        'D3' : ( 12, 13, 12, 12),
        },
    'LARGE_PIVOT' : {
        'D0' : (  8,  8,  8,  8),
        'D1' : ( 11, 11, 12, 11),
        'D2' : ( 13, 13, 13, 13),
        'D3' : ( 13, 13, 13, 13),
        },
    'LARGE_CONFIRM' : {
        'D0' : (  8,  8,  8,  8),
        'D1' : ( 11, 11, 12, 11),
        'D2' : ( 13, 13, 13, 13),
        'D3' : ( 13, 13, 13, 13),
        }
    }
#___________________________________________________________

# these functions should just map the enum used to create the nutple, see
# https://svnweb.cern.ch/trac/atlasusr/browser/ataffard/UpgradeNSW/TrigT1sTGC/trunk/TrigT1sTGC/sTGCenumeration.h?rev=140867
#___________________________________________________________
def pivotConfirm2str(pc) :
    return 'PIVOT' if pc==0 else 'CONFIRM'
#___________________________________________________________
def largeSmall2str(ls) :
    return 'SMALL' if ls==0 else 'LARGE'
#___________________________________________________________
def wedgeType2str(wt) :
    if   wt==0 : return 'SMALL_PIVOT'
    elif wt==1 : return 'SMALL_CONFIRM'
    elif wt==2 : return 'LARGE_PIVOT'
    elif wt==3 : return 'LARGE_CONFIRM'
#___________________________________________________________
def detectorNumber2str(dn) :
    return "D%d" % dn

def padPhiSize(detectorNumber) :
    return PAD_PHI_DIVISION / PAD_PHI_SUBDIVISION if detectorNumber in [0,1] else PAD_PHI_DIVISION

def padShift(pivotConfirm, layer) :
    return PHIPAD_SHIFT[pivotConfirm2str(pivotConfirm)][layer]

def padLeftmostColumn(wedgeType, detectorNumber, layer) :
    return INDEX_LEFTMOST_COL[wedgeType][detectorNumber2str(detectorNumber)][layer]

def padRightmostColumn(wedgeType, detectorNumber, layer) :
    return INDEX_RIGHTMOST_COL[wedgeType][detectorNumber2str(detectorNumber)][layer]

def padRow0(wedgeType, detectorNumber, layer) :
    return H_PAD_ROW_0[wedgeType][detectorNumber2str(detectorNumber)][layer]

def padHeight(wedgeType, detectorNumber, layer) :
    return PAD_HEIGHT[wedgeType][detectorNumber2str(detectorNumber)][layer]

def padRows(wedgeType, detectorNumber, layer) :
    return PAD_ROWS[wedgeType][detectorNumber2str(detectorNumber)][layer]
#___________________________________________________________
