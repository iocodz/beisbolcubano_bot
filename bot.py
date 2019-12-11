from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from env import API_KEY
from bs4 import BeautifulSoup as bso

import requests
from functools import wraps


def getSoup():
    url = 'http://www.beisbolcubano.cu/'
    html = requests.get(url)
    soup = bso(html.text, 'lxml')

    return soup


def getResultsToday():
    soup = getSoup()
    data = soup.find_all('div', {"id": "MainContent_ctl01_UC_MDS_UpdatePanel"})
    runs = data[0].find_all('span', {"class": "Mini_DayScore_Runs"})
    siglas = soup.find_all('span', {"class": "Mini_DayScore_Siglas"})

    results = ''

    for i in range(0 , len(runs), 2):
        results += ('%s %s - %s %s\n' % (siglas[i].text, runs[i].text, siglas[i + 1].text, runs[i + 1].text))

    return results


def getTabla():
    soup = getSoup()
    data = soup.find_all('h5', {"class": "h5_margin_top"})
    teams = soup.find_all('span', {"style": "position:absolute; margin:13px 0 0 5px;"})

    tabla = ''
    amount_teams = len(teams)
    for i in range(amount_teams):
        tabla += ('%s. %s - %s - %s - %s\n' % (i + 1, teams[i].text, data[(i + 1) * amount_teams].text, data[(i + 1) * amount_teams + 1].text, data[(i + 1) * amount_teams + 2].text))

    return tabla


def getLideresIndividuales():
    soup = getSoup()
    nombres = soup.find_all('a', {"style": "margin-left: -15px; padding: 0; font-size: 15px; color: black;"})
    departamento = soup.find_all('span', {"class": "lideres_widget_AAA_span"})
    estadistica = soup.find_all('span', {"class": "lideres_widget_000_span"})

    lideres = ''

    for i in range(0, len(nombres)):
        lideres += ('%s - %s %s \n' % (nombres[i].text, departamento[i].text, estadistica[i].text))

    return lideres


def tabla(bot, update):
    chat_id = update.message.chat_id

    tabla = getTabla()
    bot.send_message(chat_id=chat_id, text=tabla)


def resultados(bot, update):
    chat_id = update.message.chat_id
    
    results = getResultsToday()

    bot.send_message(chat_id=chat_id, text=results)
    bot.send_message(chat_id=chat_id, text='Si no aparecen los resultados completos pude que no se hallan celebrado los partidos aún.')


def lideres(bot, update):
    chat_id = update.message.chat_id

    lideres = getLideresIndividuales()

    bot.send_message(chat_id=chat_id, text=lideres)

def main():
    updater = Updater(API_KEY)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('tabla', tabla))
    dp.add_handler(CommandHandler('resultados', resultados))
    dp.add_handler(CommandHandler('lideres', lideres))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

