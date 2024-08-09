import os
import shutil
import yaml
import logging
import logging.config

import pandas as pd

try:
    logConf = yaml.safe_load(open("./logging.yaml").read())
    logging.config.dictConfig(logConf)
except OSError as e:
    print("Imposible configurar el logger")
    print(e.filename)
else:
    myLogger = logging.getLogger(__name__)

class CSVManager:
    def __init__(self, filename, config, mode):
        self.mode = mode
        self.config = config
        self.myLogger = myLogger
        self.filename = filename
        self.ndf = pd.read_excel(filename, converters={'default_code': str, 'seller_ids/product_code': str})
        self.df = self.ndf[["seller_ids/product_code", "seller_ids"]].copy()
        self.df = self.df[pd.to_numeric(self.df["seller_ids/product_code"], errors='coerce').notnull()]
        self.savefile = config["savefile"]


    def check_defaults(self, preu, preu2, ref):
        preuant = float(self.ndf.loc[self.ndf['seller_ids/product_code'] == ref, 'standard_price'].iat[0])
        preu2ant = float(self.ndf.loc[self.ndf['seller_ids/product_code'] == ref, 'list_price'].iat[0])
        preu3ant = float(self.ndf.loc[self.ndf['seller_ids/product_code'] == ref, 'seller_ids/price'].iat[0])
        if preu != preuant or preu != preu3ant or preu2 != preu2ant:
            self.myLogger.info("Preu de producte " + str(ref) + " " + self.mode + " actualitzat. Standard_price i list_price nous: " + str(preu) + " " + str(preu2) + ". Preus antics: " + str(preuant) + " " + str(preu2ant) + ".")
            return True
        return False

    def get_refs(self, store):
        return self.df.loc[self.df["seller_ids"] == store, "seller_ids/product_code"]

    def append_row(self, *row):
        ref = str(int(row[0]))
        self.ndf.loc[self.ndf['seller_ids/product_code'] == ref, 'list_price'] = row[2]
        self.ndf.loc[self.ndf['seller_ids/product_code'] == ref, 'standard_price'] = row[1]
        self.ndf.loc[self.ndf['seller_ids/product_code'] == ref, 'seller_ids/price'] = row[1]

    def saveCSV(self):
        self.ndf.to_excel(self.savefile)

