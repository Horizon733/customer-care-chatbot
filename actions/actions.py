import os
from pathlib import Path
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher

from utils.utils import get_html_data, send_email


class ValidateContactUsForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_contact_us_form"

    def validate_name(
        self,
        value: Text,
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> Dict[str, str]:
        if value is not None:
            return {"name": value}
        else:
            return {"requested_slot": "name"}

    def validate_email(
        self,
        value: Text,
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> Dict[str, str]:
        if value is not None:
            return {"email": value}
        else:
            return {"requested_slot": "email"}

    def validate_phone_number(
        self,
        value: Text,
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> Dict[str, str]:
        if value is not None:
            return {"phone_number": value}
        else:
            return {"requested_slot": "phone_number"}

    def validate_confirm_details(
        self,
        value: Text,
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> Dict[str, str]:
        intent_name = tracker.get_intent_of_latest_message()
        if value is not None:
            if intent_name in ["affirm", "deny"]:
                return {"confirm_details": intent_name}
        else:
            return {"requested_slot": "confirm_details"}


class ActionSubmitContactForm(Action):
    def name(self) -> Text:
        return "action_submit_contact_us_form"

    def run(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        confirm_details = tracker.get_slot("confirm_details")
        name = tracker.get_slot("name")
        email = tracker.get_slot("email")
        phone_number = tracker.get_slot("phone_number")
        message = tracker.get_slot("message")
        if confirm_details == "affirm":
            this_path = Path(os.path.realpath(__file__))
            user_content = get_html_data(f"{this_path.parent}/utils/user_mail.html")
            send_email("Thank you for contacting us", email, user_content)
            admin_content = get_html_data(f"{this_path.parent}/utils/admin_mail.html")
            admin_content.format(
                name=name,
                email=email,
                phone_number=phone_number,
                message=message
            )
            is_mail_sent = send_email(f"{email.split('@')[0]} contacted us!", "your@gmail.com", admin_content)
            if is_mail_sent:
                dispatcher.utter_message(template="utter_mail_success")
            else:
                dispatcher.utter_message("Sorry, I wasn't able to send mail. Please try again later.")
        else:
            dispatcher.utter_message(template="utter_mail_canceled")
        return []