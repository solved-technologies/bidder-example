#!/usr/bin/env python3

import argparse
import datetime
import json
import sys

import requests


def main():
    parser = argparse.ArgumentParser(description="Example ping/post flow.")
    parser.add_argument("username", help="username for test ping/post")
    parser.add_argument("password", help="password for test ping/post")

    args = parser.parse_args()

    ping_request_data = {
        "lead_vertical": "windows",
        "lead_data": {
            "building_stories": 2,
            "contact_tcpa_consent": True,
            "contact_tcpa_text": "I consent to robots calling me...",
            "windows_count": 3,
            "property_zipcode": "02201",
            "request_emergency": False,
            "request_timestamp": str(datetime.datetime.now()),
            "windows_action": "replace",
        },
        "test": True,
    }

    ping_request_url = "https://bidder.solvedhome.io/v1/ping"

    print("PING REQUEST:")
    print(json.dumps(ping_request_data))
    print("")

    ping_response = requests.post(
        ping_request_url,
        auth=(args.username, args.password),
        data=json.dumps(ping_request_data),
    )
    if ping_response.status_code != 200:
        sys.stderr.write(
            f"got unexpected ping HTTP status code {ping_response.status_code:d}\n"
        )
        return 1

    print("PING RESPONSE:")
    print(ping_response.text)
    print("")

    ping_response_data = json.loads(ping_response.text)

    post_request_data = ping_request_data.copy()
    post_request_data["lead_data"].update(
        {
            "contact_email": "test@solvedhome.test",
            "contact_first_name": "Testy",
            "contact_last_name": "Tester",
            "contact_phone_mobile": "987-654-3210",
            "contact_tcpa_consent": True,
            "ping_uuid": ping_response_data["ping_uuid"],
            "property_address": "1 City Hall Square #500",
            "property_city": "Boston",
            "property_state": "MA",
        }
    )

    post_request_url = "https://bidder.solvedhome.io/v1/post"

    print("POST REQUEST:")
    print(json.dumps(post_request_data))
    print("")

    post_response = requests.post(
        post_request_url,
        auth=(args.username, args.password),
        data=json.dumps(post_request_data),
    )
    if post_response.status_code != 200:
        sys.stderr.write(
            f"got unexpected post HTTP status code {post_response.status_code:d}\n"
        )
        return 1

    print("POST RESPONSE:")
    print(post_response.text)

    return 0


if __name__ == "__main__":
    sys.exit(main())
