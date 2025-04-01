import urllib.request
import json
from configs import Configs


configs = Configs()
BASE_URL = configs.GYM_URL_API


def __get_body_to_get_search_classes(activity_ids, class_day):
    body = {
        "activityGroupIds": [],
        "activityIds": [
            activity_ids
        ],
        "centers": [
            709
        ],
        "dateFrom": class_day,
        "dateTo": class_day
    }
    return json.dumps(body).encode("utf-8")


def get_class_booking_id(token, user_id, user_center_id, activity_id, class_day, class_start_time):
    body = __get_body_to_get_search_classes(activity_id, class_day)
    url = f"{BASE_URL}classes/search-booking-participations?selectedUserId={user_id}&selectedUserCenterId={user_center_id}"
    response = __post(url, body, token)

    for entry in response:
        booking = entry.get("booking")
        if booking.get("startTime") == class_start_time:
            return booking.get("id")

    return None


def __get_body_to_book_class(user_id, user_center_id, booking_id):
    body = {
        "selectedUserId": user_id,
        "selectedUserCenterId": user_center_id,
        "bookingId": booking_id,
        "bookingCenterId": 709
    }
    return json.dumps(body).encode("utf-8")


def book_class(token, user_id, user_center_id, booking_id):
    body = __get_body_to_book_class(user_id, user_center_id, booking_id)
    url = f"{BASE_URL}booking/create-booking"
    response = __post(url, body, token)
    if response.get('state') == 'BOOKED':
        return True

    return False


def __post(url, body, token=None):
    try:
        headers = {'Accept': 'application/json',
                   'Accept-Encoding': 'gzip, deflate, br',
                   'Content-Type': 'application/json',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        if token is not None:
            headers['Authorization'] = f"Bearer {token}"

        res = urllib.request.urlopen(urllib.request.Request(
            url=url,
            data=body,
            headers=headers,
            method='POST'),
            timeout=60)

        if res.status == 200:
            response_body = res.read().decode("utf-8")
            return json.loads(response_body)

        raise Exception(f"HTTP status {res.status} calling {url}")
    except urllib.error.HTTPError as e:
        raise Exception(f"Exception calling {url}:\nError message: {str(e)}")


def __get_body_for_login(email, password):
    body = {
        "email": email,
        "password": password,
        "sessionTimeoutOneMonth": False
    }
    return json.dumps(body).encode("utf-8")


def login(email, password):
    url = f"{BASE_URL}user/authenticate"
    body = __get_body_for_login(email, password)
    response = __post(url, body, None)
    return response.get('token')
