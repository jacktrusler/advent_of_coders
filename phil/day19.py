from time import perf_counter_ns
from dataclasses import dataclass
import math


@dataclass
class Blueprint:
    id: int
    ore_cost_ore: int
    clay_cost_ore: int
    obs_cost_ore: int
    obs_cost_clay: int
    geode_cost_ore: int
    geode_cost_obs: int

    def __post_init__(self):
        self.max_ore_bots = max(self.ore_cost_ore, self.clay_cost_ore, self.obs_cost_ore, self.geode_cost_ore)
        self.max_clay_bots = self.obs_cost_clay
        self.max_obs_bots = self.geode_cost_obs


def triangle(n):
    return (n**2 + n) // 2


def score(bp: Blueprint, time: int, time_states: dict, full_states: dict, best: list,
          ore_bots: int = 1, clay_bots: int = 0, obs_bots: int = 0, geode_bots: int = 0,
          ore: int = 0, clay: int = 0, obs: int = 0, geode: int = 0):

    # Determine time needed to build a geode robot
    try:
        time_spent_for_ore = math.ceil(max(bp.geode_cost_ore - ore, 0) / ore_bots)
        time_spent_for_obs = math.ceil(max(bp.geode_cost_obs - obs, 0) / obs_bots)
    except ZeroDivisionError:
        time_spent_geode = time
    else:
        time_spent_geode = max(time_spent_for_ore, time_spent_for_obs) + 1

    # If building a geode robot every turn until time runs out is still not enough to beat the current best score,
    # give up.
    scores = [geode + geode_bots * time]  # final score if no more robots are built.
    best[0] = max(best[0], scores[0])
    time_to_build_geode_bots = time - (1 if time_spent_geode == 1 else 2)
    if geode + triangle(time_to_build_geode_bots) + geode_bots * time < best[0]:
        return 0

    # If this exact state was seen at an earlier time, that branch will always be better than this one.
    time_state = (ore_bots, clay_bots, obs_bots, geode_bots, ore, clay, obs, geode)
    try:
        if time < time_states[time_state]:
            return 0
    except KeyError:
        pass
    time_states[time_state] = time

    # If this state (including time) has been seen before, return the previous result.
    full_state = (time, ore_bots, clay_bots, obs_bots, geode_bots, ore, clay, obs, geode)
    if full_state in full_states:
        return full_states[full_state]

    # Build Ore Next
    try:
        time_spent = math.ceil(max(bp.ore_cost_ore - ore, 0) / ore_bots) + 1
    except ZeroDivisionError:
        time_spent = time
    last_helpful_clay_bot_at_time = 2
    if time - time_spent >= last_helpful_clay_bot_at_time and ore_bots < bp.max_ore_bots:
        rem_ore = time_spent * ore_bots + ore - bp.ore_cost_ore
        points = score(bp, time-time_spent, time_states, full_states, best, ore_bots+1, clay_bots, obs_bots, geode_bots,
                       rem_ore, clay+clay_bots*time_spent, obs+obs_bots*time_spent, geode+geode_bots*time_spent)
        scores.append(points)

    # Build Clay Next
    try:
        time_spent = math.ceil(max(bp.clay_cost_ore - ore, 0) / ore_bots) + 1
    except ZeroDivisionError:
        time_spent = time
    last_helpful_clay_bot_at_time = 3
    if time - time_spent >= last_helpful_clay_bot_at_time and clay_bots < bp.max_clay_bots:
        rem_ore = time_spent * ore_bots + ore - bp.clay_cost_ore
        points = score(bp, time-time_spent, time_states, full_states, best, ore_bots, clay_bots+1, obs_bots, geode_bots,
                       rem_ore, clay+clay_bots*time_spent, obs+obs_bots*time_spent, geode+geode_bots*time_spent)
        scores.append(points)

    # Build Obsidian Next
    try:
        time_spent_for_ore = math.ceil(max(bp.obs_cost_ore - ore, 0) / ore_bots)
        time_spent_for_clay = math.ceil(max(bp.obs_cost_clay - clay, 0) / clay_bots)
    except ZeroDivisionError:
        time_spent_obsidian = time
    else:
        time_spent_obsidian = max(time_spent_for_ore, time_spent_for_clay) + 1
    last_helpful_obsidian_bot_at_time = 2
    if time - time_spent_obsidian >= last_helpful_obsidian_bot_at_time and obs_bots < bp.max_obs_bots:
        rem_ore = time_spent_obsidian * ore_bots + ore - bp.obs_cost_ore
        rem_clay = time_spent_obsidian * clay_bots + clay - bp.obs_cost_clay
        points = score(bp, time-time_spent_obsidian, time_states, full_states, best, ore_bots, clay_bots, obs_bots+1,
                       geode_bots, rem_ore, rem_clay, obs+obs_bots*time_spent_obsidian,
                       geode+geode_bots*time_spent_obsidian)
        scores.append(points)

    # Build Geode Next
    last_helpful_geode_bot_at_time = 1
    if time - time_spent_geode >= last_helpful_geode_bot_at_time:
        rem_ore = time_spent_geode * ore_bots + ore - bp.geode_cost_ore
        rem_obs = time_spent_geode * obs_bots + obs - bp.geode_cost_obs
        points = score(bp, time-time_spent_geode, time_states, full_states, best, ore_bots, clay_bots, obs_bots,
                       geode_bots+1, rem_ore, clay+clay_bots*time_spent_geode, rem_obs,
                       geode+geode_bots*time_spent_geode)
        scores.append(points)

    best_score = max(scores)
    full_states[full_state] = best_score
    return best_score


def solve_a(blueprints: list[Blueprint]):
    return sum(bp.id * score(bp, time=24, time_states=dict(), full_states=dict(), best=[0]) for bp in blueprints)


def solve_b(blueprints: list[Blueprint]):
    result = 1
    for bp in blueprints[:3]:
        s = score(bp, time=32, time_states=dict(), full_states=dict(), best=[0])
        result *= s
    return result


def solve(raw_input: str):
    blueprints = list()
    for line in raw_input.splitlines():
        items = line.split()
        bp = Blueprint(int(items[1][:-1]), *[int(items[i]) for i in (6, 12, 18, 21, 27, 30)])
        blueprints.append(bp)
    a = solve_a(blueprints)
    b = solve_b(blueprints)
    return a, b


def main():
    with open('./day19_input.txt', mode='r') as f:
        problem_input = f.read()
    start_time = perf_counter_ns()
    a, b = solve(problem_input)
    end_time = perf_counter_ns()
    elapsed_ms = round((end_time - start_time) / 1000000, 3)
    print(f'A: {a}')
    print(f'B: {b}')
    print(f'Elapsed time: {elapsed_ms} ms')


if __name__ == '__main__':
    main()
