
from __future__ import print_function
import requests, re
from FlaskWebProject import config


"""
Service status code:
We use status codes based on HTTP status codes which are usually returned by email service providers.
It is also easy to extend if needed.

Specifically:
Status_Code  Meaning
200          OK (Email sent successfully)
400          Bad Request

"""

class Result(object):
    def __init__(self, status, message, status_code=200):
        self.status = status
        self.message = message
        self.status_code = status_code

class SuccessResult(Result):
    def __init__(self, message, status_code=200):
        super(type(self), self).__init__('success', message, status_code)


class FailureResult(Result):
    def __init__(self, message, status_code=400):
        super(type(self), self).__init__('error', message, status_code)


"""
EmailService
"""
class EmailService:
    # Remember last working sender
    _last_sender = 0
    _senders = []

    def __init__(self, senders):
        self._senders = senders

    def send(self, message_data): 
        """
        Main API of the service to send email using one of the senders given the requested data.
        If a sender fails to send, it will try the other senders. If all fails, it returns a
        400 failure result back.
        """

        # Extract emails from request
        to_email_list = self.get_email_list(message_data['to_email']) if 'to_email' in message_data else []
        cc_email_list = self.get_email_list(message_data['cc_email']) if 'cc_email' in message_data else []
        bcc_email_list = self.get_email_list(message_data['bcc_email'])  if 'bcc_email' in message_data else []

        email_lists = [to_email_list, cc_email_list, bcc_email_list]

        # Do some validation on request
        result = self.validate_send_request(message_data, email_lists)
        if result is not None:
            return result
    
        # Send email using senders
        # Try to use the last working sender
        sender_id = self._last_sender
        while True:
            ret = self._senders[sender_id].send(message_data, email_lists)
            if ret.status_code == 200:
                # Remember the working sender
                self._last_sender = sender_id
                # Return success
                return ret
            else:
                #TODO: log failures for service quality analytics

                # Fail over to next senders
                sender_id = (sender_id + 1) % len (self._senders)
                if sender_id == self._last_sender:
                    # We have tried all senders and they all fails
                    return FailureResult('Sorry! We cannot send your email at the moment. Pleae try again later!')

    def get_email_list(self, emails):
        """
        Parse input string of emails separated by comma and remove all preceding and trailing spaces
        """
        return  [x.strip() for x in emails.split(',') if len(x.strip()) > 0]


    def validate_email(self, email_address):
        """
        Do basic email address validation with RegEx
        """
        return re.match(r"[a-zA-Z0-9]+(\.?[a-zA-Z0-9]+)*@[a-zA-Z0-9]+(\.?[a-zA-Z0-9]+)*\.[a-zA-Z0-9]{2,}", email_address)

    def validate_email_lists(self, email_lists):
        """
        Validate multiple email lists to make sure all emails look good
        """
        for list in email_lists:
            if len(list) > 0:
                for email in list:
                    if not (self.validate_email(email)):
                        return False
        # all tests passed
        return True    

    def validate_send_request(self, message_data, email_lists):
        """
        Do basic validation on send request from user. This function returns any error if found
        """
        # validate sender
        if not ('from_email' in message_data and self.validate_email(message_data['from_email'])):
            return FailureResult('Invalid sender email.')
        # validate to recipient list
        if len(email_lists[0]) == 0:
            return FailureResult('There must be at least one recipient.')
        if not (self.validate_email_lists(email_lists)):
            return FailureResult('Invalid recipient email.')
        # validate subject and content
        if (len(message_data['subject']) == 0) or (len(message_data['subject']) > config.MAX_SUBJECT_LENGTH):
            return FailureResult('Subject cannot be empty or have more than %s characters.' % config.MAX_SUBJECT_LENGTH)
        if (len(message_data['content']) == 0) or (len(message_data['content']) > config.MAX_CONTENT_LENGTH):
            return FailureResult('Content cannot be empty or have more than %s characters.' % config.MAX_CONTENT_LENGTH)

