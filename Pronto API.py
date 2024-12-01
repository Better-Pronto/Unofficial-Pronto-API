import requests, logging
from datetime import datetime
from dataclasses import dataclass, asdict

API_BASE_URL = "https://stanfordohs.pronto.io/"

class BackendError(Exception):
    pass
# Dataclass for device information
@dataclass
class DeviceInfo:
    browsername: str
    browserversion: str
    osname: str
    type: str
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#AUTHENTICATION FUNCTIONS
# Function to verify user email
def requestVerificationEmail(email):
    url = "https://accounts.pronto.io/api/v1/user.verify"
    payload = {"email": email}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        raise BackendError(f"HTTP error occurred: {http_err}")
    except Exception as err:
        raise BackendError(f"An error occurred: {err}")

# Function to log in using email and verification code
def verification_code_to_login_token(email, verification_code):
    url = "https://accounts.pronto.io/api/v3/user.login"
    device_info = DeviceInfo(
        browsername="Firefox",
        browserversion="130.0.0",
        osname="Windows",
        type="WEB"
    )
    request_payload = {
        "email": email,
        "code": verification_code,
        "device": asdict(device_info)
    }
    headers = {
        "Content-Type": "application/json"
    }
    logger.info(f"Payload being sent: {request_payload}")
    try:
        response = requests.post(url, json=request_payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")

# Function to get user access token from logintoken
def login_token_to_access_token(logintoken):
    url = f"{API_BASE_URL}api/v1/user.tokenlogin"
    device_info = {
        "browsername": "firefox",
        "browserversion": "130.0.0",
        "osname": "macOS",
        "type": "WEB",
        "uuid": "314c9314-d5e5-4ae4-84e2-9f2f3938ca28",
        "osversion": "10.15.6",
        "appversion": "1.0.0",
        }
    request_payload = {
        "logintokens": [logintoken],
        "device": device_info,
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, json=request_payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")



#BUBBLE FUNCTIONS
# Function to get all user's bubbles
def getUsersBubbles(access_token):
    url = f"{API_BASE_URL}api/v3/bubble.list"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",  # Ensure 'Bearer' is included
    }

    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")

# Function to get last 50 messages in a bubble, given bubble ID 
# and an optional argument of latest message ID, which will return a list of 50 messages sent before that message
def get_bubble_messages(access_token, bubbleID, latestMessageID):
   
    url = f"{API_BASE_URL}/api/v1/bubble.history"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    if latestMessageID is None:
        request_payload = {"bubble_id": bubbleID}
    else:
        request_payload = {"bubble_id": bubbleID, "latest": latestMessageID}

    try:
        response = requests.post(url, headers=headers, json=request_payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")

#Function to get information about a bubble
def get_bubble_info(access_token, bubbleID):
    url = f"{API_BASE_URL}/api/v2/bubble.info"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    request_payload = {
        "bubble_id": bubbleID,
    }
    try:
        response = requests.post(url, headers=headers, json=request_payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")

#Function to mark a bubble as read
def markBubble(access_token, bubbleID):
    url = f"{API_BASE_URL}/api/v1/bubble.mark"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    request_payload = {
        "bubble_id": bubbleID,
    }
    try:
        response = requests.post(url, headers=headers, json=request_payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")

#Function to create DM
def createDM(access_token, id, orgID):
    url = f"{API_BASE_URL}/api/v1/dm.create"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    request_payload = {
        "organization_id": orgID,
        "user_id": id,
    }
    try:
        response = requests.post(url, headers=headers, json=request_payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")

#Function to create a bubble/group
def createBubble(access_token, orgID, title, category_id):
    url = f"{API_BASE_URL}/api/v1/bubble.create"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    if category_id is not None:
        request_payload = {
        "organization_id": orgID,
        "title": title,
        "category_id": category_id,
    }
    else:
        request_payload = {
        "organization_id": orgID,
        "title": title,
    }

    try:
        response = requests.post(url, headers=headers, json=request_payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")

#Function to add a member to a bubble
#invitations is a list of user IDs, in the form of [{user_id: 5302519}, {user_id: 5302367}]
def addMemberToBubble(access_token, bubbleID, invitations, sendemails, sendsms):
    url = f"{API_BASE_URL}/api/v1/bubble.invite"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    request_payload = {
        "bubbleID": bubbleID,
        "invitations": invitations,
        "sendemails": sendemails,
        "sendsms": sendsms,
    }
    try:
        response = requests.post(url, headers=headers, json=request_payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")

#Function to kick user from a bubble
#users is a list of user IDs, in the form of [5302519]
def kickUserFromBubble(access_token, bubbleID, users):
    url = f"{API_BASE_URL}/api/v1/bubble.kick"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    request_payload = {
        "bubble_id": bubbleID,
        users: users,
    }
    try:
        response = requests.post(url, headers=headers, json=request_payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")



#MESSAGE FUNCTIONS
# Function to send a message to a bubble
def send_message_to_bubble(access_token, bubbleID, created_at, message, userID, uuid):
    url = f"{API_BASE_URL}/api/v1/message.create"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    request_payload = {
        "bubble_id": bubbleID,
        "created_at": created_at,
        "id": "null",
        "message": message,
        "messagemedia": [],
        "user_id": userID,
        "uuid": uuid  
    }
    try:
        response = requests.post(url, headers=headers, json=request_payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")

# Function to add a reaction to a message
def addReaction(access_token, messageID, reactiontype_id):
    url = f"{API_BASE_URL}/api/v1/message.addreaction"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    request_payload = {
        "message_id": messageID,
        "reactiontype_id": reactiontype_id,
    }
    try:
        response = requests.post(url, headers=headers, json=request_payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")

# Function to remove a reaction from a message
def removeReaction(access_token, messageID, reactiontype_id):
    url = f"{API_BASE_URL}/api/v1/message.removereaction"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    request_payload = {
        "message_id": messageID,
        "reactiontype_id": reactiontype_id,
    }
    try:
        response = requests.post(url, headers=headers, json=request_payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")

# Function to edit a message
def editMessgae(access_token, newMessage, messageID):
    url = f"{API_BASE_URL}/api/v1/message.edit"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    request_payload = {
        "message": newMessage,
        "message_id": messageID,
    }
    try:
        response = requests.post(url, headers=headers, json=request_payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")

# Function to delete a message
def deleteMessage(access_token, messageID):
    url = f"{API_BASE_URL}/api/v1/message.delete"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    request_payload = {
        "message_id": messageID,
    }
    try:
        response = requests.post(url, headers=headers, json=request_payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")


#USER INFO FUNCTIONS
# Function to get user information
def userInfo(access_token, id):
    url = f"{API_BASE_URL}/api/v1/user.info"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    request_payload = {
        "id": id,
    }
    try:
        response = requests.post(url, headers=headers, json=request_payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")

# Function to get a user's mutual groups
def mutualGroups(access_token, id):
    url = f"{API_BASE_URL}/api/v1/user.mutualgroups"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    request_payload = {
        "id": id,
    }
    try:
        response = requests.post(url, headers=headers, json=request_payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")

