from datetime import datetime, timedelta
import http_client
from configs import Configs


def __get_tomorrow_day():
    tomorrow = datetime.today() + timedelta(days=1)
    # Format as YYYY-MM-DD
    tomorrow_str = tomorrow.strftime("%Y-%m-%d")
    return tomorrow_str


def __book_for_user(class_id, user, tomorrow_day, class_time):
    configs = Configs()
    email, password, user_id, user_center_id = configs.get_user(user)

    if (email is None
            or password is None
            or user_id is None
            or user_center_id is None):
        raise Exception("Error getting parameters")

    token = http_client.login(email, password)
    if token is None:
        raise Exception("Error getting authentication token")

    class_booking_id = http_client.get_class_booking_id(token, user_id, user_center_id, class_id, tomorrow_day, class_time)
    if class_booking_id is None:
        raise Exception("Error getting booking class id ")

    # book_class(user_id, user_center_id, booking_id): 2432, 728, 28401
    result = http_client.book_class(token, user_id, user_center_id, class_booking_id)
    if result is not True:
        raise Exception("Error on result value")


def process(event, context):
    class_name = event.get('className', None)
    class_time = event.get('classTime', None)
    users = event.get("users", [])
    print(f"User: {users}, Class name: {class_name} and time: {class_time}")

    tomorrow_day = __get_tomorrow_day()
    configs = Configs()
    class_id = configs.get_class_id(class_name)
    print(f"Class id is {class_id}")
    if class_id is None:
        raise Exception(f"Invalid class id for class name parameter {class_name}")

    for user in users:
        __book_for_user(class_id, user, tomorrow_day, class_time)


def lambda_handler(event, context):
    try:
        process(event, context)
        return {
            'statusCode': 200,
            'body': 'OK'
        }
    except Exception as e:
        print(f"Exception occurred: {e}")
        return {
            'statusCode': 400,
            'body': 'OK'
        }
