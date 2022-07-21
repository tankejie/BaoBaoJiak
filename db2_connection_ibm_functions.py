#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import sys
import ibm_db

def main(param):
    
    dsn_hostname = "19af6446-6171-4641-8aba-9dcff8e1b6ff.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud"# e.g.: "dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net"
    dsn_uid = "cgs73238"# e.g. "abc12345"
    dsn_pwd = "SW5A3Om5yInzrecg"# e.g. "7dBZ3wWt9XN6$o0J"
    
    dsn_driver = "{IBM DB2 ODBC DRIVER}"
    dsn_database = "bludb"            # e.g. "BLUDB"
    dsn_port = "30699"                # e.g. "50000" 
    dsn_protocol = "TCPIP"            # i.e. "TCPIP"
    dsn_security = "SSL"
    
    dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};"
    "SECURITY={7};").format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd, dsn_security)
         
    try:
        conn = ibm_db.connect(dsn, "", "")
        print("Connected to database: ", dsn_database, "as user: ", dsn_uid, "on host: ", dsn_hostname)

    except:
        print("no connection:", ibm_db.conn_errormsg())

   
    # Execute the statement
    rating = param["sys_number"]
    #rating = 4
    feedback = param["feedback"]
    #positivefeedbacks = "awesome"
    query_str = f"insert into cgs73238.feedback_rating values ('{rating}','{feedback}')"
    selectQuery = query_str
    selectStmt = ibm_db.exec_immediate(conn, selectQuery)
    
        return {'message': 'Thank you for your positive feedbacks. We are happy that you enjoyed Bao Bao Jiak app.'}