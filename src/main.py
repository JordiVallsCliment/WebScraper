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


if __name__ == "__main__":
    res = []
    br = BrowserManager(config, myLogger)
    csvManager = CSVManager(config["refFile"], config, myLogger)
    web = config["webs"]["pecomark"]
    login = br.login("pecomark")
    eater = SoupEater()
    i = 0
    products = csvManager.get_refs()
    for prod in products:
        i += 1
        myLogger.info("Producte " + str(i) + "/" + str(len(products)))
        try:
            page = br.get(web["prod_url"] + str(prod))
            eater.prepare(prod, config["webs"]["pecomark"])
            eater.boil(page)
            name, preu, preu2 = eater.eat()
            csvManager.append_row(str(prod), name, preu, preu2)
        except:
            myLogger.error("Producte no trobat", exc_info=True)
    br.logout()
    csvManager.saveCSV()

