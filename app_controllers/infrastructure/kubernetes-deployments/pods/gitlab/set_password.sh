#!/bin/bash

docker exec 26fc4c0a614d gitlab-rails runner -e production "user = User.where(id: 1).first; user.password = user.password_confirmation = 'Changeme'; user.save!"