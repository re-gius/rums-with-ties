#!/bin/bash
python conv.py raw/*.csv raw/*.txt
for seed in {42..52}
do
    python conv.py raw/*.csv raw/*.txt --seed $seed
done