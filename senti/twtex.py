import tweepy
import sys
import datetime
import re

class TwitterClient(object): 
    def __init__(self): 
        # keys and tokens from the Twitter Dev Console 
        consumer_key = 'NkDspb5BLKqwz5sX5Xl5kT8EE'
        consumer_secret = 'NUZmCBUQzlQvXSP9ZZ6htJLalfHMxBBevVSSsBwsjOOWdDfxJZ'
        access_token = '2951604710-Iul8QojD3jPpDF9ZvGKOHvXmfpm0hgnNwstEOBo'
        access_token_secret = 'aB7Pbcw7c9tfku09TMiiuzkkCq5sEMo7AWP10gUdlM5YN'
        
        self.non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)


        try: 
            self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
            self.auth.set_access_token(access_token, access_token_secret)  
            self.api = tweepy.API(self.auth) 
        except: 
            print("Error: Authentication Failed")

    def get_tweets(self, query, count):
        tweets = []
        try:
            fetched_tweets = self.api.search(q=query, count=count, lang="en")

            for tweet in fetched_tweets:
                p_tweet = self.get_tweet_info(tweet.id)
                tweets.append(p_tweet)
                        
            return tweets
            
        except tweepy.TweepError as e: 
                print("Error : " + str(e))

    def get_tweet_info(self, idno):
        try:
            parsed_tweet = {}
            status = self.api.get_status(idno, tweet_mode="extended")
            parsed_tweet['type'] = 0
            try:
                parsed_tweet['text'] = status.retweeted_status.full_text
                retweet_likes = status.retweeted_status.favorite_count
                parsed_tweet['retweet'] = status.retweeted_status.retweet_count
                retweet_date = status.retweeted_status.created_at
                text = status.full_text
                parsed_tweet['type'] = 1
                
            except AttributeError:
                parsed_tweet['text'] = status.full_text
                parsed_tweet['likes'] = status.favorite_count

            if parsed_tweet['type'] == 1 and text[0:4] == "RT @":
                parsed_tweet['type'] = 11
                parsed_tweet['likes'] = retweet_likes
                parsed_tweet['date'] = retweet_date
                parsed_tweet['username'] = status.retweeted_status.user.screen_name
                parsed_tweet['name'] = status.retweeted_status.user.name
                parsed_tweet['propic_url'] = status.retweeted_status.user.profile_image_url
                parsed_tweet['r_username'] = status.user.screen_name
                parsed_tweet['r_name'] = status.user.name
            elif parsed_tweet['type'] == 1:
                parsed_tweet['type'] = 12
                parsed_tweet['likes'] = status.favorite_count
                parsed_tweet['date'] = status.created_at
                parsed_tweet['username'] = status.user.screen_name
                parsed_tweet['name'] = status.user.name
                parsed_tweet['propic_url'] = status.user.profile_image_url
            else:
                parsed_tweet['retweet'] = status.retweet_count
                parsed_tweet['date'] = status.created_at
                parsed_tweet['username'] = status.user.screen_name
                parsed_tweet['name'] = status.user.name
                parsed_tweet['propic_url'] = status.user.profile_image_url
            
            try:
                parsed_tweet['image_url'] = status.entities['media'][0]['media_url_https']
            except KeyError:
                parsed_tweet['image_url'] = None

            parsed_tweet['text'] = re.sub(r'#[\w]+|https:[a-zA-z0-9./]+',"", parsed_tweet['text'])
                    
            
            date_rest = (datetime.datetime.now() - (parsed_tweet['date'] + datetime.timedelta(hours=5, minutes=30))).total_seconds()
    
            if date_rest // 86400 > 0:
                parsed_tweet['date_rem'] = str(int(date_rest // 86400)) + " days ago"
            elif date_rest // 3600 > 0:
                parsed_tweet['date_rem'] = str(int(date_rest // 3600)) + " hours ago"
            elif date_rest // 60:
                parsed_tweet['date_rem'] = str(int(date_rest // 60)) + " minutes ago"
            else:
                parsed_tweet['date_rem'] = str(int(date_rest)) + " seconds ago"

            
        except tweepy.TweepError as e:
            print("Error : " + str(e))
            return
        
        return parsed_tweet
