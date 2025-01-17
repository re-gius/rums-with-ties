# RUMs with Ties: A Discrete Choice Model Allowing Multiple Winners

Here, we provide the experimental setting and algorithms from "RUMs with Ties: A Discrete Choice Model Allowing Multiple Winners",
by F. Chierichetti, R. Kumar, G. Re, A. Tomkins.
This article is going to be presented at ASONAM 2024: The 16th International Conference on Advances in Social Networks Analysis and Mining.

If you use this code, or use the findings from the paper, please cite it appropriately.

```
Check again once the Proceedings have been published
@inproceedings{chierichetti2024rums,
  title={RUMs with Ties: A Discrete Choice Model Allowing Multiple Winners},
  author={Chierichetti, Flavio and Kumar, Ravi and Re, Giuseppe and Tomkins, Andrew},
  booktitle={Proceedings of the 16th International Conference on Advances in Social Networks Analysis and Mining},
  pages={N/A},
  year={2024}
}
```

## Reproducibility

The main folder contains the notebooks used to run the experiments:
- `delta-MNL.ipynb` only contains the training/testing for delta-MNL.
- `experiments.ipynb` contains training/testing for all the other discrete choice models. 
- `inferences.ipynb` contains the experiments used to compute the implicit inferences returned by Algorithm 1.


To generate all the files needed to run these notebooks, refer to the `README` in the `data` folder.