import simpy
import random

env = simpy.Environment()
N = 5
chopsticks = [simpy.Resource(env,capacity=1) for i in range(N)]

class Philosopher():
    T0 = 10 # Mean thinking time
    T1 = 10 # Mean eating time
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
        start_waiting = self.env.now
        self.diag("request chopstick")
        rq1 = self.chopsticks[0].request()
        yield rq1

        self.diag("obtained chopstick")
        yield self.env.timeout(self.DT)

        self.diag("request another chopstick")
        rq2 = self.chopsticks[1].request()
        yield rq2

        self.diag("obtained another chopstick")
        self.waiting += self.env.now - start_waiting
        # return rq1, rq2
        return

    def run_the_party(self): # Do everything
        while True:
            # Thinking
            thinking_delay = random.expovariate(float(1) / self.T1)
            # print thinking_delay
            yield self.env.timeout(thinking_delay)

            # Getting hungry
            get_hungry_p = self.env.process(self.get_hungry())
            rq1, rq2 = get_hungry_p
            # yield get_hungry_p

            # Eating
            eating_delay = random.expovariate(float(1) / self.T1)
            yield self.env.timeout(eating_delay)

            # Done
            self.chopsticks[0].release(rq1)
            self.chopsticks[1].release(rq2)
            self.diag("released the chopsticks")

    def diag(self, message): # Diagnostic routine
        if self.DIAG:
            print("P{} {} @{} ".format(self.id, message, self.env.now))

philosophers = [Philosopher(env, (chopsticks[i], chopsticks[(i + 1) % N]), i) for i in range(N)]

env.run()
