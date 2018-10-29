import pandas
import numpy as np

def diffCol(col, gvkey, step):
    diff = col.diff(periods=step).to_frame("colRaw")
    diff["gvkeyDiff"] = compustat["gvkey"].diff(periods=step)
    diff["col"] = diff.apply(lambda x: x["colRaw"] if x["gvkeyDiff"] == 0 else float("nan"), axis=1)
    return diff["col"]

""" ========= Profitability factors ========= """

# Import csv data
compustat = pandas.read_csv("Compustat19612018.csv")
crsp = pandas.read_csv("CRSP2007_2018.csv")

# GP
gp = compustat.revt - compustat.cogs
gpoa = gp / compustat["at"]

# ROE
be = (compustat.seq - compustat.pstk).fillna(compustat.ceq + compustat.pstk).fillna(compustat["at"] - compustat["lt"] + compustat["mibt"])
roe = compustat["ib"] / be

# ROA
roa = compustat["ib"] / compustat["at"]

# CFOA
wc = compustat["act"] - compustat["lct"] - compustat["che"] + compustat["dlc"] + compustat["txp"]
wcDiff = diffCol(wc, compustat["gvkey"], 1)
cf = compustat["ib"] + compustat["dp"] - wcDiff - compustat["capx"]
cfoa = cf / compustat["at"]

# GMAR
gmar = gp / compustat["sale"]

# ACC
acc = -wcDiff / compustat["at"]


""" ========= Growth Factors ====i===== """

# Store for calculating later
ib = compustat["ib"]
diffIb = diffCol(ib, compustat["gvkey"], 5)
diffGp = diffCol(gp, compustat["gvkey"], 5)
atShift = compustat["at"].shift(5)
ceqShift = compustat["ceq"].shift(5)

# Growth factors
delGpoa = diffGp / atShift
delRoe = diffIb / ceqShift
delRoa = diffIb / atShift
delCfoa = diffCol(cf, compustat["gvkey"], 5) / ceqShift
delGpoa = diffGp / ceqShift

