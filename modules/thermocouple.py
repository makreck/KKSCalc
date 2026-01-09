import math

class Thermocouple:
    # Polynomial thermocouple tables for converting mV into °C:

    pn_mV2C_Type_B1 = [
        +9.8423321e+1, +6.9971500e+2, -8.4765304e+2, +1.0052644e+3,
        -8.3345952e+2, +4.5508542e+2, -1.5523037e+2, +2.9886750e+1,
        -2.4742860e+0,
    ]

    pn_mV2C_Type_B2 = [
        +2.1315071e+2, +2.8510504e+2, -5.2742887e+1, +9.9160804e+0,
        -1.2965303e+0, +1.1195870e-1, -6.0625199e-3, +1.8661696e-4,
        -2.4878585e-6,
    ]

    pn_mV2C_Type_E1 = [
        +0.0,          +1.6977288e+1, -4.3514970e-1, -1.5859697e-1,
        -9.2502871e-2, -2.6084314e-2, -4.1360199e-3, -3.4034030e-4,
        -1.1564890e-5,
    ]

    pn_mV2C_Type_E2 = [
        +0.0,           +1.7057035e+1,  -2.3301759e-1,  +6.5435585e-3,
        -7.3562749e-5,  -1.7896001e-6,  +8.4036165e-8,  -1.3735879e-9,
        +1.0629823e-11, -3.2447087e-14,
    ]

    pn_mV2C_Type_J1 = [
        +0.0,          +1.9528268e+1, -1.2286185e+0, -1.0752178e+0,
        -5.9086933e-1, -1.7256713e-1, -2.8131513e-2, -2.3963370e-3,
        -8.3823321e-5,
    ]

    pn_mV2C_Type_J2 = [
        +0.0,       +1.978425e+1, -2.001204e-1, +1.036969e-2,
        -2.549687e-4,  +3.585153e-6, -5.344285e-8, +5.099890e-10,
    ]

    pn_mV2C_Type_J3 = [
        -3.11358187e+3, +3.00543684e+2, -9.94773230e+0, +1.70276630e-1,
        -1.43033468e-3, +4.73886084e-6,
    ]

    pn_mV2C_Type_K1 = [
        +0.0,       +2.5173462e+1, -1.1662878e+0, -1.0833638e+0,
        -8.9773540e-1, -3.7342377e-1, -8.6632643e-2, -1.0450598e-2,
        -5.1920577e-4,
    ]

    pn_mV2C_Type_K2 = [
        +0.0,      +2.508355e+1, +7.860106e-2, -2.503131e-1,
        +8.315270e-2,  -1.228034e-2, +9.804036e-4, -4.413030e-5,
        +1.057734e-6, -1.052755e-8,
    ]

    pn_mV2C_Type_K3 = [
        -1.318058e+2, +4.830222e+1, -1.646031e+0, +5.464731e-2,
        -9.650715e-4, +8.802193e-6, -3.110810e-8,
    ]

    pn_mV2C_Type_N1 = [
        +0.0,       +3.8436847e+1, +1.1010485e+0, +5.2229312e+0,
        +7.2060525e+0, +5.8488586e+0, +2.7754916e+0, +7.7075166e-1,
        +1.1582665e-1, +7.3138868e-3,
    ]

    pn_mV2C_Type_N2 = [
        +0.0,      +3.86896e+1, -1.08267e+0, +4.70205e-2,
        -2.12169e-6,   -1.17272e-4, +5.39280e-6, -7.98156e-8,
    ]

    pn_mV2C_Type_N3 = [
        +1.972485e+1,  +3.300943e+1, -3.915159e-1, +9.855391e-3,
        -1.274371e-4, +7.767022e-7,
    ]

    pn_mV2C_Type_R1 = [
        +0.0,       +1.8891380e+2, -9.3835290e+1, +1.3068619e+2,
        -2.2703580e+2, +3.5145659e+2, -3.8953900e+2, +2.8239471e+2,
        -1.2607281e+2, +3.1353611e+1, -3.3187769e+0,
    ]

    pn_mV2C_Type_R2 = [
        +1.334584505e+1, +1.472644573e+2, -1.844024844e+1, +4.031129726e+0,
        -6.249428360e-1, +6.468412046e-2, -4.458750426e-3, +1.994710149e-4,
        -5.313401790e-6, +6.481976217e-8,
    ]

    pn_mV2C_Type_R3 = [
        -8.199599416e+1, +1.553962042e+2, -8.342197663e+0, +4.279433549e-1,
        -1.191577910e-2, +1.492290091e-4,
    ]

    pn_mV2C_Type_R4 = [
        +3.406177836e+4, -7.023729171e+3, +5.582903813e+2, -1.952394635e+1,
        +2.560740231e-1,
    ]

    pn_mV2C_Type_S1 = [
        +0.0,        +1.84949460e+2, -8.00504062e+1, +1.02237430e+2,
        -1.52248592e+2, +1.88821343e+2, -1.59085941e+2, +8.23027880e+1,
        -2.34181944e+1, +2.79786260e+0,
    ]

    pn_mV2C_Type_S2 = [
        +1.291507177e+1, +1.466298863e+2, -1.534713402e+1, +3.145945973e+0,
        -4.163257839e-1, +3.187963771e-2, -1.291637500e-3, +2.183475087e-5,
        -1.447379511e-7, +8.211272125e-9,
    ]

    pn_mV2C_Type_S3 = [
        -8.087801117e+1, +1.621573104e+2, -8.536869453e+0, +4.719686976e-1,
        -1.441693666e-2, +2.081618890e-4,
    ]

    pn_mV2C_Type_S4 = [
        +5.333875126e+4, -1.235892298e+4, +1.092657613e+3, -4.265693686e+1,
        +6.247205420e-1,
    ]

    pn_mV2C_Type_T1 = [
    +0.0,       +2.5949192e+1, -2.1316967e-1, +7.9018692e-1,
    +4.2527777e-1, +1.3304473e-1, +2.0241446e-2, +1.2668171e-3,
    ]

    pn_mV2C_Type_T2 = [
    +0.0,       +2.592800e+1, -7.602961e-1, +4.637791e-2,
    -2.165394e-3,  +6.048144e-5, -7.293422e-7,
    ]

    # Polynomial Thermocouple tables for converting °C into thermo mV:

    pn_C2mV_Type_B1 = [
        +0.0,           -2.4650818346e-4,  +5.9040421171e-6,  -1.3257931636e-9,
        +1.5668291901e-12, -1.6944529240e-15, +6.2990347094e-19,
    ]

    pn_C2mV_Type_B2 = [
        -3.8938168621,     +2.8571747470e-2,  -8.4885104785e-5,  +1.5785280164e-7,
        -1.6835344864e-10, +1.1109794013e-13, -4.4515431033e-17, +9.8975640821e-21,
        -9.3791330289e-25,
    ]

    pn_C2mV_Type_E1 = [
        +0.0,              +5.8665508708e-2,  +4.5410977124e-5,  -7.7998048686e-7,
        -2.5800160843e-8,  -5.9452583057e-10, -9.3214058667e-12, -1.0287605534e-13,
        -8.0370123621e-16, -4.3979497391e-18, -1.6414776355e-20, -3.9673619516e-23,
        -5.5827328721e-26, -3.4657842013e-29,
    ]

    pn_C2mV_Type_E2 = [
        +0.0,           +5.8665508710e-2,  +4.5032275582e-5,  +2.8908407212e-8,
        -3.3056896652e-10, +6.5024403270e-13, -1.9197495504e-16, -1.2536600497e-18,
        +2.1489217569e-21, -1.4388041782e-24, +3.5960899481e-28,
    ]

    pn_C2mV_Type_J1 = [
        +0.0,           +5.0381187815e-2,  +3.0475836930e-5,  -8.5681065720e-8,
        +1.3228195295e-10, -1.7052958337e-13, +2.0948090697e-16, -1.2538395336e-19,
        +1.5631725697e-23,
    ]

    pn_C2mV_Type_J2 = [
        +2.9645625681e+2, -1.4976127786,      +3.1787103924e-3,  -3.1847686701e-6,
        +1.5720819004e-9, -3.0691369056e-13,
    ]

    pn_C2mV_Type_K1 = [
        +0.0,              +3.9450128025e-2,  +2.3622373598e-5,  -3.2858906784e-7,
        -4.9904828777e-9,  -6.7509059173e-11, -5.7410327428e-13, -3.1088872894e-15,
        -1.0451609365e-17, -1.9889266878e-20, -1.6322697486e-23,
    ]

    pn_C2mV_Type_K2 = [
        -1.7600413686e-2,  +3.8921204975e-2,  +1.8558770032e-5,  -9.9457592874e-8,
        +3.1840945719e-10, -5.6072844889e-13, +5.6075059059e-16, -3.2020720003e-19,
        +9.7151147152e-23, -1.2104721275e-26,
    ]

    pn_C2mV_Type_N1 = [
        +0.0,              +2.6159105962e-2,  +1.0957484228e-5,  -9.3841111554e-8,
        -4.6412039759e-11, -2.6303357716e-12, -2.2653438003e-14, -7.6089300791e-17,
        -9.3419667835e-20,
    ]

    pn_C2mV_Type_N2 = [
        +0.0,              +2.5929394601e-2,  +1.5710141880e-5,  +4.3825627237e-8,
        -2.5261169794e-10, +6.4311819339e-13, -1.0063471519e-15, +9.9745338992e-19,
        -6.0863245607e-22, +2.0849229339e-25, -3.0682196151e-29,
    ]

    pn_C2mV_Type_R1 = [
        +0.0,               +5.28961729765e-3,  +1.39166589782e-5,  -2.38855693017e-8,
        +3.56916001063e-11, -4.62347666298e-14, +5.00777441034e-17, -3.73105886191e-20,
        +1.57716482367e-23, -2.81038625251e-27,
    ]

    pn_C2mV_Type_R2 = [
        +2.95157925316,     -2.52061251332e-3,  +1.59564501865e-5,  -7.64085947576e-9,
        +2.05305291024e-12, -2.93359668173e-16,
    ]

    pn_C2mV_Type_R3 = [
        +1.52232118209e+2,  -2.68819888545e-1,  +1.71280280471e-4,  -3.45895706453e-8,
        -9.34633971046e-15,
    ]

    pn_C2mV_Type_S1 = [
        +0.0,               +5.40313308631e-3,  +1.25934289740e-5,  -2.32477968689e-8,
        +3.22028823036e-11, -3.31465196389e-14, +2.55744251786e-17, -1.25068871393e-20,
        +2.71443176145e-24,
    ]

    pn_C2mV_Type_S2 = [
        +1.32900444085,     +3.34509311344e-3,  +6.54805192818e-6,  -1.64856259209e-9,
        +1.29989605174e-14,
    ]

    pn_C2mV_Type_S3 = [
        +1.46628232636e+2,  -2.58430516752e-1,  +1.63693574641e-4,  -3.30439046987e-8,
        -9.43223690612e-15,
    ]

    pn_C2mV_Type_T1 = [
        +0.0000000000000,  +3.8748106364e-2,  +4.4194434347e-5,  +1.1844323105e-7,
        +2.0032973554e-8,  +9.0138019559e-10, +2.2651156593e-11, +3.6071154205e-13,
        +3.8493939883e-15, +2.8213521925e-17, +1.4251594779e-19, +4.8768662286e-22,
        +1.0795539270e-24, +1.3945027062e-27, +7.9795153927e-31,
    ]

    pn_C2mV_Type_T2 = [
        +0.0000000000000, +3.8748106364e-2,  +3.3292227880e-5,  +2.0618243404e-7,
        -2.1882256846e-9, +1.0996880928e-11, -3.0815758772e-14, +4.5479135290e-17,
        -2.7512901673e-20,
    ]

    typeSpecTable = {
        "Type_B": (    0.0, +1820.0 ),
        "Type_E": ( -270.0, +1000.0 ),
        "Type_J": ( -210.0, +1200.0 ),
        "Type_K": ( -270.0, +1300.0 ),
        "Type_N": ( -270.0, +1300.0 ),
        "Type_R": (  -50.0, +1768.0 ),
        "Type_S": (  -50.0, +1768.0 ),
        "Type_T": ( -270.0,  +400.0 ),
    }

    def __init__(self):
        pass

    # Returns a tuple of the valid temperature range for the given thermocouple type
    def get_TemperatureRange(thermoCoupleType: str) -> tuple:
        return Thermocouple.typeSpecTable.get(thermoCoupleType, ( 0.0, 0.0 ))

    # Method for calculation of a polynomial by the given factors:
    def polynomial(self, f: float, p: list):
        mul = 1.0
        sum = 0.0
        for factor in p:
            sum = sum + factor * mul
            mul = mul * f
        return sum

    # Returns the thermo voltage in mV from a given temperature in °C
    # regarding the given Thermocouple type:
    def mV_to_Celsius(thermoCoupleType,  mV):
        Celsius = 0.0

        match thermoCoupleType:
            case "Type_B":
                if (mV >= 0.291) and (mV <= 2.431):
                    Celsius = self.polynomial(mV, Thermocouple.pn_mV2C_Type_B1)
                else:
                    if (mV >= 2.431) and (mV <= 13.820):
                        Celsius = self.polynomial(mV, Thermocouple.pn_mV2C_Type_B2)

            case "Type_E":
                if (mV >= -8.825) and (mV <= 0.0):
                    Celsius = self.polynomial(mV, Thermocouple.pn_mV2C_Type_E1)
                else:
                    if (mV >= 0.0) and (mV <= 76.373):
                        Celsius = self.polynomial(mV, Thermocouple.pn_mV2C_Type_E2)

            case "Type_J":
                if (mV >= -8.095) and (mV <= 0.0):
                    Celsius = self.polynomial(mV, Thermocouple.pn_mV2C_Type_J1)
                else:
                    if (mV >= 0.0) and (mV <= 42.919):
                        Celsius = self.polynomial(mV, Thermocouple.pn_mV2C_Type_J2)
                    else:
                        if (mV >= 42.919) and (mV <= 69.553):
                            Celsius = self.polynomial(mV, Thermocouple.pn_mV2C_Type_J3)

            case "Type_K":
                if (mV >= -5.891) and (mV < 0.0):
                    Celsius = self.polynomial(mV, Thermocouple.pn_mV2C_Type_K1)
                else:
                    if (mV >= 0.0) and (mV < 20.644):
                        Celsius = self.polynomial(mV, Thermocouple.pn_mV2C_Type_K2)
                    else:
                        if (mV >= 20.644) and (mV <= 54.886):
                            Celsius = self.polynomial(mV, Thermocouple.pn_mV2C_Type_K3)

            case "Type_N":
                if (mV >= -3.990) and (mV < 0.0):
                    Celsius = self.polynomial(mV, Thermocouple.pn_mV2C_Type_N1)
                else:
                    if (mV >= 0.0) and (mV < 20.613):
                        Celsius = self.polynomial(mV, Thermocouple.pn_mV2C_Type_N2)
                    else:
                        if (mV >= 20.613) and (mV <= 47.513):
                            Celsius = self.polynomial(mV, Thermocouple.pn_mV2C_Type_N3)

            case "Type_R":
                if (mV >= -0.226) and (mV < 1.923):
                    Celsius = self.polynomial(mV, Thermocouple.pn_mV2C_Type_R1)
                else:
                    if (mV >= 1.923) and (mV < 13.228):
                        Celsius = self.polynomial(mV, Thermocouple.pn_mV2C_Type_R2)
                    else:
                        if (mV >= 11.361) and (mV < 19.739):
                            Celsius = self.polynomial(mV, Thermocouple.pn_mV2C_Type_R3)
                        else:
                            if (mV >= 19.739) and (mV <= 21.103):
                                Celsius = self.polynomial(mV, Thermocouple.pn_mV2C_Type_R4)

            case "Type_S":
                if (mV >= -0.235) and (mV < 1.874):
                    Celsius = self.polynomial(mV, Thermocouple.pn_mV2C_Type_S1)
                else:
                    if (mV >= 1.874) and (mV < 11.950):
                        Celsius = self.polynomial(mV, Thermocouple.pn_mV2C_Type_S2)
                    else:
                        if (mV >= 10.332) and (mV < 17.536):
                            Celsius = self.polynomial(mV, Thermocouple.pn_mV2C_Type_S3)
                        else:
                            if (mV >= 17.536) and (mV <= 18.693):
                                Celsius = self.polynomial(mV, Thermocouple.pn_mV2C_Type_S4)

            case "Type_T":
                if (mV >= -5.603) and (mV < 0.0):
                    Celsius = self.polynomial(mV, Thermocouple.pn_mV2C_Type_T1)
                else:
                    if (mV >= 0.0) and (mV <= 20.872):
                        Celsius = self.polynomial(mV, Thermocouple.pn_mV2C_Type_T2)
            case _:
                pass

        return Celsius

    # Returns temperature in °C from a given thermo voltage in mV
    # regarding the given Thermocouple type:
    def Celsius_to_mV(thermoCoupleType,  Celsius):
        mV = 0.0

        match thermoCoupleType:
            case "Type_B":
                if (Celsius >= 0.0) and (Celsius < 630.615):
                    mV = self.polynomial(Celsius, Thermocouple.pn_C2mV_Type_B1)
                else:
                    if (Celsius >= 630.615) and (Celsius <= 1820.0):
                        mV = self.polynomial(Celsius, Thermocouple.pn_C2mV_Type_B2)

            case "Type_E":
                if (Celsius >= -270.0) and (Celsius < 0.0):
                    mV = self.polynomial(Celsius, Thermocouple.pn_C2mV_Type_E1)
                else:
                    if (Celsius >= 0.0) and (Celsius <= 1000.0):
                        mV = self.polynomial(Celsius, Thermocouple.pn_C2mV_Type_E2)

            case "Type_J":
                if (Celsius >= -210.0) and (Celsius < 760.0):
                    mV = self.polynomial(Celsius, Thermocouple.pn_C2mV_Type_J1)
                else:
                    if (Celsius >= 760.0) and (Celsius < 1200.0):
                        mV = self.polynomial(Celsius, Thermocouple.pn_C2mV_Type_J2)

            case "Type_K":
                if (Celsius >= -270.0) and (Celsius <= 0.0):
                    mV = self.polynomial(Celsius, Thermocouple.pn_C2mV_Type_K1)
                else:
                    if (Celsius >= 0.0) and (Celsius <= 1372.0):
                        T2 = Celsius - 126.9686
                        T2 = (0.1185976 * math.exp(-0.0001183432 * (T2 * T2)))
                        mV = T2 + self.polynomial(Celsius, Thermocouple.pn_C2mV_Type_K2)

            case "Type_N":
                if (Celsius >= -270.0) and (Celsius <= 0.0):
                    mV = self.polynomial(Celsius, Thermocouple.pn_C2mV_Type_N1)
                else:
                    if (Celsius >= 0.0) and (Celsius <= 1372.0):
                        mV = self.polynomial(Celsius, Thermocouple.pn_C2mV_Type_N2)

            case "Type_R":
                if (Celsius >= -50.0) and (Celsius < 1064.18):
                    mV = self.polynomial(Celsius, Thermocouple.pn_C2mV_Type_R1)
                else:
                    if (Celsius >= 1064.18) and (Celsius < 1664.5):
                        mV = self.polynomial(Celsius, Thermocouple.pn_C2mV_Type_R2)
                    else:
                        if (Celsius >= 1664.5) and (Celsius <= 1768.1):
                            mV = self.polynomial(Celsius, Thermocouple.pn_C2mV_Type_R3)

            case "Type_S":
                if (Celsius >= -50.0) and (Celsius < 1064.18):
                    mV = self.polynomial(Celsius, Thermocouple.pn_C2mV_Type_S1)
                else:
                    if (Celsius >= 1064.18) and (Celsius < 1664.5):
                        mV = self.polynomial(Celsius, Thermocouple.pn_C2mV_Type_S2)
                    else:
                        if (Celsius >= 1664.5) and (Celsius <= 1768.1):
                            mV = self.polynomial(Celsius, Thermocouple.pn_C2mV_Type_S3)

            case "Type_T":
                if (Celsius >= -270.0) and (Celsius < 0.0):
                    mV = self.polynomial(Celsius, Thermocouple.pn_C2mV_Type_T1)
                else:
                    if (Celsius >= 0.0) and (Celsius <= 400.0):
                        mV = self.polynomial(Celsius, Thermocouple.pn_C2mV_Type_T2)

            case _:
                pass

        return (mV)
