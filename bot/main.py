"""A bot that synchronizes with the PREP, generates a table, a figure and posts them to Reddit."""

import os
from datetime import datetime, timedelta

# Uncomment the following 2 lines if you are running this bot on a VPS.
# import matplotlib
# matplotlib.use("agg")

import matplotlib.pyplot as plt

import imgur
import prep
import reddit


def create_folder(folder_name):
    """Creates a folder if it doesn't exist.

    Parameters
    ----------
    folder_name : str
        The name of the folder to be created.

    """

    try:
        os.makedirs(folder_name)
    except FileExistsError:
        pass


def init_bot():
    """Inits the bot."""

    prep_data = prep.get_prep(NOW.timestamp())

    explodes = list()
    results_table = ""

    for index, candidate in enumerate(prep_data["candidates"]):

        candidate_votes = prep_data["votes"][index]
        candidate_percentage = prep_data["percentages"][index]

        # We check if the current candidate has the most votes. If so we format it in bold letters.
        if candidate_votes == max(prep_data["votes"]):
            explodes.append(0.1)
            results_table += "**{}** | **{:,}** | **{}%**\n".format(
                candidate, candidate_votes, candidate_percentage)
        else:
            explodes.append(0.0)
            results_table += "{} | {:,} | {}%\n".format(
                candidate, candidate_votes, candidate_percentage)

    # We create the pie plot by using a dark style.
    plt.style.use("dark_background")

    patches, texts, autotexts = plt.pie(
        prep_data["percentages"], explode=explodes, colors=prep_data["colors"], autopct="%1.2f%%", startangle=90)

    plt.axis("equal")

    plt.legend(patches, prep_data["candidates"], bbox_to_anchor=(1, 0.5),
               loc="center right", bbox_transform=plt.gcf().transFigure)

    plt.title("Elecciones Presidenciales 2018")

    plt.figtext(.5, 0, "Última actualización: {:%d-%m-%Y a las %H:%M:%S}".format(
        NOW), fontsize=12, va="baseline", ha="center")

    plt.subplots_adjust(left=0.0, bottom=0.1, right=0.45)
    plt.draw()

    # Once our plot has been drawn, we save it and prepare it for upload to Imgur.
    fig_path = "./figs/{}.png".format(int(NOW.timestamp()))
    plt.savefig(fig_path)

    image_link = imgur.upload_image(NOW, fig_path)

    # We start the Reddit Markdown message with a header.
    message = "Elecciones Presidenciales 2018.\n\nSe sincroniza cada 15 minutos.\n\n"

    # We add the results table.
    message += """Candidato | Votos | Porcentaje\n--|--|--\n"""
    message += results_table

    # We add additional metadata.
    message += "\nTotal de Votos: {:,} | Actas Computadas: {}%\n".format(
        prep_data["totalVotos"], prep_data["actasCapturadas"])

    # We add the Imgur URL.
    message += "## [Resultados en Gráfica]({})\n".format(image_link)

    # We add the footer which includes the latest formatted date.
    message += "*****\n^Última ^sincronización: ^{:%d-%m-%Y ^a ^las ^%H:%M:%S}".format(
        NOW)

    # Finally, we send it all to a Reddit post.
    reddit.update_post(message)


if __name__ == "__main__":

    # Feel free to remove the timedelta part if you are in the CST timezone.
    NOW = datetime.now() - timedelta(hours=5)

    create_folder("figs")
    create_folder("raw_data")

    init_bot()
