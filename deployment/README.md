### Deployment pipeline
1. On push to test branch, github actions runs necessary tests
2. When they succeed, the changes get merged to master
3. On merge to master, github webhook sends a POST request to the specified URL
4. On reception of the POST request from github, the server fires the following things:
    a. git pull from master
    b. builds new docker image
    c. brings down current docker image
    d. runs new docker image
