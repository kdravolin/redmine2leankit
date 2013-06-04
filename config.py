# LeanKit configuration
LEANKIT_HOST = "test.leankitkanban.com"
LEANKIT_LOGIN = "use@host.com"
LEANKIT_PASSWORD = "qwerty"
LEANKIT_BOARDNAME = "Test"

# RedMine configuration
READMINE_URL = "https://redmine.host.com"
READMINE_API_KEY = "kj46436faa25e36ade5bdsdg474325798c72234"
READMINE_PROJECT_IDENTIFIER = "test-project"

# you should specify mapping between statuses in RedMine and columns in Leankit
STATUSES_MAPPING = {
    "New": "ToDo",

    "Evaluated": "Analysis::In progress",
    "Assigned": "Analysis::Done",

    "In Progress": "Development::In progress",
    "Resolved": "Development::Done",

    "Reopened / Rejected": "Testing::In progress",
    "Tested": "Testing::Done",

    "Closed": "Delivered",
    "Blocked / Feedback": "Blocked",

    # personal statuses support
    "QA full name (the same as in redmine)::In Progress": "Testing::In progress",

    # some statuses could be ignored
    # ,"Invalid": "Analysis::ToDo" # commented statuses will no be sycnhronized
}

PREFIX_MAPPING = {
    # "title prefix" : "new status"
    "Analyse" : "Analysis",
}

IGNORE_LIST = (
    # users
     "full name",
    
    # statuses
#     "Resolved",
    
    # personal statuses
#     "full name::New",
)

PRIORITY_MAPPING = {
    "Low": 0,
    "Normal": 1,
    "High": 2,
    "Urgent": 3,
    "Immediate": 3,
}

CARDTYPE_MAPPING = {}
USER_MAPPING = {}
