#! /usr/bin/python3

from functools import lru_cache
import cProfile
import pstats
import json
import os

infinity = float('inf')


def minCoinsToValue(value, coins):

    if value == 0:
        return 0

    minCoins = infinity

    for coin in coins:

        if coin > value:
            continue

        coinsNeeded = minCoinsToValue(value - coin, coins)

        minCoins = min(minCoins, coinsNeeded + 1)

    return minCoins


@lru_cache(maxsize=1000)
def minCoinsToValueCached(value, coins):

    if value == 0:
        return 0

    minCoins = infinity

    for coin in coins:

        if coin > value:
            continue

        coinsNeeded = minCoinsToValueCached(value - coin, coins)

        minCoins = min(minCoins, coinsNeeded + 1)

    return minCoins


runs = []

runArgs = range(10, 41, 5)

for runArg in runArgs:

    currSample = {
        'algorithm': 'minCoinsToValue',
        'runArg': runArg,
        'times': [],
        'functionCalls': [],
        'primitiveCalls': []
    }

    currSampleCached = {
        'algorithm': 'minCoinsToValueCached',
        'runArg': runArg,
        'times': [],
        'functionCalls': [],
        'primitiveCalls': []
    }

    for i in range(10):

        print(f'Run {i + 1} of {runArg}...')

        minCoinsToValueCached.cache_clear()

        cProfile.run('value = minCoinsToValue(runArg, (1, 3, 4))', 'stats')
        p = pstats.Stats('stats')
        time = p.total_tt
        functionCalls = p.total_calls
        primitiveCalls = p.prim_calls

        cProfile.run(
            'valueCached = minCoinsToValueCached(runArg, (1, 3, 4))', 'stats')
        p = pstats.Stats('stats')
        timeCached = p.total_tt
        functionCallsCached = p.total_calls
        primitiveCallsCached = p.prim_calls

        if value != valueCached:
            print('Error: values do not match')
            exit(-1)

        currSample['times'].append(time)
        currSample['functionCalls'].append(functionCalls)
        currSample['primitiveCalls'].append(primitiveCalls)

        currSampleCached['times'].append(timeCached)
        currSampleCached['functionCalls'].append(functionCallsCached)
        currSampleCached['primitiveCalls'].append(primitiveCallsCached)

    currSample['meanTime'] = sum(
        currSample['times']) / len(currSample['times'])
    currSample['meanFunctionCalls'] = sum(
        currSample['functionCalls']) / len(currSample['functionCalls'])
    currSample['meanPrimitiveCalls'] = sum(
        currSample['primitiveCalls']) / len(currSample['primitiveCalls'])

    currSampleCached['meanTime'] = sum(
        currSampleCached['times']) / len(currSampleCached['times'])
    currSampleCached['meanFunctionCalls'] = sum(
        currSampleCached['functionCalls']) / len(currSampleCached['functionCalls'])
    currSampleCached['meanPrimitiveCalls'] = sum(
        currSampleCached['primitiveCalls']) / len(currSampleCached['primitiveCalls'])

    runs.append(currSample)
    runs.append(currSampleCached)

os.unlink('stats')

with open('runs2.json', 'w') as f:
    json.dump(runs, f, indent=4)
