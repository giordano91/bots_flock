# bots_flock
A simple way to create posts and interact to other users on different social platforms.  
The supported social platforms are:
- Twitter (IN PROGRESS)
- Telegram (TODO)
- Instagram (TODO)

This application is composed by several Docker containers. Each container represents a bot. Each bot has been created as CLI (Command Line Interface) application.  
In this way using different parameters it is possible to configure what the bot must do.  
Being organized in containers, it is easily possible to enable or disable the container according to your needs.  

## Twitter bot
This bot has the following options:
- **-kt** or **--keywords_to_track**: use this parameter to specify the list of keywords to track  
  example:  
  -kt python #docker  
  Using this configuration just the tweets which contain *python* or *#docker* keyword will be considered  
- **-lt** or **--languages_to_track**: use this parameter to specify the list of languages to track
  example:  
  -lt en  
  Using this configuration just the tweets in english will be considered  
- **-l** or **--like_tweet**: if this parameter is present, a like is left on tweets that match keywords and languages  
  example:  
  -l  

### How to use Twitter bot?
To use this bot you need to have Twitter API credentials ([Twitter API link](https://developer.twitter.com/en/docs/twitter-api)).  
Then, create a file called **.env** in the root of the project (copy the content from the **.env.sample** file present in the project).  
Fill up all the required information being careful not to put your credentials in double/sigle quotes.  

Before to start the bot please check the docker-compose file.  
In the *twitter_bot* section there is a subsection called *command*. Here you will find all the options passed as input to the bot.  
Please configure it as you like it.  

Once the configuration is done, it is possible to proceed in the following way:

    cd bots_flock   
    docker-compose build  
    docker-compose up  

At this point the bot is started.   





