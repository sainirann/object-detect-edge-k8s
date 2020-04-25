# object-detect-edge-k8s

    An object detection system which can be used for edge analytics. The system is deployed on kubernetes near edge and the edge device can utilize this to perform analytics close to edge.
    
    
## mobile-client
    Contains the edge application which is an android application which can capture and send images.
    
## server
    The Server folder contains the server components for the object detection system.
    
### app-server
    The application server which is exposed as a webserver which the mobile client can communicate with. Uses the model server
    to perform predictions and analyze them
    
### tfmodelserver
     The tensorflow model server which serves the SSD MobileNet COCO model v1

### email-notifier
     app-server uses the email notifier to send emails after the predictions are analyzed
