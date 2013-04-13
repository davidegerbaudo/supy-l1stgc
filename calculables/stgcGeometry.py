
# definitions from
# https://svnweb.cern.ch/trac/atlasusr/browser/ataffard/UpgradeNSW/NSWAna/NSWNtuple/trunk/NSWNtuple/sTGCgeometry.h
# NSW STGC (c) Daniel.Lellouch@cern.ch April 9, 2013

import math
#___________________________________________________________
H1 = {
    'SMALL_PIVOT' : {
        'D0' : ( 1019.4, 1019.4, 1019.4, 1019.4),
        'D1' : ( 1681.4, 1651.4, 1621.4, 1591.4),
        'D2' : ( 2541.4, 2541.4, 2541.4, 2541.4),
        'D3' : ( 3510.9, 3510.9, 3510.9, 3510.9),
        },
    'SMALL_CONFIRM' : {
        'D0' : ( 1019.4, 1019.4, 1019.4, 1019.4),
        'D1' : ( 1681.4, 1651.4, 1621.4, 1591.4),
        'D2' : ( 2541.4, 2541.4, 2541.4, 2541.4),
        'D3' : ( 3510.9, 3510.9, 3510.9, 3510.9),
        },
    'LARGE_PIVOT' : {
        'D0' : (  982.0,  982.0,  982.0,  982.0),
        'D1' : ( 1678.0, 1648.0, 1618.0, 1588.0),
        'D2' : ( 2538.0, 2538.0, 2538.0, 2538.0),
        'D3' : ( 3598.0, 3598.0, 3598.0, 3598.0),
        },
    'LARGE_CONFIRM' : {
        'D0' : (  982.0,  982.0,  982.0,  982.0),
        'D1' : ( 1678.0, 1648.0, 1618.0, 1588.0),
        'D2' : ( 2538.0, 2538.0, 2538.0, 2538.0),
        'D3' : ( 3598.0, 3598.0, 3598.0, 3598.0),
        }
    }
#___________________________________________________________
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
     'SMALL_PIVOT'   : (  922.5,  883.8,  920.3,  881.5),
     'SMALL_CONFIRM' : (  861.1,  824.2,  859.0,  822.1),
     'LARGE_PIVOT'   : (  930.0,  891.0,  927.7,  888.6),
     'LARGE_CONFIRM' : (  951.2,  910.4,  948.7,  907.7),
     }
#___________________________________________________________
PAD_HEIGHT = {
    'SMALL_PIVOT'   : (80.00, 80.12, 80.24, 80.37),
    'SMALL_CONFIRM' : (76.33, 76.45, 76.57, 76.69),
    'LARGE_PIVOT'   : (80.65, 80.77, 80.89, 81.01),
    'LARGE_CONFIRM' : (84.32, 84.44, 84.56, 84.69),
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
        'D0' : (  9,  8,  8,  7),
        'D1' : ( 11, 10, 11, 11),
        'D2' : ( 12, 13, 12, 13),
        'D3' : ( 13, 12, 13, 12),
        }
    }
#___________________________________________________________
PAD_COL_PHI0 = {
    'SMALL_PIVOT' : {
        'D0' : ( 0.002717, -0.040916, -0.002717, -0.046351),
        'D1' : ( 0.002717, -0.040916, -0.002717, -0.046351),
        'D2' : ( 0.002717, -0.062732, -0.002717, -0.068167),
        'D3' : ( 0.002717, -0.062732, -0.002717, -0.068167),
        },
    'SMALL_CONFIRM' : {
        'D0' : ( -0.019099, -0.062732, -0.024534, -0.068167),
        'D1' : ( -0.019099, -0.062732, -0.024534, -0.068167),
        'D2' : ( -0.030008, -0.095457, -0.035442, -0.100892),
        'D3' : ( -0.030008, -0.095457, -0.035442, -0.100892),
        },
    'LARGE_PIVOT' : {
        'D0' : ( 0.002717, -0.040916, -0.002717, -0.046351),
        'D1' : ( 0.002717, -0.040916, -0.002717, -0.046351),
        'D2' : ( 0.002717, -0.062732, -0.002717, -0.068167),
        'D3' : ( 0.002717, -0.062732, -0.002717, -0.068167),
        },
    'LARGE_CONFIRM' : {
        'D0' : ( -0.019099, -0.062732, -0.024534, -0.068167),
        'D1' : ( -0.019099, -0.062732, -0.024534, -0.068167),
        'D2' : ( -0.030008, -0.095457, -0.035442, -0.100892),
        'D3' : ( -0.030008, -0.095457, -0.035442, -0.100892),
        }
    }
#___________________________________________________________
Z_DANIEL = {
    'SMALL_PIVOT'   : ( 7407.5, 7418.8, 7430.2, 7441.5),
    'SMALL_CONFIRM' : ( 7067.5, 7078.8, 7090.2, 7101.5),
    'LARGE_PIVOT'   : ( 7467.5, 7478.8, 7490.2, 7501.5),
    'LARGE_CONFIRM' : ( 7807.5, 7818.8, 7830.2, 7841.5),
    }
#___________________________________________________________
Z_CURRENT_LAYOUT = {
    'SMALL_PIVOT'   : ( 7323.1, 7334.2, 7345.3, 7356.4),
    'SMALL_CONFIRM' : ( 7058.2, 7069.3, 7080.4, 7091.5),
    'LARGE_PIVOT'   : ( 7420.2, 7431.3, 7442.4, 7453.5),
    'LARGE_CONFIRM' : ( 7685.1, 7696.2, 7707.3, 7718.4),
    }
#___________________________________________________________
FIRST_PAD_ROW_DIVISION = { # currently not used
    'SMALL_PIVOT' : {
        'D0' : ( 2,  3,  2,  3),
        'D1' : (10, 10, 10, 10),
        'D2' : (21, 22, 21, 22),
        'D3' : (33, 34, 33, 34),
        },
    'SMALL_CONFIRM' : {
        'D0' : ( 3,  3,  3,  3),
        'D1' : (12, 12, 11, 11),
        'D2' : (23, 23, 23, 23),
        'D3' : (36, 36, 36, 36),
        },
    'LARGE_PIVOT' : {
        'D0' : ( 2,  2,  2,  2),
        'D1' : (10, 10,  9, 10),
        'D2' : (21, 21, 21, 21),
        'D3' : (34, 34, 34, 34),
        },
    'LARGE_CONFIRM' : {
        'D0' : ( 1,  2,  1,  2),
        'D1' : ( 9, 10,  9,  9),
        'D2' : (20, 20, 20, 20),
        'D3' : (32, 33, 32, 33),
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

def padRow0(wedgeType, layer) :
    return H_PAD_ROW_0[wedgeType][layer]

def padHeight(wedgeType, layer) :
    return PAD_HEIGHT[wedgeType][layer]

def padZsf(wedgeType, layer) : # temporary correction factor to account for the difference in Z pos
    return Z_CURRENT_LAYOUT[wedgeType][layer] / Z_DANIEL[wedgeType][layer]


def padRows(wedgeType, detectorNumber, layer) :
    return PAD_ROWS[wedgeType][detectorNumber2str(detectorNumber)][layer]

def padPhi0(wedgeType, detectorNumber, layer) :
    return PAD_COL_PHI0[wedgeType][detectorNumber2str(detectorNumber)][layer]

sectorDphi = 2.0*math.pi/16.

def midSectorPhi(sec) : return (sec-1)*sectorDphi # sector N starts from 1

#___________________________________________________________
