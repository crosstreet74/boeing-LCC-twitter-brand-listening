'''
crawl the twits at the time around each incident below
-----
United Airlines / T'way Air
=====
Boeing 737 NG (not considered)
** 2016년 3월 19일, 플라이두바이 981편 추락 사고, 탑승자 62명 전원 사망.
* 2018년 4월 17일, 사우스웨스트 항공 1380편 엔진파손 사건, 탑승자 149명 중 1명 사망, 148명 생존.
* 2019년 9월 경, FAA, Boeing 737 NG crack report
===== 
Boeing 737 MAX
* 2018년 10월 29일, 라이온 에어 소속 737 MAX 8이 바다로 추락, 189명 전원 사망
* 2019년 3월 10일, 에티오피아 항공 소속 737 MAX 8 여객기 추락, 157명 전원 사망
=====
'''
# less tweets for the korean search, chose english search
# lang=en, query('united airline 737 MAX')
# since='2018-10-01', until='2019-11-30'

import time
import datetime
import pandas
import GetOldTweets3 as got
from tqdm import tqdm_notebook
from random import uniform

start = datetime.datetime.strptime("2018-10-01", "%Y-%m-%d")
end = datetime.datetime.strptime("2019-11-30", "%Y-%m-%d")
date_generated = [
    start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

days_range = []

for date in date_generated:
    days_range.append(date.strftime("%Y-%m-%d"))

print("=== 설정된 트윗 수집 기간은 {} 에서 {} 까지 입니다 ===".format(
    days_range[0], days_range[-1]))
print("=== 총 {}일 간의 데이터 수집 ===".format(len(days_range)))

tweetCriteria = got.manager.TweetCriteria().setQuerySearch('united airline 737 MAX')\
                                           .setSince(days_range[0])\
                                           .setUntil(days_range[-1])\
                                           .setMaxTweets(-1)\
                                           .setLang('en') 

print("Collecting data start.. from {} to {}".format(
    days_range[0], days_range[-1]))

start_time = time.time()
tweet = got.manager.TweetManager.getTweets(tweetCriteria)

print("Collecting data end.. {0:0.2f} Minutes".format(
    (time.time() - start_time)/60))
print("=== Total # of tweets is {} ===".format(len(tweet)))

tweet_list = []

for index in tqdm_notebook(tweet):
    content = index.text
    tweet_date = index.date.strftime("%Y-%m-%d")
    info_list = [tweet_date, content]
    tweet_list.append(info_list)
    time.sleep(uniform(1, 3))

twitter_df = pandas.DataFrame(tweet_list,
                              columns=["date", "text"])

twitter_df.to_csv("sample_twitter_data_{}_to_{}.csv".format(
    days_range[0], days_range[-1]), index=False)
print("=== {} tweets are successfully saved ===".format(len(tweet_list)))