import json
import urllib.request

# Enter your AlphaVantage API Key here

API_KEY = ''

def lambda_handler(event, context):
    symbol = event['queryStringParameters']['symbol']
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&apikey={}".format(symbol, API_KEY)
    f = urllib.request.urlopen(url)
    print(url)
    try:
        result = json.loads(f.read().decode("utf-8"))
        print((result))
        if result['Time Series (Daily)'] is None:
            return {
                'statusCode': 200,
                'headers': {
                    "Access-Control-Allow-Headers" : "Content-Type",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                },
                'body': json.dumps('ERROR')
            }
        print(('aaaaa'))
        res = []
        for d in result['Time Series (Daily)'].items():
            #res['{}'.format(d[0])] = d[1]['4. close']
            obj = {
                "x" : d[0],
                "y" : d[1]['4. close']
            }
            res.append(obj)
    except Exception as e:
        return {
        'statusCode': 500,
        'headers': {
                    "Access-Control-Allow-Headers" : "Content-Type",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                },
        'body': json.dumps(str(e))
        }
    res = res[::-1]
    # TODO implement
    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        },
        'body': json.dumps(res[-30:])
    }
