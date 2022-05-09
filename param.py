
from collections import OrderedDict


" 80, 160 and 320 fC gain scenarios"
gain_parameters = OrderedDict()
gain_parameters[320] = (1915.0, 2.79, 0.0878)
gain_parameters[160] = (1045.0, 8.74, 0.0685)
gain_parameters[80] = (636.0, 15.6, 0.0328)

""" ileak parameters """
ileakParam_600V = [0.993, -42.668]
ileakParam_800V = [0.996, -42.464]
ileakParam = ileakParam_600V

""" CCE parameters """
#  line+log tdr 600V
cceParamFine_tdr600 = [1.5e15, -3.00394e-17, 0.318083]  # 120
cceParamThin_tdr600 = [1.5e15, -3.09878e-16, 0.211207]  # 200
cceParamThick_tdr600 = [6e14, -7.96539e-16, 0.251751]  # 300
#  line+log tdr 800V
cceParamFine_tdr800 = [4.2e15, 2.35482e-18, 0.553187]  # 120
cceParamThin_tdr800 = [1.5e15, -1.98109e-16, 0.280567]  # 200
cceParamThick_tdr800 = [6e14, -5.24999e-16, 0.357616]  # 300
#  line+log ttu 600V
cceParamFine_ttu600 = [1.5e15, 9.98631e-18, 0.343774]  # 120
cceParamThin_ttu600 = [1.5e15, -2.17083e-16, 0.304873]  # 200
cceParamThick_ttu600 = [6e14, -8.01557e-16, 0.157375]  # 300
#  line+log ttu 800V
cceParamFine_ttu800 = [1.5e15, 3.35246e-17, 0.251679]  # 120
cceParamThin_ttu800 = [1.5e15, -1.62096e-16, 0.293828]  # 200
cceParamThick_ttu800 = [6e14, -5.95259e-16, 0.183929]  # 300
# scaling the ddfz curve to match Timo's 800V measuremetn at 3.5E15
cceParamFine_epi800 = [3.5e15, -1.4285714e-17, 0.263812]  # 120
#  line+log tdr 600V EPI
cceParamFine_epi600 = [
    3.5e15,
    -3.428571e-17,
    0.263812,
]  # 120 - scaling the ddfz curve to match Timo's 600V measurement at 3.5E15
cceParamThin_epi600 = [1.5e15, -3.09878e-16, 0.211207]  # 200
cceParamThick_epi600 = [6e14, -7.96539e-16, 0.251751]  # 300

# epi 100 um in DN2019_045_v2
cceParamFine100_epi600 = [
    3.5e15,
    -0.00973872e-16,
    0.263812,
]  # 100 - # epi 100 um in DN2019_045_v2

# epi 80 um ## just a guess!
cceParamFine80_epi600 = [
    5.5e15,
    -0.00973872e-16,
    0.263812,
]
