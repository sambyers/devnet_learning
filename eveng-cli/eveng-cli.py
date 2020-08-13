'''eveng python cli'''
'''
login
curl -s -b /tmp/cookie -c /tmp/cookie -X POST -d '{"username":"admin","password":"eve"}' http://127.0.0.1/api/auth/login

logout
curl -s -c /tmp/cookie -b /tmp/cookie -X GET -H 'Content-type: application/json' http://127.0.0.1/api/auth/logout

get folders
curl -s -c /tmp/cookie -b /tmp/cookie -X GET -H 'Content-type: application/json' http://127.0.0.1/api/folders/User1

get nodes in lab
curl -s -c /tmp/cookie -b /tmp/cookie -X GET -H 'Content-type: application/json' http://127.0.0.1/api/labs/User1/Lab%201.unl/nodes
curl -s -c /tmp/cookie -b /tmp/cookie -X GET -H 'Content-type: application/json' http://127.0.0.1/api/labs/User1/BASE-10-ROUTER-LAB.unl/nodes
'''

