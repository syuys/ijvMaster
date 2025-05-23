#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 21:17:21 2021

@author: md703
"""

from mcx_ultrasound_opsbased import MCX
import postprocess
import json
import os

# %% Setting
sessionIDSet = ["ijv_dis_mus_lb_bloodG_low", "ijv_col_mus_lb_bloodG_low"]
# runningNum = False  # (Integer or False)
cvThold = 0.05
repeatTimes = 10
muaPath = "mua.json"


# run each sessionID
projectCV = {}
for sessionID in sessionIDSet:
    # load mua for calculating reflectance
    with open(os.path.join(sessionID, muaPath)) as f:
        mua = json.load(f)
    muaUsed =[mua["1: Air"],
              mua["2: PLA"],
              mua["3: Prism"],
              mua["4: Skin"],
              mua["5: Fat"],
              mua["6: Muscle"],
              mua["7: Muscle or IJV (Perturbed Region)"],
              mua["8: IJV"],
              mua["9: CCA"]
              ]
    
    
    # Do simulation
    # initialize
    simulator = MCX(sessionID)
    with open(os.path.join(sessionID, "config.json")) as f:
        config = json.load(f)
    simulationResultPath = os.path.join(config["OutputPath"], sessionID, "post_analysis", "{}_simulation_result.json".format(sessionID))
    with open(simulationResultPath) as f:
        simulationResult = json.load(f)
    existedOutputNum = simulationResult["RawSampleNum"]
    
    # run forward mcx
    with open(simulationResultPath) as f:
        simulationResult = json.load(f)
    needAddOutputNum = repeatTimes - existedOutputNum % repeatTimes
    for idx in range(existedOutputNum, existedOutputNum+needAddOutputNum):
        # run
        simulator.run(idx)
        # save progress 
        simulationResult["RawSampleNum"] = idx+1
        with open(simulationResultPath, "w") as f:
            json.dump(simulationResult, f, indent=4)
    existedOutputNum = existedOutputNum + needAddOutputNum
    # calculate reflectance
    raw, reflectance, reflectanceMean, reflectanceCV, totalPhoton, groupingNum = postprocess.analyzeReflectance(sessionID, mua=muaUsed)
    projectCV[sessionID] = reflectanceCV.max()
    print("Session name: {} \nReflectance mean: {} \nCV: {} \nNecessary photon num: {:.4e}".format(sessionID, 
                                                                                                   reflectanceMean, 
                                                                                                   reflectanceCV, 
                                                                                                   totalPhoton*groupingNum), 
          end="\n\n")


# run the session which has higher cv
while max(projectCV.values()) > cvThold:
    sessionID = max(projectCV, key=projectCV.get)
    # load mua for calculating reflectance
    with open(os.path.join(sessionID, muaPath)) as f:
        mua = json.load(f)
    muaUsed =[mua["1: Air"],
              mua["2: PLA"],
              mua["3: Prism"],
              mua["4: Skin"],
              mua["5: Fat"],
              mua["6: Muscle"],
              mua["7: Muscle or IJV (Perturbed Region)"],
              mua["8: IJV"],
              mua["9: CCA"]
              ]
    
    
    # Do simulation
    # initialize
    simulator = MCX(sessionID)
    with open(os.path.join(sessionID, "config.json")) as f:
        config = json.load(f)
    simulationResultPath = os.path.join(config["OutputPath"], sessionID, "post_analysis", "{}_simulation_result.json".format(sessionID))
    with open(simulationResultPath) as f:
        simulationResult = json.load(f)
    existedOutputNum = simulationResult["RawSampleNum"]
    
    # run forward mcx
    with open(simulationResultPath) as f:
        simulationResult = json.load(f)
    needAddOutputNum = repeatTimes - existedOutputNum % repeatTimes
    for idx in range(existedOutputNum, existedOutputNum+needAddOutputNum):
        # run
        simulator.run(idx)
        # save progress 
        simulationResult["RawSampleNum"] = idx+1
        with open(simulationResultPath, "w") as f:
            json.dump(simulationResult, f, indent=4)
    existedOutputNum = existedOutputNum + needAddOutputNum
    # calculate reflectance
    raw, reflectance, reflectanceMean, reflectanceCV, totalPhoton, groupingNum = postprocess.analyzeReflectance(sessionID, mua=muaUsed)
    projectCV[sessionID] = reflectanceCV.max()
    print("Session name: {} \nReflectance mean: {} \nCV: {} \nNecessary photon num: {:.4e}".format(sessionID, 
                                                                                                   reflectanceMean, 
                                                                                                   reflectanceCV, 
                                                                                                   totalPhoton*groupingNum), 
          end="\n\n")