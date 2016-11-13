Twitter Workflow for Alfred with Auth0
---


### How to use 

CMD + SPACE / CMD + OPTION + SPACE 
`twt Twitter clients are modern day Hello world! :boom:`

### How it works?
This workflow Opens [Auth0](https://auth0.com/)'s Authorize endpoint to authenticate using twitter and get and `access_token` to call the resource server which is secretly a [Webtask](https://webtask.io). The Python script hosts a single server which will handle the callback url. The OAuth2 Handshake uses PKCE which is a secure way to authenticate native applications like mobile clients or cli apps using a cryptographic challenge.


### Future work

- @Todo: Use `refresh_tokens` to keep the session.
- @Todo: Add workflow for signout.
- @Todo: Add Search for tweets/users/hashtags.
