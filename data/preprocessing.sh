#!/bin/bash
python random_split.py clean/*.csv
python slates_generator.py clean/train/sushi_* --slatesize=3 --minfreq=2
python slates_generator.py clean/test/sushi_* --slatesize=3 --minfreq=2 --numslates=10000
python slates_generator.py clean/train/tripadvisor_* --slatesize=4 --numslates=10000 
python slates_generator.py clean/test/tripadvisor_* --slatesize=4 --numslates=10000 
python slates_generator.py clean/train/young_people_spendinghabits_* --slatesize=2
python slates_generator.py clean/test/young_people_spendinghabits_* --slatesize=2 --numslates=10000
python slates_generator.py clean/train/movies_* --slatesize=5 --numslates=100000 --minfreq=3
python slates_generator.py clean/test/movies_* --slatesize=5 --numslates=10000 --minfreq=2
python slates_generator.py clean/train/books_* --slatesize=5 --numslates=100000 --minfreq=3
python slates_generator.py clean/test/books_* --slatesize=5 --numslates=10000 --minfreq=2
python mnl_preprocessing.py slates/train/movies_* --delta=0.25
python mnl_preprocessing.py slates/test/movies_* --delta=0.25
python mnl_preprocessing.py slates/train/*
python mnl_preprocessing.py slates/test/*
rm mnl_datasets/train/movies_20_174130_5_100000_0.5_train.csv
rm mnl_datasets/test/movies_20_17413_5_10000_0.5_test.csv
python lp_generator mnl_datasets/train/sushi_* --numbuckets=3
python lp_generator mnl_datasets/train/tripadvisor_* --numbuckets=3
python lp_generator mnl_datasets/train/young_people_spendinghabits_*_* --numbuckets=3
python lp_generator mnl_datasets/train/movie_* --numbuckets=2 --sampleprob=0.05
python lp_generator mnl_datasets/train/books_* --numbuckets=2 --sampleprob=0.00005
