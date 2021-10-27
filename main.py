import asyncio
import get_teams
import get_players
import json
from time import sleep
from tqdm import tqdm
import os

def load_team_jsons(jsonfiles):
    with open(jsonfiles, 'r') as f:
        team = json.load(f)
    return team



async def main():
    await get_teams.main() # Generates teams lists {activeteams,inactiveteams,nacionalteams}.json

    teamsfiles = [
        "activeteams",
        "inactiveteams",
        "nacionalteams"]
    teamsfiles = teamsfiles[1:]
    sleep_time = 15
    print(f"Sleeping {sleep_time} second between calls")
    for teamfile in teamsfiles:
        teams = load_team_jsons(teamfile + ".json")
        os.makedirs(teamfile, exist_ok=True)
        #os.chdir(teamfile)
        for team in tqdm(teams):
            team_name = team['name']
            team_name = team_name.replace("/", "-")
            team_url = team['url']
            output_file = f'{teamfile}/players_{team_name}_pitching.json'
            if not os.path.exists(output_file):
                print(f"getting {output_file}")
                await get_players.main(team_name, team_url, "pitching", output_dir=teamfile) # pitching players for 'team_url'
                sleep(sleep_time)
            output_file = f'{teamfile}/players_{team_name}_batting.json'
            if not os.path.exists(output_file):
                print(f"getting {output_file}")
                await get_players.main(team_name, team_url, "batting", output_dir=teamfile) # batting players for 'team_url'
                sleep(sleep_time)
        #break
        #os.chdir("..")
    pass

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())