import numpy as np
import matplotlib.pyplot as plt
from sensor import *
from param import *


epi120 = Sensor("epi", 120, 0.5, cceParamFine_epi600, ileakParam_600V)
epi100 = Sensor("epi", 100, 0.5, cceParamFine100_epi600, ileakParam_600V)
epi80 = Sensor("epi", 80, 0.5, cceParamFine80_epi600, ileakParam_600V)

sensors = []
sensors.append(epi120)
sensors.append(epi100)
sensors.append(epi80)


plots = [
    {
        "name": "cce",
        "title_y": "Charge Collection Eff.",
        "yscale": "linear",
        "leg_loc": "lower left",
    },
    {
        "name": "signal",
        "title_y": "Signal [fC]",
        "yscale": "linear",
        "leg_loc": "lower left",
    },
    {
        "name": "ileak",
        "title_y": r"$I_{leak} [\mu A]$",
        "yscale": "log",
        "leg_loc": "upper left",
    },
    {
        "name": "capacitance",
        "title_y": "Capacitance [pF]",
        "ymin": 20,
        "ymax": 120,
        "yscale": "linear",
        "leg_loc": "upper left",
    },
    {
        "name": "encs",
        "title_y": r"$ENC_{s}$ [fC]",
        "ymin": 0,
        "ymax": 1,
        "yscale": "linear",
        "leg_loc": "upper left",
    },
    {
        "name": "sadc",
        "title_y": "S [ADC counts]",
        "yscale": "linear",
        "leg_loc": "lower left",
    },
    {
        "name": "encp",
        "title_y": r"$ENC_{p}$ [fC]",
        "ymin": 0,
        "ymax": 1,
        "yscale": "linear",
        "leg_loc": "upper left",
    },
    {
        "name": "noise",
        "title_y": "Noise [fC]",
        "ymin": 0,
        "ymax": 1,
        "yscale": "linear",
        "leg_loc": "upper left",
    },
    {
        "name": "sn",
        "title_y": "S/N",
        "yscale": "linear",
        "leg_loc": "lower left",
    },
]

nose_flumax = 2.5e16
hgcal_flumax = 0.75e16

xt_hfn = 0.7675
xt_hgc = 0.6527


plt.rcParams.update({"font.size": 15})

fluence = np.logspace(13, 17, 100)

for plot in plots:
    plot["plot"] = plt.subplots()

for s in sensors:
    cce = s.get_cce_cmssw(fluence, *s.cce_param)
    signal = s.get_s(cce)
    ileak = s.get_ileak(fluence)
    capacitance = s.get_capacitance(fluence)
    encs = s.get_encs_cmssw(ileak)
    # encs = get_encs_an(ileak)
    sadc = s.get_s_adc(signal)
    encp = s.get_encp(signal, capacitance)
    noise = s.get_encn(encs, encp)
    sn = s.get_sn(signal, noise)

    ## take ax
    for plot in plots:
        varname = plot["name"]
        array_y = globals()[varname]
        ax = plot["plot"][1]
        linestyle = "solid"
        if s.d == 80:
            linestyle = "dotted"
        ax.plot(fluence, array_y, linestyle=linestyle, label="{}".format(s.label))

for plot in plots:
    fig = plot["plot"][0]
    ax = plot["plot"][1]

    ax.axvline(x=nose_flumax, linestyle="dashed", color="red", linewidth=2.0)
    ax.axvline(x=hgcal_flumax, linestyle="dashed", color="gray", linewidth=2.0)
    # ax.text(nose_text_x, 0, "HF-Nose", rotation=90, color="red")
    # ax.text(hgcal_text_x, 0, "HGCAL", rotation=90, color="gray")

    yt = 0.025
    hal = "bottom"
    if "enc" in plot["name"]:
        yt = 1 - yt
        hal = "top"

    ax.text(
        xt_hfn,
        yt,
        "HF-Nose",
        rotation=90,
        color="red",
        transform=ax.transAxes,
        verticalalignment=hal,
    )
    ax.text(
        xt_hgc,
        yt,
        "HGCAL",
        rotation=90,
        color="gray",
        transform=ax.transAxes,
        verticalalignment=hal,
    )
    # ax.text(x=nose_flumax,0,'HF-Nose',rotation=90)

    ax.legend(loc=plot["leg_loc"], frameon=False)
    ax.set_xlabel(r"f [$n_{eq}/cm^2$]")
    ax.set_ylabel(plot["title_y"])
    ax.grid(linestyle="dashed")

    if "ymin" in plot and "ymax" in plot:
        ax.set_ylim(plot["ymin"], plot["ymax"])
    ax.set_xscale("log")
    ax.set_yscale(plot["yscale"])
    fig.tight_layout()
    fig.savefig("figs/{}.pdf".format(plot["name"]))
    fig.savefig("figs/{}.png".format(plot["name"]))
