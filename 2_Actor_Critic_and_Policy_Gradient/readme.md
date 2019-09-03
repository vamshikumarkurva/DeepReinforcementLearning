Deep Reinforcement Learning Based Control in Continuous Action and State Spaces using Policy Gradients and Actor-Critic Networks
================================

## Policy Gradients:

The aim of any RL algorithm is to maximize the expected reward from any given state.

![](http://latex.codecogs.com/svg.latex?\theta^{*}%3Darg\max_{\theta}E\Big[\sum_{t}R(s_t%2Ca_t)\Big])

Policy Gradients directly differentiates the above objective to maximize the reward, which gives the REINFORCE algorithm. The name is an acronym for 'REward Increment = Non-negative Factor *times* Offset Reinforcement *times* Characteristic Eligibility' which is mentioned in [simple statistical gradient-following algorithms for connectionist reinforcement learning](http://www-anw.cs.umass.edu/~barto/courses/cs687/williams92simple.pdf).


![](Images/reinforce.png)

The second step of the algorithm, which is computing the gradients is similar to that of maximum-likelihood, except for two changes.

1. In supervised learning, we have access to the correct label for every input. But in Ploicy gradients, we sample an action from the policy and use it as the label. But the problem is we don't know whether the action is good or bad until the end of the episode. This is called the '*Credit assignment*' problem. But, if an action leads to more good actions over the time than the bad ones, it's likely to recieve more positive updates over the time.
2. The gradients are multiplied by the cumulative expected reward, which means the actions that leads to good outcomes are encouraged and the ones that leads to bad outcomes are discouraged.

Note: Policy Gradients is an on-policy algorithm, i.e. everytime the network/policy gets updated, we need to generate new samples from the updated policy.

## Actor-critic Algorithms:

Plocy Gradient algorithms like REINFORCE needs to generate the entire episode until the end, to estimate the returns and make an update. For environments where episodes last for hundereds or thousands of time frames, these algorithms need to wait for a long time just to make a single update. This kind of algorithms comes under Monte-Carlo algorithms. Actor-Critic algorithms on the other hand estimate the value-function or Q-function of the current policy using the critic network and uses it to improve the policy(Actor network). These algorithms fall under temporal difference (TD) methods, can make an update at every single step of the episode using the immediate reward and bootstrap estimate. In general, value function is estimated using the critic network.

![](http://latex.codecogs.com/svg.latex?V^{\pi}(s_t)%3DR(s_t%2Ca_t)%2B\sum_{a_t}\pi(a_t%2Fs_t)\Big(\sum_{s_{t%27}}P(s_{t%27}%2Fs_t%2Ca_t)V^{\pi}(s_{t%27})\Big))

After sampling the current state, action, next state and the reward, fit the value function using the following bootstrapped estimate

![](http://latex.codecogs.com/svg.latex?V^{\pi}(s_t)%3DR(s_t%2Ca_t)%2B\gamma%20V^{\pi}(s_{t%27}))

![](Images/actor_critic.png)

Note: Actor-critic is also an on-policy algorithm. Samples generated have to be from the current policy.

## How To Use

**Dependencies**

-TensorFlow   
-MuJoCo version 1.31 /1.51  
-OpenAI Gym
-OpenCV
-Microsoft Visual C++ 

 **Usage**

```
python train_pg.py InvertedPendulum-v2 --render -n 100 -b 5000 -e 5 -rtg --exp_name lb_continuous_5_layered_DeepNeuralNet -l 3 -lr 1e-2
```

**[Detailed Instructions](http://rail.eecs.berkeley.edu/deeprlcourse-fa17/f17docs/hw2_final.pdf)**

## Experiment 1: Cart Pole with Discrete Action 

The [cart-pole model](http://www.derongliu.org/adp/adp-cdrom/Barto1983.pdf) has four state variables
> The 4 numbers in the box space for observation represents: [position of cart, velocity of cart, angle of pole, rotation rate of pole]

![](Images/math1.png)


**Observation 1**: Comparing Fig 1 and Fig 2, it is clear that having a larger
    batch size helps in faster learning and better policies in terms of Average
    Returns.

**Observation 2**: From Fig 3 it is clear that state/action centric policy(green) gives much better policies. than a trajectory centric policy(red).

![](Images/equation2.gif)
Equation [2](https://docs.google.com/document/d/1Iw_TUijQ-C6F0M3mWWco8_rDiuEblKvtr8mCB3ITLas/edit#bookmark=id.ykbyvnen9iwg)

Also Advantage normalization gives slightly better policies.

**Observation 3**: However having a baseline didn’t improve the policy as expected as shown in figure 3.

![](Images/graph_small_batch.png)

Figure 1

![](Images/graph_large_batch.png)

Figure 2

![](Images/large_optimal.png)

Figure 3

![](Images/with-without-critic.png)

Figure 4

 
## Experiment 2: Inverted Pendulum with Continuous Actions

 Command Line Code
```
python train_pg.py InvertedPendulum-v2 --render -n 100 -b 5000 -e 5 -rtg --exp_name lb_continuous_5_layered_DeepNeuralNet -l 3 -lr 1e-2
```

![](Images/pendulum_continuous.PNG)

Figure 5

 **Observation 1:** The learning curves with two different network architectures
    is shown in Fig 6. Its clear from the graph that the 5 layered feed forward
    neural network learned better policies in lesser number of iterations.

![](Images/inverted.png)

Figure 6


## Experiment 3: HALF CHEETAH(Continuous Actions)

Code Block

```
python train_pg.py HalfCheetah-v2 -ep 150 --discount 0.9 -b 40000 -rtg -l 3 -s 32 -lr 4e-2 --exp_name half_cheetah
```

[Half-Cheetah](http://prac.elka.pw.edu.pl//~pwawrzyn/pub-s/0601_SLEAC.pdf), is a planar kinematic string of 9 links and 10 joints; the
“paws” of Half-Cheetah will also be called joints. The angles of 4-th and 5-th
joint are fixed, all the the others are controllable. Consequently, Half-Cheetah
is a 6-degree-of-freedom walking robot.

![](Images/half-ch.PNG)

Figure 7

![](Images/half-cheetah.png)

Figure 8


**Observation 1:** After a lot of hyper parameter tuning, the settings that gave
an average return above 150 before 100 iterations is given in the code block
below. It used an unusually high batch size and a 5 layered deep neural network
without a critic.

**Observation 2:** We also tested the variance reduction techniques with n-step returns and with critic.

![](http://latex.codecogs.com/svg.latex?\nabla_{\theta}J(\theta)%3D\sum_{i%3D1}^{N}\sum_{t%3D1}^{T}\nabla_{\theta}\log\pi_{\theta}(a_{it}/s_{it})%20A(s_{it}%2Ca_{it}))

where,

![](http://latex.codecogs.com/svg.latex?A(s_{t}%2Ca_{t})%3Dr(s_t%2Ca_t)%2B\gamma.V^{\pi}_{\phi}(s_{t%2B1})-V^{\pi}_{\phi}(s_t))

in case of simple actor-critic

![](http://latex.codecogs.com/svg.latex?A^{\pi}_{n}(s_t%2Ca_t)%3D\sum_{t%27%3Dt}^{t%2Bn}\gamma^{t%27-t}r(s_{t%27}%2Ca_{t%27})+\gamma^{n}V^{\pi}_{\phi}(s_{t%27%2Bn})-V^{\pi}_{\phi}(s_{t%27})) 

in case of n-step returns

Here is the plot of average returns over no of iterations. n-step return estimate is supposed to have less variance by cutting the track after n-steps.

![](Images/critic_vs_nocritic.png)


Figure 9

**Observation 3** GAE(Generalized Advantage Return) is a weighted combinations of n-step returns.
It introduces a new parameter lambda, which controls the tradeoff between bias and variance. 

![](http://latex.codecogs.com/svg.latex?A^{\pi}_{GAE}(s_t%2Ca_t)%3D\sum_{n%3D1}^{\infty}w_nA^{\pi}_{n}(s_t%2Ca_t))

![](http://latex.codecogs.com/svg.latex?A^{\pi}_{GAE}(s_t%2Ca_t)%3D\sum_{t%27%3Dt}^{\infty}(\gamma\lambda)^{t%27-t}\delta_{t%27})

and

![](http://latex.codecogs.com/svg.latex?\delta_{t}%3Dr(s_t%2Ca_t)+\gamma%20V^{\pi}_{\phi}(s_{t%2B1})-V^{\pi}_{\phi}(s_t))

When lambda=0, the estimator becomes a simple actor-critic model with less variance but with bias.

![](http://latex.codecogs.com/svg.latex?A^{\pi}_{GAE}(s_t%2Ca_t)%3D\delta_{t}%3Dr(s_t%2Ca_t)+\gamma%20V^{\pi}_{\phi}(s_{t%2B1})-V^{\pi}_{\phi}(s_t))

With lambda=1, advantage estimator becomes the empirical sum of returns with average baseline. It has more variance because
of sum of terms but with less bias. Here the plot shows the average return for different values of lambda.

![](http://latex.codecogs.com/svg.latex?A^{\pi}_{GAE}(s_t%2Ca_t)%3D\sum_{t%27%3Dt}^{\infty}(\gamma)^{t%27-t}\delta_{t%27}%20-%20V^{\pi}_{\phi}(s_t))


![](Images/GAE.png)

Figure 10

Here we can see that when lamba = 0.7, variance is minimum.

All the experiments with n-step returns and GAE used the same actor model(2 layers with 20, 10 units successively)
and same critic model(3 layers with 20, 15 and 10 units).


## REFERENCES


1. Paweł Wawrzynski, [Learning to Control a 6-Degree-of-Freedom Walking Robot](http://prac.elka.pw.edu.pl//~pwawrzyn/pub-s/0601_SLEAC.pdf) 

2. Ronald J. Williams, [simple statistical gradient-following algorithms for connectionist reinforcement learning](http://www-anw.cs.umass.edu/~barto/courses/cs687/williams92simple.pdf) 

3. A. G. Barto, R. S. Sutton, and C. W. Anderson, [“Neuronlike adaptive elements
that can solve difficult learning control problems”](
http://www.derongliu.org/adp/adp-cdrom/Barto1983.pdf)

4. John Schulman, Philipp Moritz, Sergey Levine, Michael I. Jordan and Pieter Abbee [HIGH DIMENSIONAL CONTINUOUS CONTROL USING GENERALIZED ADVANTAGE ESTIMATION](https://arxiv.org/pdf/1506.02438.pdf)

5. CS 294: Deep Reinforcement Learning, Fall 2017

 

 
