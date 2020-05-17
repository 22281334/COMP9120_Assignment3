#!/usr/bin/env python3
import psycopg2

#####################################################
##  Database Connect
#####################################################

'''
Connects to the database using the connection string
'''


def openConnection():
    # connection parameters - ENTER YOUR LOGIN AND PASSWORD HERE
    # TODO -

    userid = "y20s1c9120_qyan5974"
    passwd = "490332368"
    myHost = "soit-db-pro-2.ucc.usyd.edu.au"

    # Create a connection to the database
    conn = None
    try:
        # Parses the config file and connects using the connect string
        conn = psycopg2.connect(database=userid,
                                user=userid,
                                password=passwd,
                                host=myHost)
    except psycopg2.Error as sqle:
        print("psycopg2.Error : " + sqle.pgerror)

    # return the connection to use
    return conn


'''
List all the user associated issues in the database for a given user 
See assignment description for how to load user associated issues based on the user id (user_id)
'''


def checkUserCredentials(userName):
    userInfo = []
    conn = openConnection()
    try:
        curs = conn.cursor()
        # execute the query
        curs.execute("SELECT USER_ID,USERNAME,FIRSTNAME,LASTNAME FROM a3_user")

        #  loop through the resultset
        nr = 0
        row = curs.fetchone()
        nameState = False
        while row is not None:
            nr += 1
            if userName == row[1]:
                nameState = True
                userInfo = [str(row[0]), str(row[1]), str(row[2]), str(row[3])]
            row = curs.fetchone()

        if nr == 0:
            print("No entries found.")

        # clean up! (NOTE this really belongs in a finally block)
        curs.close()

    except psycopg2.Error as sqle:
        print("psycopg2.Error : " + sqle.pgerror)
    if nameState == True:
        return userInfo
    else:
        return


'''
List all the user associated issues in the database for a given user 
See assignment description for how to load user associated issues based on the user id (user_id)
'''
def findUserIssues(user_id):
    # TODO - list all user associated issues from db using sql
    print(user_id)
    conn = openConnection()
    try:
        curs = conn.cursor()
        curs.execute("""select issue_id, title, a.username as creator, b.username as resolver, c.username as verifier, description
                    from (select * from a3_issue where creator = %s or resolver = %s or verifier = %s) a3_issue_new 
                    join a3_user a on (a3_issue_new.creator = a.user_id) 
                    join a3_user b on (a3_issue_new.resolver = b.user_id)
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
        return issue
    except:
        print("error")

'''
Find the associated issues for the user with the given userId (user_id) based on the searchString provided as the parameter, and based on the assignment description
'''


def findIssueBasedOnExpressionSearchOnTitle(searchString):

    # TODO - find necessary issues using sql database based on search input

    print("search string '" + searchString + "'")

    conn = openConnection()
    try:
        curs = conn.cursor()
        curs.execute("""select issue_id, title, a.username as creator, b.username as resolver, c.username as verifier, description
                    from (select * from a3_issue where position(%s in title) > 0) a3_issue_new 
                    join a3_user a on (a3_issue_new.creator = a.user_id) 
                    join a3_user b on (a3_issue_new.resolver = b.user_id)
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
        return issue
    except:
        print("error")

###

#####################################################
##  Issue (new_issue, get all, get details)
#####################################################
# Add the details for a new issue to the database - details for new issue provided as parameters
def addIssue(title, creator, resolver, verifier, description):
    # TODO - add an issue
    # Insert a new issue to database
    # return False if adding was unsuccessful
    # return True if adding was successful

    conn = openConnection()
    try:
        curs =conn.cursor()
        insert_query = """INSERT INTO a3_issue(title, description, creator, resolver, verifier) VALUES (%s, %s, %s, %s, %s)"""
        insert_data = (title, description, creator, resolver, verifier)
        curs.execute(insert_query, insert_data)
        conn.commit()

    except psycopg2.Error as e:
        conn.rollback()
        return False

    finally:
        curs.close()
        conn.close()
        return True


# Update the details of an issue having the provided issue_id with the values provided as parameters
def updateIssue(issue_id, title, creator, resolver, verifier, description):
    # TODO - update the issue using db
    # return False if adding was unsuccessful
    # return True if adding was successful

    conn = openConnection()
    try:
        curs =conn.cursor()
        update_query = """UPDATE a3_issue SET title = %s, description = %s, creator = %s, resolver = %s, verifer = %s WHERE issue_id = %s"""
        update_data = (title, description, creator, resolver, verifier, issue_id)
        curs.excute(update_query, update_data)
        conn.commit()

    except psycopg2.Error as e:
        conn.rollback()
        return False

    finally:
        curs.close()
        conn.close()
        return True
