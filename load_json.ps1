cd 'C:\Program Files\MongoDB\Server\3.4\bin\'
invoke-item .\mongod.exe
.\mongoimport --db project_4 --collection tweets --drop --file "C:/SMU/2017 Spring/File Organization and Database Management/mini_project_4/mongo_tweets/json_tweets.txt"