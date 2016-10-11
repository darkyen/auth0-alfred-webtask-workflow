Twitter Workflow for Alfred with Auth0
---

This workflow Opens Auth0's Authorize endpoint to authenticate using twitter and get and `access_token` to call the tweeting server which is actually a Webtask. It will store the token in keyring once it has been fetched ones and only re-authenticate
when the token expires.

The OAuth2 Handshake uses PKCE which is a secure way to authenticate native applications like mobile clients or cli apps using a cryptographic challenge. The Python script hosts a single server which will handle the callback url.

@Todo: Use `refresh_tokens` to keep the session
