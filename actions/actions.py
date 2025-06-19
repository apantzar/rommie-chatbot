from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher


class ActionResetSlots(Action):
    def name(self) -> Text:
        return "action_reset_slots"

    def run(self, dispatcher, tracker, domain) -> List[Dict]:
        return [SlotSet("number", None), SlotSet("room_type", None)]


class MyFallbackAction(Action):
    def name(self) -> Text:
        return "action_my_fallback"

    def run(self, dispatcher, tracker, domain) -> List[Dict]:
        dispatcher.utter_message(response="utter_fallback_message")

        # Only repeat buttons or custom payload if confidence is low
        confidence = tracker.latest_message.get("intent", {}).get("confidence", 1.0)
        if confidence < 0.4:  # Adjust this threshold if needed
            repeat(tracker, dispatcher)

        return []

# Only used in fallback:
def repeat(tracker: Tracker, dispatcher: CollectingDispatcher):
    count = -1
    user_utterances_to_skip = 2
    history = []

    while abs(count) <= len(tracker.events) and user_utterances_to_skip > 0:
        event = tracker.events[count]
        if event.get('event') == 'user':
            user_utterances_to_skip -= 1
        elif event.get('event') == 'bot':
            data = event.get('data')
            # Only repeat if bot used buttons or custom payload
            if data and ("buttons" in data or "custom" in data):
                history.append(event)
        count -= 1

    history.reverse()

    for event in history:
        data = event.get('data')
        if data and "buttons" in data:
            dispatcher.utter_message(text=event.get('text'), buttons=data["buttons"])
        elif data and "custom" in data:
            dispatcher.utter_message(text=event.get('text'), json_message=data["custom"])
        break


# FAQ-style actions: keep them simple
class ActionCheckInTime(Action):
    def name(self): return "action_check_in_time"
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(response="utter_check_in_time")
        return []

class ActionCheckOutTime(Action):
    def name(self): return "action_check_out_time"
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(response="utter_check_out_time")
        return []

class ActionCancelReservation(Action):
    def name(self): return "action_cancel_reservation"
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(response="utter_cancel_reservation")
        return []

class ActionCancellationPolicy(Action):
    def name(self): return "action_cancellation_policy"
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(response="utter_cancellation_policy")
        return []

class ActionHaveRestaurant(Action):
    def name(self): return "action_have_restaurant"
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(response="utter_have_restaurant")
        return []

class ActionBreakfastAvail(Action):
    def name(self): return "action_breakfast_avail"
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(response="utter_breakfast_avail")
        return []

class ActionBreakfastTime(Action):
    def name(self): return "action_breakfast_time"
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(response="utter_breakfast_time")
        return []

class ActionRestaurantTime(Action):
    def name(self): return "action_restaurant_time"
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(response="utter_restaurant_time")
        return []
