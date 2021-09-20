from neo4j import GraphDatabase
from get_teams import Team
from get_players import Player
import json

class Neo4jConnector:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def connect_teammates(self):
        with self.driver.session() as session:
            statement_ok = session.write_transaction(self._connect_teammates)
            if statement_ok:
                print(f"Teammates connected in a complete graph.")
            else:
                print(f"Something went wrong while connecting teammates! Try to use the browser app.")

    @staticmethod
    def _connect_teammates(tx, team):
        tx.run(f"MATCH (p1:Player)-[]->(t:Team)<-[]-(p2:Player) "
            f"MERGE (p1)-[r:teammate]->(p2)")
        return True

    def create_and_return_team(self, team):
        with self.driver.session() as session:
            created_team = session.write_transaction(self._create_and_return_team, team)
            print(f"Created team: {created_team}")

    @staticmethod
    def _create_and_return_team(tx, team):
        result = tx.run(f"MERGE (a:Team {{name: '{team.name}', url: '{team.url}'}}) "
                        f"RETURN a.name + ' - ' + a.url")
        return result.single()[0]

    def create_and_return_player(self, player):
        with self.driver.session() as session:
            created_player = session.write_transaction(self._create_and_return_player, player)
            print(f"Created player: {created_player}, with team: {player.team_name}")

    @staticmethod
    def _create_and_return_player(tx, player):
        result = tx.run(f"MERGE (a:Player {{name: '{player.name}', url: '{player.url}'}})"
                        #f"ON CREATE SET a.teams_count = 1"
                        #f"ON MATCH SET a.teams_count = a.teams_count+1"
                        #f"RETURN a.name + ' - ' + a.url + ' - ' + a.teams_count")
                        f"RETURN a.name + ' - ' + a.url")
        # Relationship with the team
        tx.run(f"MATCH (a:Player), (t:Team)"
               f"WHERE a.name = '{player.name}'"
               f"AND t.name = '{player.team_name}'"
               f"MERGE (a)-[r:plays]->(t)")
        return result.single()[0]


if __name__ == "__main__":
    db = Neo4jConnector("bolt://localhost:7688", "neo4j", "1234")

    with open("activeteams.json", 'r') as f:
        teams_json_list = json.load(f)
        for team in teams_json_list:
            team_obj = Team(team['name'], team['url'])
            db.create_and_return_team(team_obj)
            #with open(f"activeteams/players_{team_obj.name}_pitching.json") as f2:
            with open(f"activeteams/players_{team_obj.name}_batting.json") as f2:
                players_json_list = json.load(f2)
                for player in players_json_list:
                    player_obj = Player(
                        name=player['name'],
                        url=player['url'],
                        team_name=team_obj.name)
                    db.create_and_return_player(player_obj)
    db.close()