import os
import shutil

import pandas as pd

class CSVManager():
    def __init__(self, filename, config, myLogger):
        self.config = config
        self.myLogger = myLogger
        self.filename = filename
        self.ndf = pd.read_excel(filename, converters={'default_code':str})
        self.df = self.ndf[["seller_ids/product_code", "seller_ids"]].copy()
        self.df = self.df[self.df["seller_ids"] == "PECOMARK SA"]
        self.df = self.df[pd.to_numeric(self.df["seller_ids/product_code"], errors='coerce').notnull()]
        self.savefile = config["savefile"]
        pass

    def get_refs(self):
        return self.df["seller_ids/product_code"]

    def append_row(self, *row):
        ref = str(int(row[0]))
        self.ndf.loc[self.ndf['seller_ids/product_code'] == ref, 'list_price'] = str(row[3]).replace(".", ",")
        self.ndf.loc[self.ndf['seller_ids/product_code'] == ref, 'standard_price'] = str(row[2]).replace(".", ",")
        self.ndf.loc[self.ndf['seller_ids/product_code'] == ref, 'seller_ids/price'] = str(row[2]).replace(".", ",")

    def saveCSV(self):
        self.ndf.to_csv(self.savefile, sep=";", mode="w+")

