GHSMIN = 20

MDSWITCH = {"JFM": "0215", "AMJ": "0515", "JAS": "0815", "OND": "1115"}

START_YEAR = 2007
END_YEAR = 2020

encoding_sig0 = {
    "sig0": {"dtype": "float32", "zlib": True, "complevel": 7},
    "time": {"dtype": "int32", "units": "days since 2007-01-01 00:00:00"},
}

encoding_sig0std = {
    "sig0std": {"dtype": "float32", "zlib": True, "complevel": 7},
    "time": {"dtype": "int32", "units": "days since 2007-01-01 00:00:00"},
}
