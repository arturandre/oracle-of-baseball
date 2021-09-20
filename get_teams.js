// https://www.baseball-reference.com/teams/

class Team
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


function scrapfranchise(franchisename)
{
    const maxTolerance = 10;
    let tolerance = maxTolerance;
    let teams = [];
    let currentNode = 1;
    //Active franchises
    while (true)
    {
        if (tolerance <= 0)
        {
            console.log("Tolerance reached zero! Probably it is over.")
            break;
        }
        let curTeam = document.querySelector(`#${franchisename} > tbody > tr:nth-child(${currentNode}) > td.left > a`)
        if (curTeam == null)
        {
            tolerance--;        
        }
        else
        {
            tolerance = maxTolerance;
            let team = new Team(curTeam.innerHTML, curTeam.href);
            teams.push(team);
        }
        currentNode++;
    }
    return teams;
}

var activeteams = scrapfranchise("teams_active");
var inactiveteams = scrapfranchise("teams_defunct");
var nacionalteams = scrapfranchise("teams_na");

downloadteamlist(activeteams, "teams_active.json");
downloadteamlist(inactiveteams, "teams_defunct.json");
downloadteamlist(nacionalteams, "teams_na.json");

// The expression below will return to the console/python calling function.

var dict = {
    "activeteams": activeteams,
    "inactiveteams": inactiveteams,
    "nacionalteams": nacionalteams
};

dict