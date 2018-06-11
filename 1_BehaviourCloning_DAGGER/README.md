# Imitation Learning(Behaviour Cloning and DAGGAR)

**Dependencies**: 
-TensorFlow   
-MuJoCo version 1.31 /1.51  
-OpenAI Gym  
-Microsoft Visual C++ ??


**Note**: MuJoCo versions until 1.5 do not support NVMe disks therefore won't be compatible with recent Mac machines.
There is a request for OpenAI to support it that can be followed [here](https://github.com/openai/gym/issues/638).

The only file that you need to look at is `run_expert.py`,`dagger.py` which is code to load up an expert policy, run a specified number of roll-outs, and save out data.

In `experts/`, the provided expert policies are:
* Ant-v1.pkl
* HalfCheetah-v1.pkl
* Hopper-v1.pkl
* Humanoid-v1.pkl
* Reacher-v1.pkl
* Walker2d-v1.pkl

**Example Usage**
```%run run_expert.py experts/Hopper-v1.pkl Hopper-v2 --render --num_rollouts 10
  ```

The name of the pickle file corresponds to the name of the gym environment.

### 1. Does Behaviour Cloning a using a four layered neural net Agent converge while imitating the expert's policy?? ###

The expert that we are trying to imitate here is the Hopper-v2.

![img](/hopper.PNG)

Plot showing the training loss as a function of the number of epochs is shown below.

![img](/warmup.png)