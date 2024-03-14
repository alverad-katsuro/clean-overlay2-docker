#!/bin/python
import os
import shutil
import json

pastasSemTratar = os.popen(
    """docker container ls -aq | xargs docker inspect | jq '[.[]|{name:.Name,image:.Id,layers:([.GraphDriver.Data[]|split(":")]|flatten)}]'""").read()

pastasSemTratar = json.loads(pastasSemTratar)

pastasNaoExcluir = []

for t in pastasSemTratar:
    pastasNaoExcluir = pastasNaoExcluir + t['layers']


pastasNaoExcluir2 = []

for pn in pastasNaoExcluir:
    pn = pn.replace("/var/lib/docker/overlay2/", "")
    pastasNaoExcluir2.append(pn.split("/")[0])

pastasNaoExcluir2.append("l") # Dot remove the l folder with links of docker images
pastasNaoExcluir2.append("L") # Dot remove the l folder with links of docker images


for pasta in os.listdir("/var/lib/docker/overlay2"):
    if (pasta not in pastasNaoExcluir2):
        print(f"\033[92m Excluindo a pasta {pasta}")
        try:
            if os.path.isdir(f"/var/lib/docker/overlay2/{pasta}"):
                shutil.rmtree(f"/var/lib/docker/overlay2/{pasta}")
            else:
                os.remove(f"/var/lib/docker/overlay2/{pasta}")
        except:
            print(f"\033[91m Deu ruim não era para excluir a pasta {pasta}")
    else:
        print(f"\033[93m Não posso excluir a pasta {pasta}")
