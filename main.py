from flask import Flask, render_template, redirect, request
import json

app = Flask(__name__)

@app.route('/')
def main_page():
    # Read data from files
    try:
        with open('data.json', 'r') as file:
            data = file.read()
            # convert to json
            data = json.loads(data)
    except Exception as e:
        return 'Data cannot be read from file:' +  str(e)

    return render_template('index.html', result=data)


@app.route('/validate', methods = ['POST'])
def validate():
    # Get id from form seller and product
    item_id = request.form['product']
    seller_id = request.form['seller']
    # load data 
    
    result = "item id: " + item_id + " seller_id "+ seller_id

    try:
        with open('data.json', 'r') as file:
            data = file.read()
            # convert to json
            data = json.loads(data)
    except Exception as e:
        return 'Data cannot be read from file:' + str(e)
    # for item_id obtained on form get seller_id that is authorized to sell product
    
    # find prducts authorized seller
    for i in data['products']:
        if i['id'] == item_id:
            authorized_seller = i['seller_id']

    #check if authorized seller for product matches seller's id selected
    if authorized_seller == seller_id:
        # transaction is ok build dictionary
        result = {"authorized":{"productId": item_id, "authorizedSellerId": seller_id }}
        result = json.dumps(result)
        #respons code 200 - sucess
        return result, 200
    else:
        # transaction is unauthorized
        result = {"unauthorized":{"productId": item_id, "unauthorisedSellerId": seller_id }}
        result = json.dumps(result)
        #unauthorised code
        return result, 401



if  __name__ == '__main__':
    app.run(debug=True)