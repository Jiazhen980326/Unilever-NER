import requests
import sqlite3
import config
import urllib
from database import DB, fetchMGDB

def dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

conn = sqlite3.connect(config.datapath)
conn.row_factory = dict_factory
cursor = conn.cursor()
q = 'SELECT context from entities'
data = cursor.execute(q).fetchall()
conn.close()
print([d['context'] for d in data])


# s = "Photodynamic therapy (PDT) has been widely used in tumor therapy due to its high spatial-temporal control and noninvasiveness. However, its clinical application is limited by weak efficacy, shallow tissue penetration, and phototoxicity. Herein, a facile theranostic nanoplatform based on photoswitchable lanthanide-doped nanoparticles was designed. Typically, these nanoparticles had UV-blue and 1525 nm emission upon 980 nm excitation and 1525 nm emission upon 800 nm excitation. We further used these nanoparticles for achieving real-time near-infrared (NIR)-IIb imaging (800 nm) with a high signal-to-noise ratio and imaging-guided PDT (980 nm). Moreover, such a photoswitchable nanoplatform capping with pH-sensitive calcium phosphate for coloading doxorubicin (a chemotherapeutic immunogenic cell death [ICD] inducer) and paramagnetic Mn2+ ions enhances T1-magnetic resonance imaging in the tumor microenvironment. Our results suggest that this theranostic nanoplatform could not only kill tumor cells directly through dual-modal image-guided PDT/chemotherapy but also inhibit distant tumor and lung metastasis through ICD. Therefore, it has great potential for clinical application ."

# Convert String To URL


# url = config.entity_extractor + '?document=' + urllib.parse.quote(s, safe='')
# res = requests.get(url).json()
# print(res)


# url = config.triple_extractor + '?document=' + urllib.parse.quote(s, safe='')
# res = requests.get(url).json()
# print(res)
# res = list({(e[0], e[1]): e for e in res}.values())

# print(res)
