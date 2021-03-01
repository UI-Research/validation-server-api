import requests
import logging

logger = logging.getLogger('django')
"""
Class: Backend
Description: Main class to communicate with simulation engine
             i.e. send analysis requests, receive notifications
"""
class Backend():

    """
    Function: send_request
    Input:
    Description: Notify the backend server that there is a
    new analysis request in the front-end DB. 
    To determine: Send JSON request directly to backend or
    let backend retrieve from DB?
    """
    def send_request(request):
        run_id = request
        logger.info('Sending run request')
        # call engine and return success or error
        try:
            response = requests.post('http://app:8080/trigger/', data={'run_id':9})
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:  # This is the correct syntax
            raise SystemExit(e)



