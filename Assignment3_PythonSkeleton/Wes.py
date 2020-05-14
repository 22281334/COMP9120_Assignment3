'''
List all the user associated issues in the database for a given user
See assignment description for how to load user associated issues based on the user id (user_id)
'''
from Assignment3_PythonSkeleton.database import openConnection


def findUserIssues(user_id):
    # TODO - list all user associated issues from db using sql
    print(user_id)
    conn = openConnection()
    curs = conn.cursor()
    curs.execute("""select issue_id, title, a.username as creator, b.username as resolver, c.username as verifier, description
                    from (select * from a3_issue where creator = %s or resolver = %s or verifier = %s) a3_issue_new 
                    join a3_user a on (a3_issue_new.creator = a.user_id) join a3_user b on (a3_issue_new.resolver = b.user_id)
                    join a3_user c on (a3_issue_new.verifier = c.user_id) 
                    order by title""", (user_id,user_id,user_id,))
    issue_db = curs.fetchall()

    issue = [{
        'issue_id': str(row[0]),
        'title': row[1],
        'creator': row[2],
        'resolver': row[3],
        'verifier': row[4],
        'description': row[5]
    } for row in issue_db]
    curs.close()
    conn.close()
    return issue if issue else None


'''
Find the associated issues for the user with the given userId (user_id) based on the searchString provided as the parameter, and based on the assignment description
'''
def findIssueBasedOnExpressionSearchOnTitle(searchString):

    # TODO - find necessary issues using sql database based on search input
    print("search string '" + searchString + "'")

    conn = openConnection()
    curs = conn.cursor()
    curs.execute("""select issue_id, title, a.username as creator, b.username as resolver, c.username as verifier, description
                    from (select * from a3_issue where position(%s in title) > 0) a3_issue_new 
                    join a3_user a on (a3_issue_new.creator = a.user_id) join a3_user b on (a3_issue_new.resolver = b.user_id)
                    join a3_user c on (a3_issue_new.verifier = c.user_id) 
                    order by title;""", (searchString,))
    issue_db = curs.fetchall()

    issue = [{
        'issue_id': str(row[0]),
        'title': row[1],
        'creator': row[2],
        'resolver': row[3],
        'verifier': row[4],
        'description': row[5]
    } for row in issue_db]
    curs.close()
    conn.close()
    return issue if issue else None

#####################################################
##  Issue (new_issue, get all, get details)
#####################################################
#Add the details for a new issue to the database - details for new issue provided as parameters
def addIssue(title, creator, resolver, verifier, description):
    # TODO - add an issue
    # Insert a new issue to database
    # return False if adding was unsuccessful
    # return True if adding was successful
    conn = openConnection()
    curs = conn.cursor()
    curs.callproc('issue_insert',[title, creator, resolver, verifier, description])
    conn.commit()
    output = curs.fetchone()
    result = output[0]
    curs.close()
    conn.close()
    if result == 0:
        return False
    else:
        return True