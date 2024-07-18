#!/bin/bash
cd raw
curl https://www.kamishima.net/asset/sushi3-2016.zip -o sushi.zip
unzip sushi.zip
cp sushi3-2016/sushi3b.5000.10.score ./sushi.txt
rm sushi.zip
rm -r sushi3-2016
curl https://archive.ics.uci.edu/static/public/484/travel+reviews.zip -o tripadvisor.zip
unzip tripadvisor.zip
rm tripadvisor.zip
curl https://github.com/zygmuntz/goodbooks-10k/blob/master/ratings.csv -o goodbooks.csv