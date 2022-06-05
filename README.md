# SlackBot
A basic implementation of SlackBot using Django and Slack API

The project includes desiging and building a SlackBot integrated with a simple Django based Backend and Postgresql Database.

The Database is modeled through 3 different Models:  <br />
1- UserInformation = This table stores user data when hey call the SlackBot. The feilds in this table includes userId(Id linked with Slack), Username(Slack UserName), Fullname, Email and password. <br />
2- MessageInformation = This tables includes a Author(UserId of the user sending the message), TestMessage, Timestamp and Channel in which the message is sent. <br />
3- Uploads = This tables stores all the data related to files and media sent in the Slack Workspace. This stores the Title of the file being sent, fileId associated with Slack and File which stores the path where File is saved. <br />

SlackBot is able to perform some pre-defined tasks which can be triggered by sent specific keywords.  <br />Below is a list of all the commands which can be sent as text messages and SlackBot willbe triggered:
1. @SlackBot = When the slackbot is mentioned without any text, it stores the information of user in UserInformation Table.
2. -setpassword <enter your new password with a single space> = This commands stores the password of the user. The user is required to give not more than 1 space between <br />
    setpassword and users password.  <br />
3. -updatepassword <enter previous password> <enter new password> = This commands updates the users password. Previous password is used for authetication purpose.  <br />
4. -getconversationhistory = Returns a list of all the messages sent by the user calling this command. All the messages will be sent from the channels, which the SlackBot is part of.  <br />
5. -uploadfile = This command must be sent as a text message when any file is uploaded to slack channel. This command stores the media file in the server.
6. -deletefile <enter the file name with media extension as well> = This command requires the user to enter the file that must be deleted from server. User is required to provide the file with its extension as well.  <br />
7. -getfile <enter the file name with media extension as well> = Using this command, file is retreived from the server and sent to the user calling this command.  <br />

Note: All the messages sent by the SlackBot are sent to the DM Channel between the SlackBot and User.
