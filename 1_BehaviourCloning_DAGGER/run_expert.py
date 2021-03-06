#!/usr/bin/env python

"""
Code to load an expert policy and generate roll-out data for behavioral cloning.
Example usage:
            %run run_expert.py experts/Hopper-v1.pkl Hopper-v2 --render --num_rollouts 10

Dagger and Behaviour Clonning Implementation : @uthor : vaisakhs (vaisakhs.shaj@gmail.com)
Author of this script and included expert policies: Jonathan Ho (hoj@openai.com)


"""

import pickle
import tensorflow as tf
import numpy as np
import tf_util
import gym
import load_policy
import matplotlib.pyplot as plt
from keras.layers.advanced_activations import LeakyReLU, PReLU

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('expert_policy_file', type=str)
    parser.add_argument('envname', type=str)
    parser.add_argument('--render', action='store_true')
    parser.add_argument("--max_timesteps", type=int)
    parser.add_argument('--num_rollouts', type=int, default=20,
                        help='Number of expert roll outs')
    args = parser.parse_args()
    

    print('loading and building expert policy')
    policy_fn = load_policy.load_policy(args.expert_policy_file)
    print('loaded and built')

    with tf.Session():
        tf_util.initialize()

        import gym
        env = gym.make(args.envname)
        max_steps = args.max_timesteps or env.spec.timestep_limit
        returns = []
        observations = []
        actions = []
        for i in range(args.num_rollouts):
            print('iter', i)
            obs = env.reset()
            done = False
            totalr = 0.
            steps = 0
            while not done:
                action = policy_fn(obs[None,:])
                #print(action.shape)
                observations.append(obs)
                actions.append(action)
                obs, r, done, _ = env.step(action)
                #print(r)
                totalr += r
                steps += 1
                if args.render:
                    env.render()
                if steps % 100 == 0: print("%i/%i"%(steps, max_steps))
                if steps >= max_steps:
                    break
            returns.append(totalr)

        print('returns', returns)
        print('mean return', np.mean(returns))
        print('std of return', np.std(returns))

        expert_data = {'observations': np.array(observations),
                       'actions': np.array(actions)}
        
        return expert_data,args
    
def behaviourCloning(expert_data,args):
    from keras import utils
    from keras.models import Sequential
    from keras.layers import Dense, Dropout, Activation
    from keras.layers.advanced_activations import LeakyReLU, PReLU
    xTr=expert_data['observations']
    yTr=expert_data['actions']

    import numpy as np
    #print(xTr.shape)
    #print(yTr.shape)
    yTr=np.reshape(yTr,(yTr.shape[0],yTr.shape[2]))
    #construct Model
    model = Sequential()
    model.add(Dense(120, input_dim=xTr.shape[1], init="uniform",
        activation="linear"))
    model.add(LeakyReLU(alpha=.01))
    model.add(Dropout(0.5))
    model.add(Dense(100, init="uniform", activation="linear"))
    model.add(LeakyReLU(alpha=.01))
    model.add(Dropout(0.5))
    model.add(Dense(80, init="uniform", activation="linear"))
    model.add(LeakyReLU(alpha=.01))
    model.add(Dropout(0.5))
    model.add(Dense(yTr.shape[1]))
    
    #compile Model
    model.compile(loss='mean_squared_error',
                  optimizer='adam',
                  metrics=['accuracy'])
    model.save_weights(R"D:\MCAFEE\GITHUB\DeepReinforcementLearning\BehaviourCloning-DAGGER\Policies\policyDNNBC.h5")
    
    history=model.fit(xTr, yTr,
              epochs=12,
              batch_size=256,validation_split=0.1)
    #print(history.history['loss'])
    
    #print(model.predict(xTr))
    ######### Training Error Plot
    det=list()
    for i,e in enumerate(history.history['loss'],0):
        det.append(e)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    det=np.log(det)
    det=[round(float(x),3) for x in det]
    plt.plot(range(len(det)),det, linestyle='dashed', marker='o',
         markerfacecolor='blue', markersize=12)
    for x, y in zip( range(len(det)), det):
        plt.text(x, y, str(y), color="blue", fontsize=12)
    plt.title("Log Loss Vs Epoch Curve")
    plt.xlabel("epoch")
    plt.ylabel("Log Loss")
    plt.grid()
    plt.show()
    ################################################################################
    
    env = gym.make(args.envname)
    max_steps = args.max_timesteps or env.spec.timestep_limit
    returns = []
    observations = []
    actions = []
    obs = env.reset()
    done = False
    totalr = 0
    steps = 0
    while not done:
        predicted_action = model.predict(np.array(obs[None,:]))
        obs, r, done, _ = env.step(predicted_action)
        totalr += r
        steps += 1
        if args.render:
            env.render()
        if steps >= max_steps:
            break
    print("BC ",totalr)
    model.save_weights(r"C:\Users\DELL\Desktop\GITHUB\DeepReinforcementLearning\1_BehaviourCloning_DAGGER\Policies\policyDNN_ANTBC.h5")
    returns.append(totalr)

    print('returns', returns)
 

    
    

if __name__ == '__main__':
    expert_data,args=main()
    ed2=behaviourCloning(expert_data,args)
