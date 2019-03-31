# Solving Multi-Armed Problem

Repository consists of:

* Notebook (`mab_problem/notebook/multi_armed_bandit.ipynb`) with explanations on how to deal with multi-armed problems through four different approaches:

1. Random Selection
2. Epsilon Greedy
3. Thompson Sampling
4. Upper Confidence Bound (UCB1)

*Should be opened by [Jupyter NBViewer](https://nbviewer.jupyter.org/github/ruslan-kl/mab_problem/blob/9c169814aebb3eaed978cf7a447639c3e9fa91b9/notebook/multi_armed_bandit.ipynb) in order to see the plots.*

* Flask app (`mab_problem/flask_app`) for interactive experience with 2 variants and 1000 trials.

### App preview:
![](https://i.ibb.co/kcH3BnT/peek-new.gif)

To run an app on your machine clone/download the repo and follow the commands:
```
$ cd mab_problem/flask_app
$ export FLASK_APP=app.py
$ flask run
```
