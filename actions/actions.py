from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher


def repeat(tracker: Tracker, dispatcher: CollectingDispatcher):
    user_ignore_count = 2
    count = -1
    tracker_list = []

    while abs(count) <= len(tracker.events) and user_ignore_count > 0:
        event = tracker.events[count].get('event')
        if event == 'user':
            user_ignore_count -= 1
        elif event == 'bot':
            tracker_list.append(tracker.events[count])
        count -= 1

    tracker_list.reverse()

    for event in tracker_list:
        data = event.get('data')
        if data and "buttons" in data:
            dispatcher.utter_message(text=event.get('text'), buttons=data["buttons"])
        elif event.get('text'):
            dispatcher.utter_message(text=event.get('text'))
        break


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
        return [UserUtteranceReverted()]


class ActionCheckInTime(Action):
    def name(self): return "action_check_in_time"
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(response="utter_check_in_time")
        repeat(tracker, dispatcher)
        return [UserUtteranceReverted()]


class ActionCheckOutTime(Action):
    def name(self): return "action_check_out_time"
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(response="utter_check_out_time")
        repeat(tracker, dispatcher)
        return [UserUtteranceReverted()]


class ActionCancelReservation(Action):
    def name(self): return "action_cancel_reservation"
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(response="utter_cancel_reservation")
        repeat(tracker, dispatcher)
        return [UserUtteranceReverted()]


class ActionCancellationPolicy(Action):
    def name(self): return "action_cancellation_policy"
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(response="utter_cancellation_policy")
        repeat(tracker, dispatcher)
        return [UserUtteranceReverted()]


class ActionHaveRestaurant(Action):
    def name(self): return "action_have_restaurant"
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(response="utter_have_restaurant")
        repeat(tracker, dispatcher)
        return [UserUtteranceReverted()]


class ActionBreakfastAvail(Action):
    def name(self): return "action_breakfast_avail"
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(response="utter_breakfast_avail")
        repeat(tracker, dispatcher)
        return [UserUtteranceReverted()]


class ActionBreakfastTime(Action):
    def name(self): return "action_breakfast_time"
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(response="utter_breakfast_time")
        repeat(tracker, dispatcher)
        return [UserUtteranceReverted()]


class ActionRestaurantTime(Action):
    def name(self): return "action_restaurant_time"
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(response="utter_restaurant_time")
        repeat(tracker, dispatcher)
        return [UserUtteranceReverted()]
