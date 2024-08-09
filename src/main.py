import json
import logging
import logging.config
import os

import yaml

from BrowserManager import BrowserManager
from SoupEater import SoupEater
from CSVManager import CSVManager

''' Comprovació i generació de directoris necessaris '''
try:
    if not os.path.exists(os.path.join(os.getcwd(), "log")):
        os.makedirs(os.path.join(os.getcwd(), "log"))
except:
    print("Error durant les comprovacións inicials")
    raise

''' Configuració inicial del programa '''
try:
    with open("./config.json") as f:
        config = json.load(f)
except OSError as e:
    print("Fitxer de configuració absent")
    print(e.filename)
    raise
''' Comprovació de carpetes '''
if not os.path.exists(os.path.dirname(os.path.join(os.getcwd(), config["refFile"]))):
    os.makedirs(os.path.dirname(os.path.join(os.getcwd(), config["selfFile"])))
if not os.path.exists(os.path.dirname(os.path.join(os.getcwd(), config["savefile"]))):
    os.makedirs(os.path.dirname(os.path.join(os.getcwd(), config["savefile"])))
''' Logger '''
try:
    logConf = yaml.safe_load(open("./logging.yaml").read())
    logging.config.dictConfig(logConf)
except OSError as e:
    print("Imposible configurar el logger")
    print(e.filename)
else:
    myLogger = logging.getLogger(__name__)


def scraper(selection=None):
    mode = config[selection]
    br = BrowserManager(config)
    csvManager = CSVManager(config["refFile"], config, mode)
    web = config["webs"][mode]
    br.login(mode)
    eater = SoupEater()
    i = 0

    for store in csvManager.df["seller_ids"].unique():
        if selection is not None:
            if selection != store:
                continue
        products = csvManager.get_refs(store)
        for prod in products:
            i += 1
            myLogger.debug("Producte " + str(i) + "/" + str(len(products)))
            try:
                page = br.get(web["prod_url"] + str(prod))
                eater.prepare(prod, config["webs"][mode])
                eater.boil(page)
                preu, preu2 = eater.eat()
                save = csvManager.check_defaults(preu, preu2, str(prod))
                if save:
                    csvManager.append_row(str(prod), preu, preu2)
            except Exception as e:
                myLogger.debug("Producte no trobat", exc_info=True)
        br.logout()
    csvManager.saveCSV()


if __name__ == "__main__":
    while True:
        print("Actualització dels preus del catàleg de productes de Valls Climent\n"
              "1. Actualització de Pecomark.\n2. Actualització de Ohaus.\n"
              "9. Actualització universal\n"
              "10. Sortir")
        cmd = input("Comanda: ")
        if cmd == "1":
            scraper("PECOMARK SA")
        if cmd == "2":
            print("No implementat. Executant amb pecomark\n")
            scraper("PECOMARK SA")
        if cmd == "9":
            print("No implementat. Executant amb pecomark")
            scraper("PECOMARK SA")
        if cmd == "10":
            break
