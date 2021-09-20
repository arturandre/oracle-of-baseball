import asyncio
from pyppeteer import launch
import json
import argparse
import os

class Player:
    def __init__(self, name, url, team_name):
        self.name = name.replace("'", r"\'")
        self.url = url.replace("'", r"\'")
        self.team_name = team_name.replace("'", r"\'")



async def load_js(jsfilename, page):
    with open(jsfilename, 'r') as f:
        content = f.read()
        return await page.evaluate(content)
    

async def get_players_jsons(page, team_name, team_url, playertype="pitching"):
    """
    playertype must be either 'pitching' or 'batting'
    """
    output_filename = f'players_{team_name}_{playertype}.json'
    if os.path.exists(output_filename):
        return
    if playertype == "pitching":
        team_url = team_url + "pitch.shtml"
    elif  playertype == "batting":
        team_url = team_url + "bat.shtml"
    else:
        raise Exception("playertype must be either 'pitching' or 'batting'.")
    await page.goto(team_url)
    await load_js("get_players.js", page)
    playerslist = await page.evaluate(f'scrapplayer("{playertype}")')
    with open(output_filename, 'w') as fp:
        json.dump(playerslist, fp)
    
    

async def main(team_name, team_url, player_type):
    browser = await launch()
    page = await browser.newPage()
    await get_players_jsons(page, team_name, team_url, player_type)
    await browser.close()

if __name__ == "__main__":
    team_url = "https://www.baseball-reference.com/teams/ARI/"
    player_type = "pitching"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(team_name=team_url, player_type=player_type))

"""
loop = asyncio.get_event_loop()
r = loop.run_until_complete

browser = r(launch())
page = r(browser.newPage())
r(page.goto(team_url_pitch))
r(load_js("get_players.js", page))

with open('activeteams.json', 'w') as fp:
    json.dump(teamsdict["activeteams"], fp)


with open('inactiveteams.json', 'w') as fp:
    json.dump(teamsdict["inactiveteams"], fp)


with open('nacionalteams.json', 'w') as fp:
    json.dump(teamsdict["nacionalteams"], fp)

"""