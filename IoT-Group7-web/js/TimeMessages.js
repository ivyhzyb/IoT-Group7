// Browser based Thing Shadow Updater

/*
* Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
*
* Licensed under the Apache License, Version 2.0 (the "License").
* You may not use this file except in compliance with the License.
* A copy of the License is located at
*
*  http://aws.amazon.com/apache2.0
*
* or in the "license" file accompanying this file. This file is distributed
* on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
* express or implied. See the License for the specific language governing
* permissions and limitations under the License.
*/

// Instantiate the AWS SDK and configuration objects.  The AWS SDK for 
// JavaScript (aws-sdk) is used for Cognito Identity/Authentication, and 
// the AWS IoT SDK for JavaScript (aws-iot-device-sdk) is used for the
// WebSocket connection to AWS IoT and device shadow APIs.
var AWS = require('aws-sdk');
var AWSIoTData = require('aws-iot-device-sdk');

// Set Thing name constant
const thingName = "Door_Sensor";

// Initialize the configuration.
AWS.config.region = AWSConfiguration.region;

AWS.config.credentials = new AWS.CognitoIdentityCredentials({
   IdentityPoolId: AWSConfiguration.poolId
});

// Keep track of whether or not we've registered the shadows used by this
// example.
var shadowsRegistered = false;

// Attempt to authenticate to the Cognito Identity Pool.
var cognitoIdentity = new AWS.CognitoIdentity();
AWS.config.credentials.get(function (err, data) {
    if (!err) {
        console.log('retrieved identity from Cognito: ' + AWS.config.credentials.identityId);
        var params = {
            IdentityId: AWS.config.credentials.identityId
        };
        cognitoIdentity.getCredentialsForIdentity(params, function (err, data) {
            if (!err) {

                // Create the AWS IoT shadows object.
                const thingShadows = AWSIoTData.thingShadow({
                    // Set the AWS region we will operate in.
                    region: AWS.config.region,

                    //Set the AWS IoT Host Endpoint   
                    host: AWSConfiguration.endpoint,

                    // Use a random client ID.
                    clientId: thingName + '-' + (Math.floor((Math.random() * 100000) + 1)),

                    // Connect via secure WebSocket
                    protocol: 'wss',

                    // Set the maximum reconnect time to 8 seconds; this is a browser application
                    // so we don't want to leave the user waiting too long for re-connection after
                    // re-connecting to the network/re-opening their laptop/etc...
                    maximumReconnectTimeMs: 8000,

                    // Set Access Key, Secret Key and session token based on credentials from Cognito
                    accessKeyId: data.Credentials.AccessKeyId,
                    secretKey: data.Credentials.SecretKey,
                    sessionToken: data.Credentials.SessionToken
                });

                // Update Armed image whenever we receive status events from the shadows.
                thingShadows.on('status', function (thingName, statusType, clientToken, stateObject) {
                    console.log('status event received for my own operation')
                    if (statusType === 'rejected') {
                        // If an operation is rejected it is likely due to a version conflict;
                        // request the latest version so that we synchronize with the shadow
                        // The most notable exception to this is if the thing shadow has not
                        // yet been created or has been deleted.
                        if (stateObject.code !== 404) {
                            console.log('re-sync with thing shadow');
                            var opClientToken = thingShadows.get(thingName);
                            if (opClientToken === null) {
                                console.log('operation in progress');
                            }
                        }
                    } else { // statusType === 'accepted'
                        if (stateObject.state.hasOwnProperty('reported') && stateObject.state.reported.hasOwnProperty('Armed_Status')) {
                            
                            // Update the messages div with new status
                            //document.getElementById('messages').innerHTML = '<p>Armed_status successfully received.</p><p>Connected to AWS IoT.</p>';
                            
                            //handleArmedImage(stateObject.state.reported.Armed_Status);
                        }
                    }
                });

                // Update Armed image whenever we receive foreignStateChange events from the shadow.
                // This is triggered when the Armed Thing updates its state.
                thingShadows.on('foreignStateChange', function (thingName, operation, stateObject) {
                    console.log('foreignStateChange event received')
                    
                    // If the operation is an update
                    if (operation === "update") {

                        // Make sure the Armed_Status property exists
                        if (stateObject.state.hasOwnProperty('reported') && stateObject.state.reported.hasOwnProperty('Armed_Status')) {
                            //handleArmedImage(stateObject.state.reported.Armed_Status);
                        } else {
                            console.log('no reported Armed_Status state');
                        }
                    }
                });


                // Connect handler; update div visibility and fetch latest shadow documents.
                // Register shadows on the first connect event.
                thingShadows.on('connect', function () {
                    console.log('connect event received');

                    // Update the messages div with new status
                    //document.getElementById('messages').innerHTML = '<p>Connected to AWS IoT. Registering...</p>';

                    // We only register the shadow once.
                    if (!shadowsRegistered) {
                        thingShadows.register(thingName, {}, function (err, failedTopics) {
                            
                            // If there are no errors
                            if (!err) {                    
                                console.log(thingName + ' has been registered');

                                // Update the messages div with new status
                                //document.getElementById('messages').innerHTML = '<p>Registered to ' + thingName + ' Shadow. Fetching the current Armed_Status</p>';

                                // Fetch the initial state of the Shadow
                                var opClientToken = thingShadows.get(thingName);
                                if (opClientToken === null) {
                                    console.log('operation in progress');
                                }
                                shadowsRegistered = true;
                            }
                        });
                    }
                });

                // When the ArmedLightsEventButton is clicked, update the Thing Shadow with the inverse of the 
                // current light status
                const DeviceTimeSetButton = document.getElementById('DeviceTimeSetButton');
                DeviceTimeSetButton.addEventListener('click', (evt) => {
                    StartTime = document.getElementById('time1').value;
                    EndTime = document.getElementById('time2').value;
                    console.log(StartTime);
                    console.log(EndTime);
                    if(StartTime != "" && EndTime != ""){
                        thingShadows.update(thingName, { state: { reported: { Armed_Time: {Start: StartTime, End: EndTime}} } });
                    }
                    else{
                        document.getElementById("ErrorMessage").innerHTML = "\nPlease Select Valid Times"
                    }
                });

            } else {
                console.log('error retrieving credentials: ' + err);
                alert('Error retrieving credentials: ' + err);
            }
        });
    } else {
        console.log('error retrieving identity:' + err);
        alert('Error retrieving identity: ' + err);
    }
});

 // Function handling the Armed image based on the newArmedStatus
function handleArmedImage(newArmedStatus) {

    // Don't do anything if the light status hasn't changed
    if (currentArmedStatus === newArmedStatus) {
        return;
    } else if (newArmedStatus === true) {
        console.log('changing Armed image to Armed ON');

        // Set the Armed image to ON and appropriate text
        document.getElementById("Armed").src="img/element-2-obj-locked.png";
        document.getElementById('lights').innerHTML = '<h1>The Device Is Armed</h1>';

    } else {
        console.log('changing Armed image to lights OFF');
        
        // Set the Armed image to OFF and appropriate text
        document.getElementById("Armed").src="img/element-2-obj-unlocked.png";
        document.getElementById('lights').innerHTML = '<h1>The Device Is Disarmed</h1>';
        
    }

    // Save the new light status
    currentArmedStatus = newArmedStatus;
}
