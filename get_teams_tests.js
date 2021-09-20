// https://www.baseball-reference.com/teams/

const maxTolerance = 10;
let tolerance = maxTolerance;
let currentNode = 1;

class Team
{
    constructor(name, url)
    {
        this.name = name;
        this.url = url;
    }
}

var activeteams = [];
var inactiveteams = [];
var nacionalteams = [];




//Active franchises
while (true)
{
    if (tolerance <= 0)
    {
        console.log("Tolerance reached zero! Probably it is over.")
        break;
    }
    let curTeam = $(`#teams_active > tbody > tr:nth-child(${currentNode}) > td.left > a`)
    if (curTeam == null)
    {
        tolerance--;        
    }
    else
    {
        tolerance = maxTolerance;
        let team = new Team(curTeam.innerHTML, curTeam.href);
        activeteams.push(team);
    }
    currentNode++;
}

currentNode = 1;
tolerance = maxTolerance;

//Inactive franchises
while (true)
{
    if (tolerance <= 0)
    {
        console.log("Tolerance reached zero! Probably it is over.")
        break;
    }
    let curTeam = $(`#teams_defunct > tbody > tr:nth-child(${currentNode}) > td.left > a`)
    if (curTeam == null)
    {
        tolerance--;        
    }
    else
    {
        tolerance = maxTolerance;
        let team = new Team(curTeam.innerHTML);
        inactiveteams.push(team);
    }
    currentNode++;
}

currentNode = 1;
tolerance = maxTolerance;

//Nacional Association franchises
while (true)
{
    if (tolerance <= 0)
    {
        console.log("Tolerance reached zero! Probably it is over.")
        break;
    }
    let curTeam = $(`#teams_na > tbody > tr:nth-child(${currentNode}) > td.left > a`)
    if (curTeam == null)
    {
        tolerance--;        
    }
    else
    {
        tolerance = maxTolerance;
        let team = new Team(curTeam.innerHTML);
        nacionalteams.push(team);
    }
    currentNode++;
}