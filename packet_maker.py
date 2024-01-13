import os
import random
import pandas as pd

NUM_PACKETS = 10
BREAKDOWN = [6, 5, 5, 4]
VERBOSE = True
START = 6

c_questions = pd.read_csv("custom_qs.csv")
o_questions = pd.read_csv("questions.csv")


ct_ps = c_questions[((c_questions["Category"] == "chemistry") | (c_questions["Category"] == "physics")) & (c_questions["Type"] == "toss-up")]
ct_biology = c_questions[(c_questions["Category"] == "biology") & (c_questions["Type"] == "toss-up")]
ct_math = c_questions[(c_questions["Category"] == "mathematics") & (c_questions["Type"] == "toss-up")]
ct_es = c_questions[(c_questions["Category"] == "earth and space") & (c_questions["Type"] == "toss-up")]

cb_ps = c_questions[((c_questions["Category"] == "chemistry") | (c_questions["Category"] == "physics")) & (c_questions["Type"] == "bonus")]
cb_biology = c_questions[(c_questions["Category"] == "biology") & (c_questions["Type"] == "bonus")]
cb_math = c_questions[(c_questions["Category"] == "mathematics") & (c_questions["Type"] == "bonus")]
cb_es = c_questions[(c_questions["Category"] == "earth and space") & (c_questions["Type"] == "bonus")]

if VERBOSE:
    print(f"Custom Physics Toss-Ups: {len(ct_ps)}")
    print(f"Custom Biology Toss-Ups: {len(ct_biology)}")
    print(f"Custom Math Toss-Ups: {len(ct_math)}")

    print(f"Custom Physics Bonuses: {len(cb_ps)}")
    print(f"Custom Biology Bonuses: {len(cb_biology)}")
    print(f"Custom Math Bonuses: {len(cb_math)}")

for j in range(1, NUM_PACKETS+1):
    ind = j+START
    print(f"{ind}")

    ot_ps = o_questions[(o_questions["Category"] == "physical science") & (o_questions["Type"] == "toss-up") & (o_questions["Round"] == ind)]
    ot_biology = o_questions[(o_questions["Category"] == "life science") & (o_questions["Type"] == "toss-up") & (o_questions["Round"] == ind)]
    ot_es = o_questions[(o_questions["Category"].isin(["earth and space", "earth and space science"])) & (o_questions["Type"] == "toss-up") & (o_questions["Round"] == ind)]
    ot_math = o_questions[(o_questions["Category"] == "math") & (o_questions["Type"] == "toss-up") & (o_questions["Round"] == ind)]

    ob_ps = o_questions[(o_questions["Category"] == "physical science") & (o_questions["Type"] == "bonus") & (o_questions["Round"] == ind)]
    ob_biology = o_questions[(o_questions["Category"] == "life science") & (o_questions["Type"] == "bonus") & (o_questions["Round"] == ind)]
    ob_es = o_questions[(o_questions["Category"].isin(["earth and space", "earth and space science"])) & (o_questions["Type"] == "bonus") & (o_questions["Round"] == ind)]
    ob_math = o_questions[(o_questions["Category"] == "math") & (o_questions["Type"] == "bonus") & (o_questions["Round"] == ind)]

    print(len(ob_ps))
    psqs = []
    for i in range(BREAKDOWN[0]):
        tos = ""
        bon = ""
        if len(ct_ps) > 0:
            tos = ct_ps.sample()
            ct_ps = ct_ps.drop(tos.index)
        else:
            print('ran out of custom physics tossups')
            tos = ot_ps.sample()
            ot_ps = ot_ps.drop(tos.index)
        if len(cb_ps) > 0:
            bon = cb_ps.sample()
            cb_ps = cb_ps.drop(bon.index)
        else:
            print('ran out of custom physics bonuses')
            bon = ob_ps.sample()
            ob_ps = ob_ps.drop(bon.index)
        psqs.append([tos["Question"].values[0], bon["Question"].values[0]])
    lsqs = []
    for i in range(BREAKDOWN[1]):
        tos = ""
        bon = ""
        if len(ct_biology) > 0:
            tos = ct_biology.sample()
            ct_biology = ct_biology.drop(tos.index)
        else:
            tos = ot_biology.sample()
            ot_biology = ot_biology.drop(tos.index)
        if len(cb_biology) > 0:
            bon = cb_biology.sample()
            cb_biology = cb_biology.drop(bon.index)
        else:
            bon = ob_biology.sample()
            ob_biology = ob_biology.drop(bon.index)
        lsqs.append([tos["Question"].values[0], bon["Question"].values[0]])
    esqs = []
    for i in range(BREAKDOWN[2]):
        tos = ""
        bon = ""
        if len(ct_es) > 0:
            tos = ct_es.sample()
            ct_es = ct_es.drop(tos.index)
        else:
            tos = ot_es.sample()
            ot_es = ot_es.drop(tos.index)
        if len(cb_es) > 0:
            bon = cb_es.sample()
            cb_es = cb_es.drop(bon.index)
        else:
            bon = ob_es.sample()
            ob_es = ob_es.drop(bon.index)
        esqs.append([tos["Question"].values[0], bon["Question"].values[0]])
    mathqs = []
    for i in range(BREAKDOWN[3]):
        tos = ""
        bon = ""
        if len(ct_math) > 0:
            tos = ct_math.sample()
            ct_math = ct_math.drop(tos.index)
        else:
            tos = ot_math.sample()
            ot_math = ot_math.drop(tos.index)
        if len(cb_math) > 0:
            bon = cb_math.sample()
            cb_math = cb_math.drop(bon.index)
        else:
            bon = ob_math.sample()
            ob_math = ob_math.drop(bon.index)
        mathqs.append([tos["Question"].values[0], bon["Question"].values[0]])
    qs = psqs + lsqs + esqs + mathqs
    random.shuffle(qs)
    output = ""
    for i in range(len(qs)):
        output += f"TOSS-UP\n {i+1}) {qs[i][0]}\n"
        output += f"BONUS\n {i+1}) {qs[i][1]}\n"
        output += "\n"
    with open(f"packets\\packet{j}.txt", "w", encoding="utf-8") as f:
        f.write(output)