const randomBytes = require('crypto').randomBytes;
const AWS = require('aws-sdk');
const ddb = new AWS.DynamoDB.DocumentClient();


exports.handler = (event, context, callback) => {

  const recordId = toUrlString(randomBytes(16));
  console.log('Received event (', recordId, '): ', event);

  // The body field of the event in a proxy integration is a raw string.
  // In order to extract meaningful values, we need to first parse this string
  // into an object. A more robust implementation might inspect the Content-Type
  // header first and use a different parsing strategy based on that value.
  const requestBody = JSON.parse(event.body);

  const carId = requestBody.CarId;
  const gpsCoords = requestBody.GpsCoords;
  const speed = requestBody.Speed;
  const fuelLevel = requestBody.FuelLevel;
  const engineStatus = requestBody.EngineStatus;
  const odometerReading = requestBody.OdometerReading;
  const internalCarTemp = requestBody.InternalCarTemp;
  const externalTemp = requestBody.ExternalTemp;
  const weatherConditions = requestBody.WeatherConditions;
  const maintenanceAlerts = requestBody.MaintenanceAlerts;



  // create a single record with above details
  const recordItem = {
    RecordId: recordId,
    CarId: carId,
    GpsCoords: gpsCoords,
    Speed: speed,
    FuelLevel: fuelLevel,
    EngineStatus: engineStatus,
    OdometerReading: odometerReading,
    InternalCarTemp: internalCarTemp,
    ExternalTemp: externalTemp,
    WeatherConditions: weatherConditions,
    MaintenanceAlerts: maintenanceAlerts,
  };



  recordRide(recordItem).then(() => {
    // You can use the callback function to provide a return value from your Node.js
    // Lambda functions. The first parameter is used for failed invocations. The
    // second parameter specifies the result data of the invocation.

    // Because this Lambda function is called by an API Gateway proxy integration
    // the result object must use the following structure.
    callback(null, {
      statusCode: 201,
      body: JSON.stringify({
        Item: recordItem,
        Message: 'Successfully created record',
      }),
      headers: {
        'Access-Control-Allow-Origin': '*',
      },
    });
  }).catch((err) => {
    console.error(err);

    // If there is an error during processing, catch it and return
    // from the Lambda function successfully. Specify a 500 HTTP status
    // code and provide an error message in the body. This will provide a
    // more meaningful error response to the end client.
    errorResponse(err.message, context.awsRequestId, callback)
  });
};


function recordRide(recordItem) {
  return ddb.put({
    TableName: 'VehicleTelemetry-dev',
    Item: recordItem,
  }).promise();
}

function toUrlString(buffer) {
  return buffer.toString('base64')
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=/g, '');
}

function errorResponse(errorMessage, awsRequestId, callback) {
  callback(null, {
    statusCode: 500,
    body: JSON.stringify({
      Error: errorMessage,
      Reference: awsRequestId,
    }),
    headers: {
      'Access-Control-Allow-Origin': '*',
    },
  });
}