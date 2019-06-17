
import os
from jira import JIRA

# aws lambda environment variables encryption using kms
ATLASSIAN_API_TOKEN = os.environ['ATLASSIAN_API_TOKEN']
USER = os.environ['USER_EMAIL']
SERVER = os.environ['SERVER']
options = {
    'server': SERVER
}
print('Starting:', SERVER)
print(USER)
print(ATLASSIAN_API_TOKEN)
print(SERVER)
jira = JIRA(options, basic_auth=(USER, ATLASSIAN_API_TOKEN))
print(str(jira.projects()))


def lambda_handler(event, context):
    """
    main lambda function for handling events of AWS instance health
    """
    print("---event--------: ", event)

    if not 'issue_event_type_name' in event:
        # if data['issue_event_type_name'] == 'issue_generic':
        return 'OK'
    issue = event['issue']
    customername = issue["fields"]["assignee"]

    issuekey = issue["key"]
    # requesttype         = body.issues["fields"]["customfield_12400"]
    toolname = ''
    if 'customfield_10106' in issue['fields']:
        if 'value' in issue['fields']['customfield_10106']:
            toolname = issue['fields']['customfield_10106']['value']

    # if 'customfield_12936'in issue['fields']:
    #     toolname = issue["fields"]["customfield_12936"]

    customerusername = None
    customeremail = None
    if "reporter" in issue["fields"]:
        customerusername = issue["fields"]["reporter"]
        customeremail = customerusername["emailAddress"]
    if not customername:
        customername = ''
    else:
        if customerusername:
            customername = customerusername["displayName"]

        print(f'customer name is {customername}')
        print(f'customer email is {customeremail}')

    # "switch cases" for tool access

    if toolname == "1Password":
        comment = jira.add_comment(issuekey, '1Password: this is a test')
        print(f'A comment has been posted on {issuekey}')
    if toolname == "2Password":
        comment = jira.add_comment(issuekey, '2Password: this is a test')
        print(f'A comment has been posted on {issuekey}')

        # transitions = jira.transitions(issuekey)
        # for t in transitions:
        #     print(t['name'])
        #     print(t['id'])
        #
        # transition = jira.transition_issue(issuekey, t['id'])
        # print(f'{issuekey} has been resolved')

    return "OK"
