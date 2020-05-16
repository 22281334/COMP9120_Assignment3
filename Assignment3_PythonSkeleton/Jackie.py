
def addIssue(title, creator, resolver, verifier, description):

    # TODO - add an issue

    conn = openConnection()
    try：
        curs = conn.cursor()
        curs.execute("""INSERT INTO A3_ISSUE(TITLE, DESCRIPTION, CREATOR, RESOLVER, VERIFIER) VALUES (%s, %s, %s, %s, %s)""")
        print("New issue has been added successfully!")
        return True

    except:
        print("Your issue was added unsuccessfully!")
        return False

    finally:
        curs.close()
        conn.close()

# Update the details of an issue having the provided issue_id with the values provided as parameters
def updateIssue(issue_id, title, creator, resolver, verifier, description):

    # TODO - update the issue using db

    conn = open.Connection
    try:
        curs = conn.cursor
        cur.execute("""UPDATE A3_ISSUE SET TITLE = %S, DESCRIPTION = %s, CREATOR = %s, RESOLVER = %s, VERIFIER = %s WHERE ISSUE_ID = %s""")
        print("Your issue has been updated successfully!")
        return True

    except:
        return False

    finally:
        curs.colse()
        conn.colse()
