var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var jwt = require('express-jwt');
var rsaValidation = require('auth0-api-jwt-rsa-validation');
var Webtask = require('webtask-tools');

const request = require('request-promise');
const Twitter = require('twit@2.2.3')


var jwtCheck = jwt({
  secret: rsaValidation(),
  algorithms: ['RS256'],
  issuer: "https://alfred3-sample.auth0.com/",
  audience: 'https://twitter.webtask/'
});

app.use(jwtCheck);
app.use(bodyParser.json());

app.post('/tweet', function (req, res) {
  // 140 chars... sure!
  const userId = req.user.sub;
  const status = req.body.status;
  const secrets = req.webtaskContext.secrets;
  console.log("tweeting ", status);
  const MGMT_API_TOKEN          = secrets.MGMT_API_TOKEN; // Key from MGMT api console with read:idp_access_tokens
  const AUTH0_DOMAIN            = secrets.AUTH0_DOMAIN;   // if your domain is some-game.auth0.com it should be some-game
  const TWITTER_CONSUMER_KEY    = secrets.TWITTER_CONSUMER_KEY;    // Twitter consumer key
  const TWITTER_CONSUMER_SECRET = secrets.TWITTER_CONSUMER_SECRET; // Twitter consumer secret 
  
  function handleFailure(error){
    console.log(error);
    return res.status(500).json({
      message: error.message
    });
  }

  request.get(`https://${AUTH0_DOMAIN}/api/v2/users/${userId}`,{
    headers: {
        'Authorization': `Bearer ${MGMT_API_TOKEN}`
    },
    json: true
  }).then(function(user){
    
      const twitterUser = user.identities.filter(function(identity){
         return identity.provider === 'twitter'; 
      })[0];
      
    
      const client = new Twitter({
          consumer_key:         TWITTER_CONSUMER_KEY,
          consumer_secret:      TWITTER_CONSUMER_SECRET,
          access_token:         twitterUser.access_token,
          access_token_secret:  twitterUser.access_token_secret,
      });
      
      client.post('statuses/update', {
        status: status
      }).then(function(tres){
        return res.status(200).json({
          message: 'Ok',
          res: tres.resp
        });
      }, handleFailure);
  }, handleFailure);
  
});

module.exports = Webtask.fromExpress(app);
