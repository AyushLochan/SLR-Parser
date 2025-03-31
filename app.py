import streamlit as st
import copy
import pandas as pd

def grammarAugmentation(rules, nonterm_userdef, start_symbol):
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
            rhs1 = rhs1.strip()
            if rhs1 == '#':
                rhs_split = []
            else:
                rhs_split = rhs1.split()
            rhs_split.insert(0, '.')
            newRules.append([lhs, rhs_split])
    return newRules

def findClosure(input_state, dotSymbol, separatedRulesList, init_start_symbol):
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
            if indexOfDot < len(rule[1]) - 1:
                dotPointsHere = rule[1][indexOfDot + 1]
                for in_rule in separatedRulesList:
                    if dotPointsHere == in_rule[0] and in_rule not in tempClosureSet and in_rule not in closureSet:
                        tempClosureSet.append(in_rule)
        closureSet.extend(tempClosureSet)
    return closureSet

def compute_GOTO(state, statesDict, stateMap, separatedRulesList):
    generateStatesFor = []
    for rule in statesDict[state]:
        indexOfDot = rule[1].index('.')
        if indexOfDot < len(rule[1]) - 1:
            dotPointsHere = rule[1][indexOfDot + 1]
            if dotPointsHere not in generateStatesFor:
                generateStatesFor.append(dotPointsHere)

    for symbol in generateStatesFor:
        GOTO(state, symbol, statesDict, stateMap, separatedRulesList)

def GOTO(state, charNextToDot, statesDict, stateMap, separatedRulesList):
    newState = []
    for rule in statesDict[state]:
        indexOfDot = rule[1].index('.')
        if indexOfDot < len(rule[1]) - 1 and rule[1][indexOfDot + 1] == charNextToDot:
            shiftedRule = copy.deepcopy(rule)
            shiftedRule[1][indexOfDot], shiftedRule[1][indexOfDot + 1] = shiftedRule[1][indexOfDot + 1], shiftedRule[1][indexOfDot]
            newState.append(shiftedRule)

    closure = findClosure(newState, charNextToDot, separatedRulesList, None)
    for item in closure:
        if item not in newState:
            newState.append(item)

    stateExists = -1
    for state_num in statesDict:
        if statesDict[state_num] == newState:
            stateExists = state_num
            break
    if stateExists == -1:
        new_index = max(statesDict.keys()) + 1 if statesDict else 0
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
        for key in keys:
            if key not in called_GOTO_on:
                called_GOTO_on.append(key)
                compute_GOTO(key, statesDict, stateMap, separatedRulesList)

def first(rule, diction, term_userdef):
    if not rule:
        return ['#']
    first_symbol = rule[0]
    if first_symbol in term_userdef:
        return [first_symbol]
    elif first_symbol == '#':
        return ['#']
    elif first_symbol in diction:
        fres = []
        for production in diction[first_symbol]:
            prod_first = first(production, diction, term_userdef)
            fres.extend(prod_first)
        if '#' in fres:
            fres.remove('#')
            if len(rule) > 1:
                rest_first = first(rule[1:], diction, term_userdef)
                fres.extend(rest_first)
            else:
                fres.append('#')
        return list(set(fres))
    return []

def follow(nt, diction, start_symbol, term_userdef):
    solset = set()
    if nt == start_symbol:
        solset.add('$')
    for curNT in diction:
        for prod in diction[curNT]:
            for i, symbol in enumerate(prod):
                if symbol == nt:
                    next_pos = i + 1
                    while next_pos <= len(prod):
                        if next_pos == len(prod):
                            if curNT != nt:
                                solset.update(follow(curNT, diction, start_symbol, term_userdef))
                            break
                        next_symbol = prod[next_pos]
                        first_next = first([next_symbol], diction, term_userdef)
                        if '#' in first_next:
                            solset.update([x for x in first_next if x != '#'])
                            next_pos += 1
                        else:
                            solset.update(first_next)
                            break
    return list(solset)

def createParseTable(statesDict, stateMap, T, NT, separatedRulesList, rules, diction, term_userdef, start_symbol):
    rows = list(statesDict.keys())
    cols = T + ['$'] + NT
    Table = []
    for _ in rows:
        Table.append([''] * len(cols))

    for entry in stateMap:
        state = entry[0]
        symbol = entry[1]
        a = rows.index(state)
        b = cols.index(symbol)
        if symbol in NT:
            Table[a][b] += f"{stateMap[entry]} "
        elif symbol in T:
            Table[a][b] += f"S{stateMap[entry]} "

    numbered = {}
    key_count = 0
    for rule in separatedRulesList:
        tempRule = copy.deepcopy(rule)
        if '.' in tempRule[1]:
            tempRule[1].remove('.')
        numbered[key_count] = tempRule
        key_count += 1

    rules_copy = rules.copy()
    addedR = f"{separatedRulesList[0][0]} -> {separatedRulesList[0][1][1]}"
    rules_copy.insert(0, addedR)

    for rule in rules_copy:
        lhs, rhs = rule.split("->")
        lhs = lhs.strip()
        rhs = [r.strip().split() for r in rhs.strip().split('|')]
        diction[lhs] = [['#'] if part == [''] else part for part in rhs]

    for stateno in statesDict:
        for rule in statesDict[stateno]:
            if rule[1][-1] == '.' or (len(rule[1]) == 1 and rule[1][0] == '.'):
                temp2 = copy.deepcopy(rule)
                temp2[1] = [x for x in temp2[1] if x != '.']
                for key in numbered:
                    if numbered[key] == temp2:
                        follow_result = follow(rule[0], diction, start_symbol, term_userdef)
                        for col in follow_result:
                            if col in cols:
                                index = cols.index(col)
                                if key == 0:
                                    Table[stateno][index] = "Accept"
                                else:
                                    Table[stateno][index] += f"R{key} " if Table[stateno][index] != "Accept" else f"R{key} "

    return Table, rows, cols


def generate_conflict_counts(table):
    sr = 0
    rr = 0

    for row in table:
        for cell in row:
            if cell and cell != 'ac':
                actions = cell.split()
                shift_count = sum(1 for action in actions if action.startswith('S'))
                reduce_count = sum(1 for action in actions if action.startswith('R'))

                if shift_count > 0 and reduce_count > 0:
                    sr += 1
                elif reduce_count > 1:
                    rr += 1

    return sr, rr



def main():
    st.set_page_config(page_title="SLR(1) Parser Generator", layout="wide")
    st.title("SLR(1) Parser Generator")
    
    with st.sidebar:
        st.header("Grammar Input")
        grammar_input = st.text_area(
            "Enter Grammar Rules (one per line)", 
            height=150,
            value="""E -> E + T | T
T -> T * F | F
F -> ( E ) | id"""
        )
        nonterm_input = st.text_input("Non-Terminals (comma separated)", value="E, T, F")
        term_input = st.text_input("Terminals (comma separated)", value="id, +, *, (, )")
        generate_btn = st.button("Generate SLR(1) Parsing Table")
    
    if generate_btn:
        rules = [line.strip() for line in grammar_input.splitlines() if line.strip()]
        nonterm_userdef = [x.strip() for x in nonterm_input.split(',')]
        term_userdef = [x.strip() for x in term_input.split(',')]
        start_symbol = nonterm_userdef[0]

        st.subheader("Original Grammar:")
        for rule in rules:
            st.write(rule)

        separatedRulesList = grammarAugmentation(rules, nonterm_userdef, start_symbol)
        st.subheader("Augmented Grammar:")
        aug_output = "\n".join([f"{rule[0]} -> {' '.join(rule[1]) if rule[1] else 'ε'}" for rule in separatedRulesList])
        st.text(aug_output)

        init_start_symbol = separatedRulesList[0][0]
        I0 = findClosure([separatedRulesList[0]], separatedRulesList[0][1][1], separatedRulesList, init_start_symbol)
        st.subheader("Initial Closure (I0):")
        closure_output = "\n".join([f"{rule[0]} -> {' '.join(rule[1]) if rule[1] else 'ε'}" for rule in I0])
        st.text(closure_output)

        statesDict = {0: I0}
        stateMap = {}
        generateStates(statesDict, stateMap, separatedRulesList)

        st.subheader("Generated States:")
        states_output = ""
        for st_num, state in statesDict.items():
            states_output += f"State I{st_num}:\n"
            for rule in state:
                rhs = ' '.join(rule[1]) if rule[1] else 'ε'
                states_output += f"    {rule[0]} → {rhs}\n"
            states_output += "\n"
        st.text(states_output)

        st.subheader("GOTO Transitions:")
        goto_output = ""
        for (src, symbol), dest in stateMap.items():
            goto_output += f"GOTO(I{src}, {symbol}) = I{dest}\n"
        st.text(goto_output)

        diction = {}
        Table, rowStates, cols = createParseTable(
            statesDict,
            stateMap,
            term_userdef,
            nonterm_userdef,
            separatedRulesList,
            rules,
            diction,
            term_userdef,
            separatedRulesList[0][0]
        )

        st.subheader("SLR(1) Parsing Table:")
        df = pd.DataFrame(Table, index=[f"I{i}" for i in rowStates], columns=cols)
        st.dataframe(df)

        sr, rr = generate_conflict_counts(Table)
        st.subheader("Conflict Analysis:")
        st.markdown(f"**Shift-Reduce Conflicts:** {sr}")
        st.markdown(f"**Reduce-Reduce Conflicts:** {rr}")
        if sr == 0 and rr == 0:
            st.success("The grammar is SLR(1).")
        else:
            st.error("The grammar is NOT SLR(1).")

if __name__ == "__main__":
    main()
