import requests
import time
import json

# Documentation of AmplitudeHTTP API V2:
#   https://developers.amplitude.com/docs/http-api-v2
#
# Convert Curl queries - such as below to - python:
#   https://curl.trillworks.com/
#
# Example HTTP Curl Query for Amplitude:
# curl --data '{"api_key": "SOMEIDOFAKIND", "events": [{"user_id": "john_doe@gmail.com", "event_type": "watch_tutorial", "user_properties": {"Cohort": "Test A"}, "country": "United States", "ip": "127.0.0.1"}]}' https://api.amplitude.com/2/httpapi


class AmplitudeLogger:
    def __init__(self, api_key, api_uri="https://api.amplitude.com/2/httpapi"):
        self.api_key = api_key
        self.api_uri = api_uri
        self.is_logging = True

    def turn_on_logging(self):
        self.is_logging = True

    def turn_off_logging(self):
        self.is_logging = False

    def create_event(self, **kwargs):
        event = dict()
        user_id = kwargs.get('user_id', None)
        device_id = kwargs.get('device_id', None)
        event_type = kwargs.get('event_type', None)

        if user_id is None or device_id is None or event_type is None:
            raise ValueError('user_id, device_id, event_type should be non empty sting')

        event["device_id"] = device_id if device_id is str else str(device_id)
        event["user_id"] = user_id if user_id is str else str(user_id)
        event["event_type"] = event_type if event_type is str else str(event_type)
        event["time"] = long(time.time() * 1000)

        user_properties = kwargs.get('user_properties', None)
        if user_properties is not None and type(user_properties) == dict:
            event["user_properties"] = user_properties

        event_properties = kwargs.get('event_properties', None)
        if event_properties is not None and type(event_properties) == dict:
            event["event_properties"] = event_properties

        app_version = kwargs.get('app_version', None)
        if app_version is not None and app_version is str:
            event["app_version"] = app_version

        platform = kwargs.get('platform', None)
        if platform is not None and platform is str:
            event["platform"] = platform

        event_package = {
            'api_key': self.api_key,
            'events': [event]
        }

        return event_package

    def log_event(self, event):
        if event is not None:
            if self.is_logging:
                result = requests.post(self.api_uri, json=event)
                return result
