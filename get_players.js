// https://www.baseball-reference.com/teams/

class Player
{
    constructor(name, url)
    {
        this.name = name;
        this.url = url;
    }
}


/*
    Ref: https://stackoverflow.com/users/3954175/jcc-sanabria
    https://stackoverflow.com/a/68330734/3562468
*/ 

//download (type_of = "text/plain", filename= "data.json") {
function downloadteamlist (teamslist, filename= "data.json", type_of = "application/json")
{
    let jsonArray = [];
    for (i in teamslist)
    {
        let curTeam = teamslist[i];
        let data = 
        {
            "name":curTeam.name,
            "url":curTeam.url
        };
        jsonArray.push(data);
    }

    let body = document.body;
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([JSON.stringify(jsonArray, null, 2)], {
        type: type_of
    }));
    a.setAttribute("download", filename);
    body.appendChild(a);
    a.click();
    body.removeChild(a);
}

// playertype must be either pitching or batting
function scrapplayer(playertype)
{
    function getQuery(playertype, playerindex)
    {
        if (playertype === "pitching")
        {
            query = [`#pitching_register > tbody > tr:nth-child(${playerindex}) > td.left > a`,
            `#pitching_register > tbody > tr:nth-child(${playerindex}) > td.left > strong > a`];
        }
        else if (playertype === "batting")
        {
            query = [`#batting_register > tbody > tr:nth-child(${playerindex}) > td:nth-child(2) > a`,
            `#batting_register > tbody > tr:nth-child(${playerindex}) > td:nth-child(2) > strong > a`];
            
        }
        else
        {
            throw new Error(`playertype must be either pitching or batting. (playertype: ${playertype})`);
        }
        return query
    }
    
    const maxTolerance = 10;
    let tolerance = maxTolerance;
    let players = [];
    let currentNode = 1;
    //Active franchises
    while (true)
    {
        if (tolerance <= 0)
        {
            console.log("Tolerance reached zero! Probably it is over.")
            break;
        }
        let queries = getQuery(playertype, currentNode);
        let curPlayer = "";
        for (let q = 0; q < queries.length; q++)
        {
            curPlayer = document.querySelector(queries[q]);
            if (curPlayer != null)
            {
                break;
            }
        }
        if (curPlayer == null)
        {
            tolerance--;        
        }
        else
        {
            tolerance = maxTolerance;
            let player = new Player(curPlayer.innerHTML, curPlayer.href);
            players.push(player);
        }
        currentNode++;
    }
    return players;
}

// var pitchingplayers = scrapplayer("pitching");

// downloadteamlist(pitchingplayers, "players_pitching.json");

// // The expression below will return to the console/python calling function.

// var dict = {
//     "pitchingplayers": pitchingplayers,
// };

// dict