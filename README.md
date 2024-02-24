# Friendzone: Our iNTUition hack

Spot and block 'fake friend' call scammers with the power of AI and Automation.

## Installation guide

1. Install requirements.txt  
  `pip install -r requirements.txt`
2. Set up Twilio:  
  Create an account and set up the "Voice" service.
  `export TWILIO_ACCOUNT_SID=<your id here>`  
  `export TWILIO_AUTH_TOKEN=<your token here>`
3. Set up ngrok:  
  `ngrok config add-authtoken <your token here>`
4. Set up GPT:  
  `export OPENAI_API_KEY=<your key here>`
  
## Inspiration
In 2023 alone, there has been 46,563 reported scam cases - a 50% rise from 2022 - and more than $650 million has been lost to such scams. By far the fastest rising group of scams so far are "fake friend" call scams, which have risen 225% in the past year.

There are not many ways to counter such scams - rule-based and blacklist-based softwares such as ScamShield are unable to keep up with the vast amounts of new phone numbers used for scamming, and no existing approach is able to filter the call by what the scammer says to block the call in this manner to block such a scam.

## What it does
FriendZone is a service that allows users to use a protected phone number. 
- These phone numbers will use an automated platform (Twilio) to make all first-time callers say their name, which will be recorded by speech recognition software.
- The call is routed for the actual user to pick up and is monitored in real time by AI (powered by GPT). 
- If the AI detects anomalous behaviour by the caller, such as repeatedly asking for the user to guess their name, the call will be flagged and ended automatically.
- If the AI detects names being used that are different from the initial name given, the call will also be flagged. 

## How we built it
We used Twilio to control the protected numbers, allowing us to use basic text to speech functions, stream the call to Flask for further processing, as well as dial a real phone number to as to forward the call. On the processing side, we used Vosk to recognize the speech said, then used GPT-4 to parse what was said to determine if the caller is indeed a scammer or not.

## Check out our [Devpost](https://devpost.com/software/friendzone-wfhiav)!
