import json
import boto3
import urllib.request
import urllib

# Enter your AlphaVantage API Key here

API_KEY = ''

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    
    query = urllib.parse.quote(event['queryStringParameters']['query'])
   
    response = client.get_item(TableName='stockmarket_symbols', Key={'name':{'S':query.upper()}})
    symbol = ""
    if len(response) == 1:
        url = "https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={}&apikey={}".format(query, API_KEY)
        f = urllib.request.urlopen(url)
        result = json.loads(f.read().decode("utf-8"))
        symbols = result['bestMatches']
        if len(symbols) == 0:
            return {
                'statusCode': 200,
                'headers': {
                    "Access-Control-Allow-Headers" : "Content-Type",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                },
                'body': json.dumps("NULL")
            }
        symbol = symbols[0]['1. symbol']
        client.put_item(TableName='stockmarket_symbols', Item={'name':{'S':query.upper()},'symbol':{'S':symbol}})
    else:
        #print(response['Item']['symbol'])
        symbol = response['Item']['symbol']['S']
    
    # TODO implement
    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        },
        'body': json.dumps(symbol)
    }
