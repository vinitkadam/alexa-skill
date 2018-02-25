# Alexa IPL

## Introduction

This is an alexa skill which gives you answers about all the previous IPL matches till Season10 (2017), based on your queries.

## How does it work?

### Workflow
You can test out this skill using an Amazon Echo device or at [Echosim](https://echosim.io) (Web Browser) or at [Reverb](https://reverb.ai/) (Android/iOS). The workflow is as follows:
- You invoke the skill saying "Alexa, start IPL Search."
- Alexa will speak a welcome message and wait for your query.
- Currently we have 3 types of queries that can be invoked  
    **1. Match Summary:**  
    		*sample invocation* - `Summarize the match on April 9, 2017`  
    **2. Man of the Match:**  
    		*sample invocation* - `Who was awarded the man of the match on April 9, 2017`  
    **3. Match Result:**  
    		*sample invocation* - `Who won the match between Kolkata and Mumbai that took place on April 9, 2017`  
    **4. Season Winners:**  
    		*sample invocation* - `Who was the winner of IPL Season 2014`  
-If you want to exit the skill, you can do so by saying `exit` or `goodbye` or `close IPL search`  
**_Note:_** We will iteratively add more intents to the skills, which will be introduced in later releases.  

### Internal Implementation

This skill is written in Python using Flask and the python library [Flask-Ask](https://github.com/johnwheeler/flask-ask). The Implementation is as follows:
- When you make a particular type of query, an appropriate intent from the skill set is invoked and then the relevant method mapped to that intent is called from the Flask script, which fetches the results from the matches database.
A response string is generated using fetched data, which is spoken out by Alexa.  
- If Alexa is not able to recognise the spoken words or if there exists no results based on the parameters passed, Alexa will humbly respond and ask you to try again.


## How to get it up and running?
### Deployment
This skill can be deployed on any server that supports HTTPS over SSL. 
For our testing purpose we are using services of Hasura. Hasura automatically generates SSL certificates for you.
Just run the following commands to deploy your skill.

(Make sure you have [hasura-cli](https://docs.hasura.io/0.15/manual/install-hasura-cli.html))

```
$ hasura quickstart khan185/alexa-ipl-skill
$ cd alexa-ipl-skill
$ git add . && git commit -m "Initial Commit"
$ git push hasura master
```

### How to add the skill to your Amazon account?

To link it with your Amazon Echo Device, go to your [Amazon developer console](https://developer.amazon.com/edw/home.html#/skills).

1. Create a new skill. Call it `IPL Ask` (or any name you'd like to give). Give the invocation name as `ipl ask`. Click next.  

2. Add this intent schema
```
"intents": [
      {
        "name": "AMAZON.CancelIntent",
        "samples": []
      },
      {
        "name": "AMAZON.HelpIntent",
        "samples": []
      },
      {
        "name": "AMAZON.StopIntent",
        "samples": []
      },
      {
        "name": "Exit",
        "samples": [
          "Bye",
          "Quit",
          "Exit",
          "Close IPL Search",
          "Close",
          "Shutdown"
        ],
        "slots": []
      },
      {
        "name": "IPLFinal",
        "samples": [
          "Who won the final match of season {season}",
          "who won the IPL in the year {season}",
          "tell me about the final match of season {season}",
          "who won IPL season {season}",
          "who was the winner of IPL season {season}",
          "who won the final match of IPL {season}",
          "who won the IPL trophy in season {season}"
        ],
        "slots": [
          {
            "name": "season",
            "type": "AMAZON.NUMBER",
            "samples": [
              "{season}"
            ]
          }
        ]
      },
      {
        "name": "MatchResult",
        "samples": [
          "Did {teamA} win the match against {teamB} on {date_of_match}",
          "Tell me the result of the match between {teamA} and {teamB} on {date_of_match}",
          "Tell me about the winner of the match between {teamA} and {teamB} the date of the match is {date_of_match}",
          "give me the match result between {teamA} and {teamB} that took place on {date_of_match}",
          "Who won the match between {teamA} and {teamB} on {date_of_match}",
          "Who was the winner in the match of {teamA} versus {teamB} that took place on {date_of_match}"
        ],
        "slots": [
          {
            "name": "teamA",
            "type": "IPL_TEAM"
          },
          {
            "name": "teamB",
            "type": "IPL_TEAM"
          },
          {
            "name": "date_of_match",
            "type": "AMAZON.DATE"
          }
        ]
      },
      {
        "name": "MatchSummary",
        "samples": [
          "Please give summary of the match that took place on {date_of_match}",
          "Give highlights of the match that took place on {date_of_match}",
          "Summarize the match played on {date_of_match}",
          "Give details of that match that was played on {date_of_match}",
          "Tell me more about the match played on {date_of_match}"
        ],
        "slots": [
          {
            "name": "date_of_match",
            "type": "AMAZON.DATE"
          }
        ]
      },
      {
        "name": "MOMatch",
        "samples": [
          "Who was the player of the match on {date_of_match}",
          "Who was awarded the man of the match that took place on {date_of_match}",
          "Who was the best player of the match that took place on {date_of_match}",
          "Who was the man of the match for the match that took place on {date_of_match}",
          "Which player showed best performance in the match that took place on {date_of_match}"
        ],
        "slots": [
          {
            "name": "date_of_match",
            "type": "AMAZON.DATE"
          }
        ]
      }
    ]
```

3. Create custom slot with the name 'IPL_TEAM', and add all the IPL teams of previous seasons along with their sample utterances.  

   Click next.  

**_Note:_** The entire skill setup on Amazon portal can now be done easily with the help of a GUI 'Alexa Skill Builder' which is currently present as a Beta version on Amazon Developer portal.

4. For the service endpoint, check the `HTTPS` radio button.

	Put the default URL as `https://bot.<cluster-name>.hasura-app.io/ipl`. (Run `$ hasura cluster status` from root directory to know your cluster name).

	Click next.

5. About SSL certificates, Hasura services have auto generated `LetsEncrypt` Grade A SSL certificates. This means, you have to check the radio button that says `My development endpoint has a certificate from a trusted certificate authority`

	Click next.

6. Your skill is live on the ECHO device associated with your account. Test it by saying **Alexa**, `start IPL Ask`. And Alexa will become your Harsha Bhogle :)

## How to use it as a boilerplate?

The source code lies in the `microservices/bot/app/src` directory. This is a simple application, so the entire code lies in `server.py`.  
You might want to go through the Flask-ask docs (a very quick read).    

## Contributors  
1. Shahbaz Khan ([@shahbazkhan185](https://twitter.com/shahbazkhan185), [fb/khandemic](https://fb.com/khandemic))
2. Vinit Kadam ([@vinitkadam1997](https://twitter.com/vinitkadam1997))

