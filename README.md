# Simple Python-Flask REST API demo for use on CSC Rahti

## 1. On rahti.csc.fi Openshift Web Console:
- Create python-project on CSC Rahti (use github repo over https)
- Set any environment variables you need, _Builds/ [your app]/ Environment_
- When the first build is complete, find the Webhook url (_Builds/ [your app]/ Configuration_)

## 2. On Github (setup push-to-deploy)
- Copy-paste the GitHub Webhook URL from Rahti to the GitHub-repo: _Settings/ Webhooks/ New Webhook_. 
- Set Webhook Content type to _application/json_

### Note
- Make sure your default branch is named `master` not `main`.
- Rahti wants your app to listen on port 8080 (can be changed under _Routes_)
- To run you app over SSL (https) just enable it in you Route (Applications/Routes) by enabling "Secure Route" (you can also set "Insecure Traffic" to _redirect_ or _allow_)
- The `.devcontainer` folder is a VSCode thing, not needed for Rahti. 



