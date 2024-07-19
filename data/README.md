# Instructions

## Requirements
You need Python 3 with the libraries Numpy, Pandas, and Scikit-Learn installed. 
You also need to have CPLEX installed.
You need the `python` command working and referring to Python 3. If you only have a `python3` command like in MacOS, you can either change every `python` command in a `.sh` file to `python3` or alias `python` to reference your Python 3 binary by editing your `.bashrc` or `.zshrc` file like this:

```
# This works on MacOS with Homebrew
echo "alias python=/opt/homebrew/bin/python3" >> ~/.bashrc 
```

## Data Preprocessing
Start from the current folder (`data/`).

First, download the datasets listed in the paper and put them in a folder named `raw`. You can do that with the script `download.sh` for the Sushi, TripAdvisor, and GoodBooks datasets. For the datasets available on Kaggle, you need to log in and download them from:
- YPSH: `https://www.kaggle.com/datasets/miroslavsabo/young-people-survey?select=responses.csv`
- MovieLens: `https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset`

After that, perform 

```
bash clean_all.sh
```

to standardise the format for each dataset. Output datasets will be in the folder `clean`.
After that, run

```
bash preprocessing.sh
```

## Learn LP-RUMwt
You can use cplex interactive optimiser to solve the LPs in the `lp` folder. For each file in this folder, execute the following commands inside cplex: 

```
read lp/<file_name>.lp
opt
write lp/<file_name>.sol
```

After that, you can compute the predictions of all the models by running

```
bash predictions.sh
```

## Evaluation
Use the notebooks in the main folder to train the MNLs and compute the metrics for the different discrete choice models.
