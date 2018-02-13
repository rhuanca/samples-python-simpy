import simpy
import random

env = simpy.Environment()
N = 5
chopsticks = [simpy.Resource(env,capacity=1) for i in range(N)]

class Philosopher():
    T0 = 10 # Mean thinking time
    T1 = 1 # Mean eating time
    DT = 1 # Time to pick another chopstick

    def __init__(self, env, chopsticks, my_id, DIAG = False):
        self.env = env
        self.chopsticks = chopsticks
        self.id = my_id
        self.waiting = 0
        self.DIAG = DIAG
        # Register the process with the environment
        env.process(self.run_the_party())

    def get_hungry(self): # Request the resources
        yield # Do nothing so far

    def run_the_party(self): # Do everything
        yield # ...but do nothing so far

    def diag(self, message): # Diagnostic routine
        if self.DIAG:
            print("P{} {} @{} ".format(self.id, message, self.env.now))

philosophers = [Philosopher(env,
                                (chopsticks[i], chopsticks[(i + 1) % N]), i)
                            for i in range(N)]
