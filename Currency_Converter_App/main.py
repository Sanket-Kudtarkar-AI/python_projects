'''This is main python flask application file , programme execution starts from here'''

# importing all dependencies
from flask import Flask,render_template,request
import requests
import os

# creating a Flask app and name it 'app'
app = Flask(__name__)

# api key taken from 'www.alphavantage.co' 
if 'API_KEY' in os.environ:
    API_KEY = os.environ['API_KEY']
else:
    API_KEY = '61HB6H2OO2BXNM8Q'

# default ('/') route of the application
@app.route('/',methods=['GET','POST'])
def home():
    # this part executes when users make a POST request to the server
    if request.method == 'POST':
        try:
            # extracting data (include --> amount:given amount,from_c:convert from which currency,to_c:convert to which currency) given by user to the server
            amount = request.form['amount']
            amount = float(amount)
            from_c = request.form['from_c']
            to_c = request.form['to_c']

            # making of the proper url before create a GET request to 'www.alphavantage.co' api service
            url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={}&to_currency={}&apikey={}'.format(from_c,to_c,API_KEY)
            
            # make the GET request to 'www.alphavantage.co' api service and then store the Response to 'response' variable
            response = requests.get(url=url).json()

            # calculating the amount according to the Currency Exchange Rate and store the value to 'result' variable 
            rate = response['Realtime Currency Exchange Rate']['5. Exchange Rate']
            rate = float(rate)
            result = rate * amount

            # Extracting all other necessary information from 'response' to display in web-page
            from_c_code = response['Realtime Currency Exchange Rate']['1. From_Currency Code']
            from_c_name = response['Realtime Currency Exchange Rate']['2. From_Currency Name']
            to_c_code = response['Realtime Currency Exchange Rate']['3. To_Currency Code']
            to_c_name = response['Realtime Currency Exchange Rate']['4. To_Currency Name']
            time = response['Realtime Currency Exchange Rate']['6. Last Refreshed']

            # finally it returns to home page of application with essential information for displaying to user 
            return render_template('home.html', result=round(result,2), amount=amount,
                                    from_c_code=from_c_code, from_c_name=from_c_name, 
                                    to_c_code=to_c_code, to_c_name=to_c_name, time=time)
        
        # This part executes if server fails to response then display an Error Message
        except Exception as e:
            return '<h1>Bad Request : {}</h1>'.format(e)
    
    # if user make a simple GET request to this server it returns 'home.html' page
    else:
        return render_template('home.html')



# Running the server/app, when this file will be executed/run
if __name__ == "__main__":
    app.run(debug= True)
