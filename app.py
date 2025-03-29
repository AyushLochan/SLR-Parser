import streamlit as st
import copy
import pandas as pd

def grammarAugmentation(rules, nonterm_userdef, start_symbol):
    """Augment the grammar by adding S' -> S."""
    newRules = []
    newChar = start_symbol + "'"
    while newChar in nonterm_userdef:
        newChar += "'"
    newRules.append([newChar, ['.', start_symbol]])
    
    for rule in rules:
        lhs, rhs = rule.split("->")
        lhs = lhs.strip()
        rhs = rhs.strip()
        multirhs = rhs.split('|')
        for rhs1 in multirhs:
            rhs1 = rhs1.strip().split()
            rhs1.insert(0, '.')
            newRules.append([lhs, rhs1])
    return newRules

def findClosure(input_state, dotSymbol, separatedRulesList, init_start_symbol):
    """Compute the closure for a given set of items."""
    closureSet = []

    if dotSymbol == init_start_symbol:
        for rule in separatedRulesList:
            if rule[0] == dotSymbol:
                closureSet.append(rule)
    else:
        closureSet = input_state.copy()

    prevLen = -1
    while prevLen != len(closureSet):
        prevLen = len(closureSet)
        tempClosureSet = []
        for rule in closureSet:
            indexOfDot = rule[1].index('.')
            if rule[1][-1] != '.':
                dotPointsHere = rule[1][indexOfDot + 1]
                for in_rule in separatedRulesList:
                    if dotPointsHere == in_rule[0] and in_rule not in tempClosureSet:
                        tempClosureSet.append(in_rule)
        for rule in tempClosureSet:
            if rule not in closureSet:
                closureSet.append(rule)
    return closureSet
    
def compute_GOTO(state, statesDict, stateMap, separatedRulesList):
    generateStatesFor = []
    for rule in statesDict[state]:
        if rule[1][-1] != '.':
            indexOfDot = rule[1].index('.')
            dotPointsHere = rule[1][indexOfDot + 1]
            if dotPointsHere not in generateStatesFor:
                generateStatesFor.append(dotPointsHere)

    for symbol in generateStatesFor:
        GOTO(state, symbol, statesDict, stateMap, separatedRulesList)
        
def GOTO(state, charNextToDot, statesDict, stateMap, separatedRulesList):
    newState = []
    for rule in statesDict[state]:
        indexOfDot = rule[1].index('.')
        if rule[1][-1] != '.':
            if rule[1][indexOfDot + 1] == charNextToDot:
                shiftedRule = copy.deepcopy(rule)

                shiftedRule[1][indexOfDot] = shiftedRule[1][indexOfDot + 1]
                shiftedRule[1][indexOfDot + 1] = '.'
                newState.append(shiftedRule)

    addClosureRules = []
    for rule in newState:
        indexDot = rule[1].index('.')
        if rule[1][-1] != '.':
            closureRes = findClosure(newState, rule[1][indexDot + 1], separatedRulesList, None)
            for r in closureRes:
                if r not in addClosureRules and r not in newState:
                    addClosureRules.append(r)
    newState.extend(addClosureRules)

    stateExists = -1
    for state_num, st_state in statesDict.items():
        if st_state == newState:
            stateExists = state_num
            break

    if stateExists == -1:
        new_index = max(statesDict.keys()) + 1
        statesDict[new_index] = newState
        stateMap[(state, charNextToDot)] = new_index
    else:
        stateMap[(state, charNextToDot)] = stateExists
        
def generateStates(statesDict, stateMap, separatedRulesList):
    prev_len = -1
    called_GOTO_on = []
    while len(statesDict) != prev_len:
        prev_len = len(statesDict)
        keys = list(statesDict.keys())

def first(rule, diction, term_userdef):
   
    if rule and rule[0]:
        if rule[0] in term_userdef:
            return rule[0]
        elif rule[0] == '#':
            return '#'
    if rule:
        if rule[0] in diction:
            fres = []
            rhs_rules = diction[rule[0]]
            for itr in rhs_rules:
                indivRes = first(itr, diction, term_userdef)
                if isinstance(indivRes, list):
                    fres.extend(indivRes)
                else:
                    fres.append(indivRes)
            if '#' not in fres:
                return fres
            else:
                newList = []
                fres.remove('#')
                if len(rule) > 1:
                    ansNew = first(rule[1:], diction, term_userdef)
                    if ansNew:
                        if isinstance(ansNew, list):
                            newList = fres + ansNew
                        else:
                            newList = fres + [ansNew]
                    else:
                        newList = fres
                    return newList
                fres.append('#')
                return fres
        for key in keys:
            if key not in called_GOTO_on:
                called_GOTO_on.append(key)
                compute_GOTO(key, statesDict, stateMap, separatedRulesList)
