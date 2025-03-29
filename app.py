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