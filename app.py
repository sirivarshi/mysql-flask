from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import pandas as pd
import io
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Siri@131211'
app.config['MYSQL_DB'] = 'employee'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        details = request.form
        firstName = details['fname']
        lastName = details['lname']
        amount = details["year"]
        amounts = int(amount)
        year = details["year"]


        cur = mysql.connection.cursor()
        cur.execute("CREATE TABLE if not exists MyUser ( firstname VARCHAR(30) NOT NULL,  lastname VARCHAR(30) NOT NULL, amount int(30) not null, year varchar(30) not null)")

        cur.execute("INSERT INTO MyUser(firstName, lastName,amount,year) VALUES (%s, %s, %s, %s)", (firstName, lastName,amounts,year))
        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template('index.html')
@app.route('/display', methods = ["GET","POST"])
def display():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("select year, sum(amount) as total from MyUser group by year")
        result = cur.fetchall()
        df = pd.DataFrame(result,columns=["year","amount"])

        x = df.to_html(header = "true",table_id="table")
        return "success {}".format(x)



@app.route('/print-plot')
def plot_png():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("select year, sum(amount) as total from MyUser group by year")
        result = cur.fetchall()
        df = pd.DataFrame(result,columns=["year","amount"])
        x = df["year"]
        y = df["amount"]
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        xs = np.random.rand(100)
        ys = np.random.rand(100)
        axis.plot(x, y)
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')





@app.route('/graph')
def type():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("select year, sum(amount) as total from MyUser group by year")
        result = cur.fetchall()
        df = pd.DataFrame(result,columns=["year","amount"])











if __name__ == '__main__':
    app.run()