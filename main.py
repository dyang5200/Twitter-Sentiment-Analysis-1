import sys,tweepy,csv,re
from textblob import TextBlob
import matplotlib.pyplot as plt


class SentimentAnalysis:

    def __init__(self):
        self.num_of_tweets = 0
        self.terms = []
        self.str_terms = ""
        # self.tweets = []
        self.tweetText = []

        self.total_num_tweets = 0

        # creating some variables to store info
        self.polarity = 0
        self.positive = 0
        self.wpositive = 0
        self.spositive = 0
        self.negative = 0
        self.wnegative = 0
        self.snegative = 0
        self.neutral = 0

    def get_user_input(self):
        # input how many terms to search for, continues until user inputs an integer.
        while True:
            try:
                num_of_hashtags = int(input("How many hashtags would you like to search for? "))
            except ValueError:
                print("Please try again. That is not an integer!")
                continue
            else:
                print("\n")
                break

        while True:
            try:
                self.num_of_tweets = int(input("Enter how many tweets to search: "))
            except ValueError:
                print("Please try again. That is not an integer!")
                continue
            else:
                print("\n")
                break

        for i in range(num_of_hashtags):
            # input for term to be searched and how many tweets to search
            searchTerm = input("Enter Keyword/Tag to search about: ")
            self.terms.append(searchTerm)
            self.DownloadData(searchTerm)

        self.display_data()

    def DownloadData(self, input_search_term):
        # authenticating
        consumerKey = 'rrHjkbgnDRVVGGXlsnTftNERp'
        consumerSecret = 'Pd3gIPusYoZA63zsuV84e4xZcjJwG9DkId3Fixn7rbvq6YZBwX'
        accessToken = '1099184520832651265-aydSwMd4xbIQ71oVXsCEf4Tlzqhu8j'
        accessTokenSecret = 'ygmasWq85HZX2dBqWvN8UDeHYWjJ9HWEPOpkXugKRJyDn'
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)

        # searching for tweets
        tweets = tweepy.Cursor(api.search, q=input_search_term, lang = "en").items(self.num_of_tweets)

        # Open/create a file to append data to
        csvFile = open('result.csv', 'a')

        # Use csv writer
        csvWriter = csv.writer(csvFile)

        # iterating through tweets fetched
        for tweet in tweets:
            #Append to temp so that we can store in csv later. I use encode UTF-8
            self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
            # print (tweet.text.translate(non_bmp_map))    #print tweet's text
            analysis = TextBlob(tweet.text)
            # print(analysis.sentiment)  # print tweet's polarity
            self.polarity += analysis.sentiment.polarity  # adding up polarities to find the average later

            if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
                self.neutral += 1
            elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
                self.wpositive += 1
            elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
                self.positive += 1
            elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
                self.spositive += 1
            elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
                self.wnegative += 1
            elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
                self.negative += 1
            elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
                self.snegative += 1


        # Write to csv and close csv file
        csvWriter.writerow(self.tweetText)
        csvFile.close()


    def display_data(self):
        self.total_num_tweets = self.num_of_tweets * len(self.terms)
        # finding average of how people are reacting
        self.positive = self.percentage(self.positive, self.total_num_tweets)
        self.wpositive = self.percentage(self.wpositive, self.total_num_tweets)
        self.spositive = self.percentage(self.spositive, self.total_num_tweets)
        self.negative = self.percentage(self.negative, self.total_num_tweets)
        self.wnegative = self.percentage(self.wnegative, self.total_num_tweets)
        self.snegative = self.percentage(self.snegative, self.total_num_tweets)
        self.neutral = self.percentage(self.neutral, self.total_num_tweets)

        # finding average reaction
        polarity = self.polarity / self.total_num_tweets

        # Make a string of all the hashtags searched for
        self.str_terms = ""
        for i in range(len(self.terms)):
            if i == (len(self.terms) - 2):
                self.str_terms = self.str_terms + self.terms[i] + " and "
            elif i != (len(self.terms) - 1):
                self.str_terms = self.str_terms + self.terms[i] + ", "
            else:
                self.str_terms += self.terms[i]

        # printing out data
        print("How people are reacting on " + self.str_terms + " by analyzing " + str(self.num_of_tweets) + " tweets per term.")
        print()
        print("General Report: ")

        if (polarity == 0):
            print("Neutral")
        elif (polarity > 0 and polarity <= 0.3):
            print("Weakly Positive")
        elif (polarity > 0.3 and polarity <= 0.6):
            print("Positive")
        elif (polarity > 0.6 and polarity <= 1):
            print("Strongly Positive")
        elif (polarity > -0.3 and polarity <= 0):
            print("Weakly Negative")
        elif (polarity > -0.6 and polarity <= -0.3):
            print("Negative")
        elif (polarity > -1 and polarity <= -0.6):
            print("Strongly Negative")

        print()
        print("Detailed Report: ")
        print(str(self.positive) + "% people thought it was positive")
        print(str(self.wpositive) + "% people thought it was weakly positive")
        print(str(self.spositive) + "% people thought it was strongly positive")
        print(str(self.negative) + "% people thought it was negative")
        print(str(self.wnegative) + "% people thought it was weakly negative")
        print(str(self.snegative) + "% people thought it was strongly negative")
        print(str(self.neutral) + "% people thought it was neutral")

        if len(self.terms) > 1:
            self.plotTotalPieChart(self.positive, self.wpositive, self.spositive, self.negative,
                          self.wnegative, self.snegative, self.neutral, self.str_terms, self.num_of_tweets)


    def cleanTweet(self, tweet):
        # Remove Links, Special Characters etc from tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    # function to calculate percentage
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    def plotPieChart(self, positive, wpositive, spositive, negative, wnegative, snegative, neutral, term, num_of_tweets):
        labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]','Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]', 'Strongly Negative [' + str(snegative) + '%]']
        sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
        colors = ['yellowgreen','lightgreen','darkgreen', 'gold', 'red','lightsalmon','darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('How people are reacting on ' + term + ' by analyzing ' + str(num_of_tweets) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

    def plotTotalPieChart(self, positive, wpositive, spositive, negative, wnegative, snegative, neutral, str_terms, num_of_tweets):
        if len(self.terms) > 1:
            for i in range(len(self.terms)):
                self.plotPieChart(self.positive, self.wpositive, self.spositive, self.negative,
                                  self.wnegative, self.snegative, self.neutral, self.terms[i], self.num_of_tweets)
        
        labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]','Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]', 'Strongly Negative [' + str(snegative) + '%]']
        sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
        colors = ['yellowgreen','lightgreen','darkgreen', 'gold', 'red','lightsalmon','darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('How people are reacting on ' + str_terms + ' by analyzing ' + str(num_of_tweets) + ' Tweets per term.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()



if __name__== "__main__":
    sa = SentimentAnalysis()
    sa.get_user_input()
