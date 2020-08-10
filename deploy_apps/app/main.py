from flask import Flask
from subprocess import check_output
import mysql.connector


app = Flask(__name__)
mydb = mysql.connector.connect(
    host='172.20.0.200',
    database='inventory',
)
mycursor = mydb.cursor()

@app.route('/')
def index():
    mycursor.execute("SELECT * FROM inventory.routers")
    routers = mycursor.fetchall()
    ip = check_output(['hostname', '--all-ip-addresses'])
    out = (
        'DevNet<br>'
        f'This container is using the IP address {ip}<br>'
    )
    out += 'List of routers in inventory:<br>'
    for r in routers:
        out += f'-> Hostname: {r[0]}, IP: {r[1]}<br>'
    return out


if __name__ == '__main__':
    app.run(host='0.0.0.0')