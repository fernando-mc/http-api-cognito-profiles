// Load the AWS SDK for JS
var AWS = require("aws-sdk");

// Set a region to interact with (make sure it's the same as the region of your table)
AWS.config.update({region: 'us-east-1'});

// Set a table name that we can use later on
const tableName = process.env.DYNAMODB_TABLE

// Create the Document Client interface for DynamoDB
var dynamodb = new AWS.DynamoDB.DocumentClient();


module.exports.create = async function(event, context) {
    const user_sub = event['requestContext']['authorizer']['claims']['sub']
    const profile_data = JSON.parse(event['body'])
    const item = {
        'pk': 'USERS#ALL',
        'sk': 'USER#' + user_sub,
        'profile_data': profile_data
    }
    const putParams = {
        TableName: tableName,
        Item: item
    }
    try {
        await dynamodb.put(putParams).promise()
        return {
            "statusCode": 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            "body": JSON.stringify(item)
        }
    } catch (error) {
        console.log(error)
        throw new Error(error)
    }
}

module.exports.get = async function(event, context) {
    const user_sub = event['requestContext']['authorizer']['claims']['sub']
    const getParams = {
        TableName: tableName,
        Key: {
            'pk': 'USERS#ALL',
            'sk': 'USER#' + user_sub
        }
    }
    let getResult
    try {
        getResult = await dynamodb.get(getParams).promise()
        return {
            "statusCode": 200,
            "body": JSON.stringify(getResult)
        }
    } catch (error) {
        console.log(error)
        throw new Error(error)
    }
}
