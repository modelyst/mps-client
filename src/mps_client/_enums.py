#   Copyright 2022 Modelyst LLC
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import logging
from enum import Enum


class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

    def get_log_level(self):
        return getattr(logging, self)


class EntityType(str, Enum):
    PLATE = "plate"
    RUN = "run"
    ANALYSIS = "analysis"


class ColorMap(str, Enum):
    jet = "jet"
    viridis = "viridis"
    plasma = "plasma"
    inferno = "inferno"
    magma = "magma"
    cividis = "cividis"


class Fom(str, Enum):
    ETA_V_AVE = 'Eta.V_ave'
    ETA_V_FIN = 'Eta.V_fin'
    E_V_AVE = 'E.V_ave'
    E_V_FIN = 'E.V_fin'
    I_A_FIN = 'I.A_fin'
    I_A_AVE = 'I.A_ave'
    Q_C = 'Q.C'
    I_STD_DEV = "I.std_dev"
    I_A_MAX = "I.A_max"
    I_A_MIN = "I.A_min"
    ETA_V_ITHRESH = "Eta.V_Ithresh"
    E_V_ITHRESH = "E.V_Ithresh"

    def get_label(self) -> str:
        """Get matplotlib label for fom."""
        return self.value


class CompositionName(str, Enum):
    INTERP = 'interp'
    INKJET = 'inkjet'
    PLATE_MAP = 'platemap'
    XRFS = 'xrfs'


class GroupBy(str, Enum):
    MAX = 'max'
    MEAN = 'mean'
    MEDIAN = 'median'
    MIN = 'min'


class PlotType(str, Enum):
    tern = 'ternary'
    quatslice_5 = 'quatslice_5'
    quatslice_10 = 'quatslice_10'


class Element(str, Enum):
    """Element of the periodic table"""

    H = "H"
    He = "He"
    Li = "Li"
    Be = "Be"
    B = "B"
    C = "C"
    N = "N"
    O = "O"
    F = "F"
    Ne = "Ne"
    Na = "Na"
    Mg = "Mg"
    Al = "Al"
    Si = "Si"
    P = "P"
    S = "S"
    Cl = "Cl"
    Ar = "Ar"
    K = "K"
    Ca = "Ca"
    Sc = "Sc"
    Ti = "Ti"
    V = "V"
    Cr = "Cr"
    Mn = "Mn"
    Fe = "Fe"
    Co = "Co"
    Ni = "Ni"
    Cu = "Cu"
    Zn = "Zn"
    Ga = "Ga"
    Ge = "Ge"
    As = "As"
    Se = "Se"
    Br = "Br"
    Kr = "Kr"
    Rb = "Rb"
    Sr = "Sr"
    Y = "Y"
    Zr = "Zr"
    Nb = "Nb"
    Mo = "Mo"
    Tc = "Tc"
    Ru = "Ru"
    Rh = "Rh"
    Pd = "Pd"
    Ag = "Ag"
    Cd = "Cd"
    In = "In"
    Sn = "Sn"
    Sb = "Sb"
    Te = "Te"
    I = "I"
    Xe = "Xe"
    Cs = "Cs"
    Ba = "Ba"
    La = "La"
    Ce = "Ce"
    Pr = "Pr"
    Nd = "Nd"
    Pm = "Pm"
    Sm = "Sm"
    Eu = "Eu"
    Gd = "Gd"
    Tb = "Tb"
    Dy = "Dy"
    Ho = "Ho"
    Er = "Er"
    Tm = "Tm"
    Yb = "Yb"
    Lu = "Lu"
    Hf = "Hf"
    Ta = "Ta"
    W = "W"
    Re = "Re"
    Os = "Os"
    Ir = "Ir"
    Pt = "Pt"
    Au = "Au"
    Hg = "Hg"
    Tl = "Tl"
    Pb = "Pb"
    Bi = "Bi"
    Po = "Po"
    At = "At"
    Rn = "Rn"
    Fr = "Fr"
    Ra = "Ra"
    Ac = "Ac"
    Th = "Th"
    Pa = "Pa"
    U = "U"
    Np = "Np"
    Pu = "Pu"
    Am = "Am"
    Cm = "Cm"
    Bk = "Bk"
    Cf = "Cf"
    Es = "Es"
    Fm = "Fm"
    Md = "Md"
    No = "No"
    Lr = "Lr"
    Rf = "Rf"
    Db = "Db"
    Sg = "Sg"
    Bh = "Bh"
    Hs = "Hs"
    Mt = "Mt"
    Ds = "Ds"
    Rg = "Rg"
    Cn = "Cn"
    Nh = "Nh"
    Fl = "Fl"
    Mc = "Mc"
    Lv = "Lv"
    Ts = "Ts"
    Og = "Og"

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return repr(self.__str__())
