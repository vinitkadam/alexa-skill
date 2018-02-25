from src import app
from flask import Flask, request, redirect, make_response, render_template
from flask_ask import Ask, statement, question, session
import requests
import json



ask = Ask(app, "/ipl")





url = "https://data.julep91.hasura-app.io/v1/query"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer db710c4b45facbfb0b422a58888bd7bf7b64781b1cbbfa1e"
}
query_match_result = '''{{
    "type": "select",
    "args": {{
        "table": "matches",
        "columns": [
            "winner"
        ],
        "where": {{
            "team1": {{
                "$eq": "{}"
            }},
            "team2": {{
                "$eq": "{}"
            }},
            "date":{{
                "$eq": "{}"
            }}
        }}
    }}
}}'''

query_mom = '''{{
    "type": "select",
    "args": {{
        "table": "matches",
        "columns": [
            "team1",
            "team2",
            "player_of_match"
        ],
        "where": {{
            "date": {{
                "$eq": "{}"
            }}
        }}
    }}
}}'''
query_summary='''{{
    "type": "select",
    "args": {{
        "table": "matches",
        "columns": [
            "team1",
            "team2",
            "venue",
            "city",
            "toss_winner",
            "toss_decision",
            "winner",
            "win_by_runs",
            "win_by_wickets",
            "player_of_match"
        ],
        "where": {{
            "date": {{
                "$eq": "{}"
            }}
        }}
    }}
}}
'''
query_final = '''
{{
    "type": "select",
    "args": {{
        "table": "ipl_finals",
        "columns": [
            "match_id"
        ],
        "where": {{
            "season": {{
                "$eq": "{}"
            }}
            
        }}
    }}
}}
'''
query_by_id='''{{
    "type": "select",
    "args": {{
        "table": "matches",
        "columns": [
            "team1",
            "team2",
            "winner",
            "win_by_runs",
            "win_by_wickets"
        ],
        "where": {{
            "id": {{
                "$eq": "{}"
            }}
            
        }}
    }}
}}'''

teams_mapping = {'rcb':'Royal Challengers Bangalore', 'bangalore':'Royal Challengers Bangalore', 'royal challengers bangalore': 'Royal Challengers Bangalore',
'mi':'Mumbai Indians', 'mumbai':'Mumbai Indians', 'mumbai indians': 'Mumbai Indians',
'hyderabad':'Sunrisers Hyderabad', 'srh':'Sunrisers Hyderabad','sunrisers hyderabad':'Sunrisers Hyderabad', 'sunrisers':'Sunrisers Hyderabad',
'csk':'Chennai Super Kings','chennai':'Chennai Super Kings', 'chennai super kings':'Chennai Super Kings',
'kxip':'Kings XI Punjab', 'punjab':'Kings XI Punjab','kings eleven punjab':'Kings XI Punjab',
'rps':'Rising Pune Supergiant', 'pune':'Rising Pune Supergiant','rising pune supergiant':'Rising Pune Supergiant',
'gujrat':'Gujarat Lions','gujarat':'Gujarat Lions','gl':'Gujarat Lions', 'gujarat lions':'Gujarat Lions',
'kkr':'Kolkata Knight Riders', 'kolkata':'Kolkata Knight Riders', 'knight riders':'Kolkata Knight Riders','kolkata knight riders':'Kolkata Knight Riders',
'rajasthan':'Rajasthan Royals', 'rr':'Rajasthan Royals','rajasthan royals':'Rajasthan Royals',
'delhi':'Delhi Daredevils', 'daredevils':'Delhi Daredevils', 'dd':'Delhi Daredevils','delhi daredevils':'Delhi Daredevils'
}
seasons={"2008":2008,"1":2008,"2009":2009,"2":2009,"2010":2010,"3":2010,"2011":2011,"4":2011,"2012":2012,"5":2012,"2013":2013,"6":2013,"2014":2014,"7":2014,"2015":2015,
"8":2015,"2016":2016,"9":2016,"2017":2017,"10":2017}
@app.route('/')
def homepage():
    return "Alexa skill is running."

@ask.launch
def welcome():
	welcome_msg = render_template('welcome')
	return question(welcome_msg)

@ask.intent("MatchResult")
def match_result(teamA,teamB,date_of_match):
	try:
		teamA=teamA.lower()
		teamB=teamB.lower()
		teamA = teams_mapping[teamA]
		teamB = teams_mapping[teamB]
	except:
		teamA=None
		teamB=None	
	requestPayload = query_match_result.format(teamA,teamB,date_of_match)
	resp = requests.request("POST", url, data=(requestPayload), headers=headers)
	result = json.loads(resp.content)
	if len(result) == 0:
		teamA,teamB = teamB,teamA
		requestPayload = query_match_result.format(teamA,teamB,date_of_match)
		resp = requests.request("POST", url, data=(requestPayload), headers=headers)
		result = json.loads(resp.content)
		if len(result) == 0:
			return statement('Sorry I could not find any result for your query. Please try again')
	else:
		winner = result[0]['winner']
		return question('You have queried about the match between {} and team {} that took place on {}. The winner of the match was {}'.format(teamA,teamB,date_of_match, winner))

    
@ask.intent("MOMatch")
def mom(date_of_match):
	requestPayload = query_mom.format(date_of_match)
	resp = requests.request("POST", url, data=(requestPayload), headers=headers)
	result = json.loads(resp.content)
	if len(result)>0:
		response = 'A total of {} matches took place on {}.\n'.format(len(result),date_of_match)
		for i in range(len(result)):
			response += 'Match {}: {} versus {}. Man of the match was {}.\n'.format((i+1),result[i]["team1"],result[i]["team2"],result[i]["player_of_match"])
	else:
		response = 'Sorry, Your query did not return any result. Please try again.'
	return question(response)	

@ask.intent("MatchSummary")	
def summarize_match(date_of_match):
	requestPayload = query_summary.format(date_of_match)
	resp = requests.request("POST", url, data=(requestPayload), headers=headers)
	result = json.loads(resp.content)
	if len(result)>0:
		response = 'A total of {} matches took place on {}.\n'.format(len(result),date_of_match)
		for i in range(len(result)):
			if result[i]["win_by_runs"]>0:
				response += 'Match {}: {} versus {}. The match was played at {},{}. {} won the toss and elected to {} first. {} won the match by {} runs. Man of the match was {}.\n'.format((i+1),result[i]["team1"],result[i]["team2"],result[i]["venue"],result[i]["city"],result[i]["toss_winner"],result[i]["toss_decision"],result[i]["winner"],result[i]["win_by_runs"],result[i]["player_of_match"])
			else:
				response += 'Match {}: {} versus {}. The match was played at {},{}. {} won the toss and elected to {} first. {} won the match by {} wickets. Man of the match was {}.\n'.format((i+1),result[i]["team1"],result[i]["team2"],result[i]["venue"],result[i]["city"],result[i]["toss_winner"],result[i]["toss_decision"],result[i]["winner"],result[i]["win_by_wickets"],result[i]["player_of_match"])
					
	else:
		response = 'Sorry, Your query did not return any result. Please try again.'
	return question(response)

@ask.intent("IPLFinal")
def ipl_final(season):
	if season in seasons:

		season = seasons[season]
		requestPayload = query_final.format(season)
		resp = requests.request("POST", url, data=(requestPayload), headers=headers)
		result = json.loads(resp.content)
		match_id=result[0]["match_id"]
		requestPayload = query_by_id.format(match_id)
		resp = requests.request("POST", url, data=(requestPayload), headers=headers)
		result_final = json.loads(resp.content)
		team1,team2,winner,win_by_runs,win_by_wickets = result_final[0]["team1"],result_final[0]["team2"],result_final[0]["winner"],result_final[0]["win_by_runs"],result_final[0]["win_by_wickets"]
		if winner==team1:
			loser=team2
		else:
			loser=team1
		if win_by_runs>0:
			response = "{} won the IPL season {}, defeating {} in the final match by {} runs.".format(winner,season,loser,win_by_runs)
		else:
			response = "{} won the IPL season {}, defeating {} in the final match by {} wickets.".format(winner,season,loser,win_by_wickets)	

	else:
		response = 'Sorry, Your query did not return any result. Please try again.'
	return question(response)	


@ask.intent("Exit")
def exit():
	return statement("Thank you for using IPL search. Bye !")


