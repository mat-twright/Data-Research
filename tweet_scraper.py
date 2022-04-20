import tweepy #https://github.com/tweepy/tweepy
import csv

#Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""


def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method

	#authorize twitter, initialize tweepy
    auth = tweepy.OAuth2AppHandler("qqLpS9SikkE1wvYamVQujUaqu", "zjVex6MmUy8590ZUAJEgpsaOGRLhwg3nyJtpok0SOJI2pr1Gwe")
    api = tweepy.API(auth)

	#initialize a list to hold all the tweepy Tweets
    alltweets = []

	#make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)

	#save most recent tweets
    alltweets.extend(new_tweets)

	#save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

	#keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
    	print("getting tweets before {}".format(oldest))

    	#all subsiquent requests use the max_id param to prevent duplicates
    	new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

    	#save most recent tweets
    	alltweets.extend(new_tweets)

    	#update the id of the oldest tweet less one
    	oldest = alltweets[-1].id - 1

    	print("...{} tweets downloaded so far".format(len(alltweets)))

    #transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]

	#write the csv
    with open('{}_tweets.csv'.format(screen_name), 'w') as f:
    	writer = csv.writer(f)
    	writer.writerow(["id","created_at","text"])
    	writer.writerows(outtweets)
    	print('{}_tweets.csv was successfully created.'.format(screen_name))
    pass


if __name__ == '__main__':
    #pass in the username of the account you want to download
    get_all_tweets("RUN_Store")
