import asyncio
import pyppeteer
from pyppeteer import launch
import json
import os


class Team:
    """
    Replication of the javascript class with
    the same name defined at get_teams.js
    """
    def __init__(self, name, url):
        self.name = name.replace("'", r"\'")
        self.url = url.replace("'", r"\'")

teams_url = "https://www.baseball-reference.com/teams/"

async def load_js(jsfilename, page):
    with open(jsfilename, 'r') as f:
        content = f.read()
        return await page.evaluate(content)
    

async def get_teams_jsons(page):
    global teams_url
    if os.path.exists("activeteams.json") and\
       os.path.exists("inactiveteams.json") and\
       os.path.exists("nacionalteams.json"):
       return
    try:
        await page.goto(teams_url, {"timeout": 10*1000})
    except pyppeteer.errors.TimeoutError:
        await page.evaluate("window.stop()")
    teamsdict = await load_js("get_teams.js", page)
    with open('activeteams.json', 'w') as fp:
        json.dump(teamsdict["activeteams"], fp)
    with open('inactiveteams.json', 'w') as fp:
        json.dump(teamsdict["inactiveteams"], fp)
    with open('nacionalteams.json', 'w') as fp:
        json.dump(teamsdict["nacionalteams"], fp)
    

async def main():
    browser = await launch({"headless": False})
    page = await browser.newPage()
    await get_teams_jsons(page)
    await browser.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

"""
loop = asyncio.get_event_loop()
r = loop.run_until_complete

browser = r(launch())
page = r(browser.newPage())
r(page.goto('https://www.baseball-reference.com/teams/'))
teamsdict = r(load_js("get_teams.js", page))

with open('activeteams.json', 'w') as fp:
    json.dump(teamsdict["activeteams"], fp)


with open('inactiveteams.json', 'w') as fp:
    json.dump(teamsdict["inactiveteams"], fp)


with open('nacionalteams.json', 'w') as fp:
    json.dump(teamsdict["nacionalteams"], fp)

"""