from abc import ABCMeta, abstractmethod
import mandrill

from FlaskWebProject import config
from FlaskWebProject.email_service import Result, FailureResult, SuccessResult

class BaseSender(object):
    __metaclass__ = ABCMeta
    """
    Base class for all email senders
    """

    @abstractmethod
    def send(self, message, email_lists):
        """
        Main send mail function
        :param message: dictionary of send request data
        :param email_lists: list of to/cc/bcc emails. Note: Not all email senders support all of these fields.
        """
        pass

    return_message_success_result = SuccessResult('Email sent successfully.')
    

class MandrillSender(BaseSender):
    """
    Email sender using Mandrill service
    """
    def send(self, message_data, email_lists):
        
        to_email_list = email_lists[0]
        cc_email_list = email_lists[1]
        bcc_email_list = email_lists[2]

        to_list = []
        for email in to_email_list:
            to_list.append({'email': email, 'type':'to'})
        for email in cc_email_list:
            to_list.append({'email': email, 'type':'cc'})
        for email in bcc_email_list:
            to_list.append({'email': email, 'type':'bcc'})

        message = {
            'from_email': message_data['from_email'],
            'to': to_list,
            'subject': message_data['subject'],
            'text': message_data['content']
        }

        ret = None
        mandrill_client = mandrill.Mandrill(config.MANDRILL_API_KEY)
        try:
            ret = mandrill_client.messages.send(message=message, async=False, ip_pool='Main Pool')
        except mandrill.Error as e:
            return FailureResult(e.message)

        result = ret[0]
        if result['status'] == 'sent':
            return self.return_message_success_result
        elif result['status'] == 'error':
            return Result(result['status'], 'Unexpected: Error %s ' % result['message'])
        elif result['status'] == 'rejected':
            return Result(result['status'], "Unexpected: Rejected due to %s " % (result['email'], result['reject_reason']))
        else:
            return Result(result['status'], "Unexpected: Get an unexpected status from Mandrill!")


class MailgunSender(BaseSender):
    """
    Email sender using Mailgun service
    """

    def send(self, message_data, email_lists):

        to_email_list = email_lists[0]
        cc_email_list = email_lists[1]
        bcc_email_list = email_lists[2]

        data_dict = {
            'from': message_data['from_email'],
            'to': ','.join(to_email_list),
            'subject': message_data['subject'],
            'text': message_data['content']
        }

        if len(cc_email_list) > 0:
            data_dict['cc'] = ",".join(cc_email_list)

        if len(bcc_email_list) > 0:
            data_dict['bcc'] = ",".join(bcc_email_list)

        ret = requests.post(
                config.MAILGUN_MESSAGE_BASE_URL,
                auth=("api", config.MAILGUN_API_KEY),
                data=data_dict)
            
        r_status_code = ret.status_code
        r_json = ret.json()
        r_message = r_json['message']
        if r_status_code == 200:
            return self.return_message_success_result
        return FailureResult(r_message, r_status_code)

