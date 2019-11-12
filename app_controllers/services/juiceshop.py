# Keep up with latest juice-shop builds
"""
git clone https://github.com/bkimminich/juice-shop.git
cd ./juice-shop
rm -rf .git
git init
npm install nodemon node-serialize@0.0.4 csurf node-vault --save


EDIT package.json:

"start": "nodemon app",

EDIT Dockerfile:

FROM node:8-jessie as installer
FROM node:8-jessie
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get install -y nodejs
RUN apt-get update
RUN useradd -ms /bin/bash juicer
RUN usermod -a -G juicer juicer
RUN chown -R juicer /juice-shop
RUN chgrp -R 0 /juice-shop/
CMD DEBUG=express:* nodemon app.js


EDIT server.js:

/* backdoor for RCE */
const escape = require('escape-html')
const serialize = require('node-serialize');

app.get('/backdoor', function(req, res) {
  if (req.cookies.profile) {
    var str = new Buffer(req.cookies.profile, 'base64').toString();
    var obj = serialize.unserialize(str);
    if (obj.username) {
      res.send("Hello " + escape(obj.username));
    }
  } else {
      res.cookie('profile', "eyJ1c2VybmFtZSI6ImFqaW4iLCJjb3VudHJ5IjoiaW5kaWEiLCJjaXR5IjoiYmFuZ2Fsb3JlIn0=", {
        maxAge: 900000,
        httpOnly: true
      });
  }
  res.send("I'm a backdoor");
 });

 /


"""