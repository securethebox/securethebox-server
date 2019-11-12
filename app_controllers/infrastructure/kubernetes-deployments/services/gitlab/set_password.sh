#!/bin/bash

docker exec cf23bfaab93c gitlab-rails runner -e production "user = User.where(id: 1).first; user.password = user.password_confirmation = 'Changeme'; user.save!"