#!/bin/bash
python parse_lp_sol.py lp/*.sol
python lp_rumwt_predictor.py mnl_datasets/test/sushi_10_431_3_10000_0.5_test.csv --lprum=sushi_10_4310_3_1000_0.5._learned_rumwt.csv
python lp_rumwt_predictor.py mnl_datasets/test/tripadvisor_10_98_4_10000_0.5_test.csv --lprum=tripadvisor_10_980_4_10000_0.5._learned_rumwt.csv
python lp_rumwt_predictor.py mnl_datasets/test/young_people_spendinghabits_7_101_2_10000_0.5_test.csv --lprum=young_people_spendinghabits_7_1010_2_1000_0.5._learned_rumwt.csv
python lp_rumwt_predictor.py mnl_datasets/test/movies_20_17413_5_10000_0.25_test.csv --lprum=movies_20_174130_5_100000_0.25._learned_rumwt.csv
python lp_rumwt_predictor.py mnl_datasets/test/books_30_4721_5_10000_0.5_test.csv --lprum=books_30_4721_5_10000_0.5._learned_rumwt.csv
python rumwt_predictor.py mnl_datasets/test/sushi_* --trainrum=sushi_10_4310_train.csv --testrum=sushi_10_4310.csv
python rumwt_predictor.py mnl_datasets/test/tripadvisor_* --trainrum=tripadvisor_10_980_train.csv --testrum=tripadvisor_10_980.csv
python rumwt_predictor.py mnl_datasets/test/young_people_* --trainrum=young_people_spendinghabits_7_1010_train.csv --testrum=young_people_spendinghabits_7_1010.csv
python rumwt_predictor.py mnl_datasets/test/movies_* --trainrum=movies_20_174130_train.csv --testrum=movies_20_174130.csv
python rumwt_predictor.py mnl_datasets/test/books_* --trainrum=books_30_47211_train.csv --testrum=books_30_47211.csv