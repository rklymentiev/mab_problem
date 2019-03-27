from flask import Flask, render_template, request, jsonify, abort
from scipy.stats import beta, bernoulli
import pandas as pd
import numpy as np
import math
import random

app = Flask(__name__)


# Define the Model
def random_sampling(CTR1, CTR2):
    CTR1 = float(CTR1)
    CTR2 = float(CTR2)
    ACTUAL_CTR = [CTR1, CTR2]

    n = 1000  # number of trials
    regret = 0
    total_reward = 0
    regret_list = []  # list for collecting the regret values for each impression (trial)
    ctr = {0: [], 1: []}  # lists for collecting the calculated CTR
    index_list = []  # list for collecting the number of randomly choosen Ad
    impressions = [0, 0]
    clicks = [0, 0]

    for i in range(n):

        random_index = np.random.randint(0, 2, 1)[0]  ## randomly choose the value between [0,1]
        index_list.append(random_index)  ## add the value to list

        impressions[random_index] += 1  ## add 1 impression value for the choosen Ad
        did_click = bernoulli.rvs(
            ACTUAL_CTR[random_index])  ## simulate if the person clicked on the ad usind Actual CTR value
        # did_click = False

        if did_click:
            clicks[random_index] += did_click  ## if person clicked add 1 click value for the choosen Ad

        ## calculate the CTR values and add them to list
        if impressions[0] == 0:
            ctr_0 = 0
        else:
            ctr_0 = clicks[0] / impressions[0]

        if impressions[1] == 0:
            ctr_1 = 0
        else:
            ctr_1 = clicks[1] / impressions[1]

        ctr[0].append(ctr_0)
        ctr[1].append(ctr_1)

        ## calculate the regret and reward
        regret += max(ACTUAL_CTR) - ACTUAL_CTR[random_index]
        regret_list.append(regret)
        total_reward += did_click

    count_series = pd.Series(index_list).value_counts(normalize=True)
    ad_1 = round(count_series[0], 3)
    ad_2 = round(count_series[1], 3)
    regret_list = [round(x,2) for x in regret_list]
    return total_reward, ad_1, ad_2, regret_list


def epsilon_greedy(CTR1, CTR2):
    CTR1 = float(CTR1)
    CTR2 = float(CTR2)
    ACTUAL_CTR = [CTR1, CTR2]
    n = 1000

    e = .05  ## set the Epsilon value
    n_init = 100  ## number of impressions to choose the winning Ad
    impressions = [0, 0]
    clicks = [0, 0]

    for i in range(n_init):
        random_index = np.random.randint(0, 2, 1)[0]

        impressions[random_index] += 1
        did_click = bernoulli.rvs(ACTUAL_CTR[random_index])
        if did_click:
            clicks[random_index] += did_click

    ctr_0 = clicks[0] / impressions[0]
    ctr_1 = clicks[1] / impressions[1]
    win_index = np.argmax([ctr_0, ctr_1])  ## select the Ad number with the highest CTR

    regret = 0
    total_reward = 0
    regret_list = []
    ctr = {0: [], 1: []}
    index_list = []
    impressions = [0, 0]
    clicks = [0, 0]

    for i in range(n):

        epsilon_index = random.choices([win_index, 1 - win_index], [1 - e, e])[0]
        index_list.append(epsilon_index)

        impressions[epsilon_index] += 1
        did_click = bernoulli.rvs(ACTUAL_CTR[epsilon_index])
        if did_click:
            clicks[epsilon_index] += did_click

        if impressions[0] == 0:
            ctr_0 = 0
        else:
            ctr_0 = clicks[0] / impressions[0]

        if impressions[1] == 0:
            ctr_1 = 0
        else:
            ctr_1 = clicks[1] / impressions[1]

        ctr[0].append(ctr_0)
        ctr[1].append(ctr_1)

        regret += max(ACTUAL_CTR) - ACTUAL_CTR[epsilon_index]
        regret_list.append(regret)
        total_reward += did_click

    count_series = pd.Series(index_list).value_counts(normalize=True)
    ad_1 = round(count_series[0], 3)
    ad_2 = round(count_series[1], 3)
    regret_list = [round(x, 2) for x in regret_list]

    return total_reward, ad_1, ad_2, regret_list


def thompson_sampling(CTR1, CTR2):
    CTR1 = float(CTR1)
    CTR2 = float(CTR2)
    ACTUAL_CTR = [CTR1, CTR2]
    n = 1000

    regret = 0
    total_reward = 0
    regret_list = []
    ctr = {0: [], 1: []}
    index_list = []
    impressions = [0, 0]
    clicks = [0, 0]
    priors = (1, 1)
    win_index = np.random.randint(0, 2, 1)[0]  ## randomly choose the first shown Ad

    for i in range(n):

        impressions[win_index] += 1
        did_click = bernoulli.rvs(ACTUAL_CTR[win_index])
        if did_click:
            clicks[win_index] += did_click

        ctr_0 = random.betavariate(priors[0] + clicks[0], priors[1] + impressions[0] - clicks[0])
        ctr_1 = random.betavariate(priors[0] + clicks[1], priors[1] + impressions[1] - clicks[1])
        win_index = np.argmax([ctr_0, ctr_1])
        index_list.append(win_index)

        ctr[0].append(ctr_0)
        ctr[1].append(ctr_1)

        regret += max(ACTUAL_CTR) - ACTUAL_CTR[win_index]
        regret_list.append(regret)
        total_reward += did_click

    count_series = pd.Series(index_list).value_counts(normalize=True)
    ad_1 = round(count_series[0], 3)
    ad_2 = round(count_series[1], 3)
    regret_list = [round(x, 2) for x in regret_list]

    return total_reward, ad_1, ad_2, regret_list


def ucb1(CTR1, CTR2):
    CTR1 = float(CTR1)
    CTR2 = float(CTR2)
    ACTUAL_CTR = [CTR1, CTR2]

    n = 1000
    regret = 0
    total_reward = 0
    regret_list = []
    index_list = []
    impressions = [0, 0]
    clicks = [0, 0]
    ctr = {0: [], 1: []}
    total_reward = 0

    for i in range(n):

        index = 0
        max_upper_bound = 0
        for k in [0, 1]:
            if (impressions[k] > 0):
                CTR = clicks[k] / impressions[k]
                delta = math.sqrt(2 * math.log(i + 1) / impressions[k])
                upper_bound = CTR + delta
                ctr[k].append(CTR)
            else:
                upper_bound = 1e400
            if upper_bound > max_upper_bound:
                max_upper_bound = upper_bound
                index = k
        index_list.append(index)
        impressions[index] += 1
        reward = bernoulli.rvs(ACTUAL_CTR[index])

        clicks[index] += reward
        total_reward += reward

        regret += max(ACTUAL_CTR) - ACTUAL_CTR[index]
        regret_list.append(regret)

    count_series = pd.Series(index_list).value_counts(normalize=True)
    ad_1 = round(count_series[0], 3)
    ad_2 = round(count_series[1], 3)
    regret_list = [round(x, 2) for x in regret_list]

    return total_reward, ad_1, ad_2, regret_list


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    content = request.get_json()
    CTR1 = content.get('CTR1')
    CTR2 = content.get('CTR2')

    reward_rs, ad_1_rs, ad_2_rs, regret_rs = random_sampling(CTR1, CTR2)
    reward_eg, ad_1_eg, ad_2_eg, regret_eg = epsilon_greedy(CTR1, CTR2)
    reward_ts, ad_1_ts, ad_2_ts, regret_ts = thompson_sampling(CTR1, CTR2)
    reward_ucb1, ad_1_ucb1, ad_2_ucb1, regret_ucb1 = ucb1(CTR1, CTR2)

    return jsonify(
        reward_rs=reward_rs,
        reward_eg=reward_eg,
        reward_ts=reward_ts,
        reward_ucb1=reward_ucb1,
        ad_1_rs=ad_1_rs,
        ad_2_rs=ad_2_rs,
        ad_1_eg=ad_1_eg,
        ad_2_eg=ad_2_eg,
        ad_1_ts=ad_1_ts,
        ad_2_ts=ad_2_ts,
        ad_1_ucb1=ad_1_ucb1,
        ad_2_ucb1=ad_2_ucb1,
        regret_rs=regret_rs,
        regret_eg=regret_eg,
        regret_ts=regret_ts,
        regret_ucb1=regret_ucb1,
    )


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')
