# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []

import requests

CRIC_API_URL = "https://api.cricapi.com/v1/"
CRIC_API_KEY = "bade5f2e-fcc9-44b9-9659-2f0498e37dc0"

SHOW_RECENT_MATCHES = 5

class ActionGetRecentMatches(Action):
	def name(self):
		return 'action_get_recent_matches'

	def run(self, dispatcher, tracker, domain):
		res = requests.get(CRIC_API_URL + "currentMatches" + "?apikey=" + CRIC_API_KEY + "&offset=0")
		if res.status_code == 200:
			matches_data = res.json()["data"]
			matches_data.sort(key=lambda x: x["date"], reverse=True)
			matches_data = [x for x in matches_data if "matchType" in x]
			recent_matches = matches_data[:SHOW_RECENT_MATCHES]
			dispatcher.utter_message(f'Showing the status of {len(recent_matches)} recent matches\n')
			for index, match in enumerate(recent_matches):
				msg = f'{index+1}. {match["matchType"].upper()} match between ' \
					  f'{match["teams"][0]} and {match["teams"][1]} played on {match["date"]}\n' \
					  f'Match Status: {match["status"]}\n'
				dispatcher.utter_message(msg)
		else:
			dispatcher.utter_message(f'Unable to fetch the recent matches details. Please try with some other query!!')
		return []