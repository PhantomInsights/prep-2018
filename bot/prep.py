"""This module connects to the PREP website, gets the latest JSON file and extracts what we need."""

import requests


def get_prep(file_name):
    """Gets a JSON file from the PREP, saves it and extracts required data to a dict.

    Parameters
    ----------
    file_name : str
        The name of the file used for the log.

    Returns
    -------
    dict
        A dictionary containing all the data we will require for the plot and the table.

    """

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0"}

    url = "https://rp18.ine.mx/assets/JSON/PRESIDENTE/NACIONAL/Presidente_NACIONAL.json"

    with requests.get(url, headers=headers) as response:

        # Save a copy for future analysis.
        with open("./raw_data/{}.json".format(file_name), "w", encoding="utf-8") as temp_file:
            temp_file.write(response.text)

        candidates = list()
        percentages = list()
        votes = list()
        colors = list()

        json_data = response.json()

        for item in json_data["votosCandidatoPartidoCoalicion"]:

            name = item["nombreCandidatoPropietario"]

            if item["siglasPartido"] == "CNR":
                name = "Candidatos No Registrados"

            if item["siglasPartido"] == "VN":
                name = "Nulos"

            color = "#{}".format(item["colorPartido"])
            colors.append(color)

            candidates.append(name)
            percentages.append(float(item["porcentaje"]))
            votes.append(int(item["total"]))

        return dict({"candidates": candidates, "percentages": percentages,
                     "votes": votes, "colors": colors, "totalVotos": json_data["totalVotos"],
                     "actasCapturadas": json_data["actasCapturadas"]["porcentaje"]})
