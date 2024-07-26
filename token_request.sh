#!/bin/bash

USERNAME=$1
PASSWORD=$2
CLIENT_ID=$3
CLIENT_SECRET=$4
TOKEN_URL=$5

RESPONSE=$(curl -X POST "$TOKEN_URL" --silent \
  -d "grant_type=password" \
  -d "client_id=$CLIENT_ID" \
  -d "client_secret=$CLIENT_SECRET" \
  -d "username=$USERNAME" \
  -d "password=$PASSWORD")

ACCESS_TOKEN=$(echo $RESPONSE | jq -r '.access_token')

echo "access_token=$ACCESS_TOKEN" >> $GITHUB_OUTPUT