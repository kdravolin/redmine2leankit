from python_leankit import LeankitKanban, LeankitCard
from python_redmine import Redmine
from config import *
import re

def getDueDate(issue):
    '''Get and convert Redmine date into Leankit format'''
    due_date = None
    if hasattr(issue, 'due_date'):
                dd_atr = issue.due_date.split("-")
                due_date = "%s/%s/%s" % (dd_atr[2],dd_atr[1],dd_atr[0])
    return due_date

def getCardType(issue, lane):
    '''Matching Redmine tracker and Leankit card type'''
    if issue.tracker['name'] in CARDTYPE_MAPPING:
        card_type = CARDTYPE_MAPPING[issue.tracker['name']]
    else:
        card_type = lane.board.default_cardtype.id
    return card_type

def getUserId(issue):
    '''Get Leankit User Id by Redmine User Name'''
    if not hasattr(issue, 'assigned_to'):
        return None
    
    atr_user = (issue.assigned_to['name']).split(' ')
    surname = atr_user[0]
    name = atr_user[1]
    
    if name + ' ' + surname in USER_MAPPING:
        user_id = USER_MAPPING[name + ' ' + surname]
    elif surname + ' ' + name in USER_MAPPING:
        user_id = USER_MAPPING[surname + ' ' + name]
    else:
        user_id = None
    return user_id

if __name__ == '__main__':

    kanban = LeankitKanban(LEANKIT_HOST, LEANKIT_LOGIN, LEANKIT_PASSWORD)
    redmine = Redmine(READMINE_URL, READMINE_API_KEY)

    print "Getting RedMine project '%s' ... " % READMINE_PROJECT_IDENTIFIER,
    project = redmine.get_project(identifier = READMINE_PROJECT_IDENTIFIER)
    print "[yes]"
    # for b in kanban.getBoards():
    #     print b.title

    print "Getting LeanKit board '%s'..." % LEANKIT_BOARDNAME,
    board = kanban.getBoard(title = LEANKIT_BOARDNAME)
    
    #filling map of card types from board
    for type_id in board.cardtypes:
        CARDTYPE_MAPPING[board.cardtypes[type_id].name] = type_id
        
    #filling map of Leankit users from board
    for user_id in board.users_by_id:
        USER_MAPPING[board.users_by_id[user_id].full_name] = user_id

    print "Cleanup LeanKit board ... "
    for card in board.cards:
        card.remove()
    print "[yes]"

    print "Start copy tickets from RedMine to LeanKit ..."
    for issue in project.filter_issues(IGNORE_LIST, status_id = "*"):
        if issue.status['name'] in STATUSES_MAPPING:

            lk_status = ""
            
            # support synchronization based on ticket status
            lk_status = STATUSES_MAPPING[issue.status['name']]

            # support synchronization based on ticket status and assign person
            if hasattr(issue, 'assigned_to') and issue.assigned_to['name'] + "::" + issue.status['name'] in STATUSES_MAPPING:
                lk_status = STATUSES_MAPPING[issue.assigned_to['name'] + "::" + issue.status['name']]
            
            # support for changing status by prefix
            for prefix in PREFIX_MAPPING:
                p = re.compile(prefix.lower() + " .*")
                m = p.match(issue.subject.lower())
                if m:
                    st = lk_status.split('::')
                    if len(st) == 2:
                        lk_status = PREFIX_MAPPING[prefix] + '::' + st[1]
                
            lane = board.getLane(lk_status)

            print "sync '%s' ... " % issue.subject,
            
            #set values of card arguments
            externalId = issue.id
            title = issue.subject
            card_type = getCardType(issue, lane)
            priority = PRIORITY_MAPPING[issue.priority['name']]
            description = issue.description
            due_date = getDueDate(issue)
            assigned_user_id = getUserId(issue)
            
            #create and save Leankit card
            card = LeankitCard.create(lane, title, card_type, externalId, priority, 
                                      description, due_date, assigned_user_id
                                      ).save()
            print "[yes]"
    print "Finished"
