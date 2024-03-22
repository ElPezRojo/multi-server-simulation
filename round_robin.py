import sys
from queue import Queue as Q
import random
import math

num_servers = 1
num_customers = 10000
mu = 3
lmbda = 4
rand_seed = 12


if len(sys.argv) > 1:
    num_servers = int(sys.argv[1])
if len(sys.argv) > 2:
    num_customers = int(sys.argv[2])
if len(sys.argv) > 3:
    mu = float(sys.argv[3])
if len(sys.argv) > 4:
    lmbda = float(sys.argv[4])
if len(sys.argv) > 5:
    rand_seed = float(sys.argv[5])

# mu = 1/mu
lmbda = 1/lmbda
    
DEPARTURE = -1
ARRIVAL = 1

random.seed(rand_seed)
all_customers = []
queues = [[] for i in range(num_servers)]
event_list = []

class Customer:
    def __init__(self, C_AT):
        self.arrival_time = C_AT
        self.service_time = 0
        self.departure_time = 0
        self.queuing_time = 0
        self.service_start_time = 0
        
class Event:
    
    def __init__(self,  E_customer:Customer, E_time:float, E_type:int):
        self.customer: Customer = E_customer
        self.time: float = E_time
        self.type: int = E_type
        
    def is_departure(self): 
        if(self.type == DEPARTURE):
            return True
        else:
            return False
    
    def get_time(e):
        return e.time
        
        

class Event_List:
    def __init__(self):
        l = []
    
    def add(self, item:Event):
        self.l:list
        self.l.append(item)
        self.l.sort(key=Event.get_time)
        
    def get(self):
        item = self.l.pop()
    
    def is_empty(self):
        return len(self.l) == 0
        

def get_exponential(mean):
    ret_val = -mean * math.log(random.random())
    while ret_val < 0:
        ret_val = -mean * math.log(random.random())
    return ret_val

def init_customers():
    clock = 0.0
    customer_list = []
    for x in range(num_customers):
      interarrival_time = get_exponential(lmbda)
      c: Customer = Customer(clock)
      all_customers.append(c)
      customer_list.append(c)
      clock += interarrival_time
    
    for x in range(num_customers):
        cur_queue = queues[x % num_servers]
        cur_queue.append(customer_list[x])

init_customers()
total_simulation_time = 0.0
done_queues = [[] for i in range(num_servers)] 

for s in range(num_servers):
    clock = 0.0
    cur_queue = queues[s]
    cur_done_queue = done_queues[s]
    cur_queue_size = len(cur_queue)
    for c in range(cur_queue_size):
        service_time = get_exponential(mu)
        cur_customer: Customer = cur_queue.pop(0)
        cur_customer.queuing_time = clock - cur_customer.arrival_time
        if(clock < cur_customer.arrival_time):
            clock = cur_customer.arrival_time
        cur_customer.service_time = service_time
        cur_customer.service_start_time = clock
        
        clock += service_time
        cur_customer.departure_time = clock
        cur_done_queue.append(cur_customer)
    last_ele = len(cur_done_queue) - 1
    if(last_ele >= 0 and cur_done_queue[last_ele].departure_time > total_simulation_time):
        total_simulation_time = cur_done_queue[last_ele].departure_time
    

avg_time_spent_in_system = 0
for c in all_customers:
    c:Customer
    avg_queue_time = 0
    avg_waiting_time = 0
    
    
    avg_time_spent_in_system += (c.departure_time - c.arrival_time)/num_customers

print("avg time spent in system: " + str(avg_time_spent_in_system))



max_q_len = 0
for s_num in range(len(done_queues)):
    q = done_queues[s_num]
    avg_line_length = 0.0
    events = []
    cur_line_len = 0
    clock = 0.0
    while(len(q) != 0):
        clock = 0
        cur_customer = q.pop(0)
        events.append([cur_customer.arrival_time, ARRIVAL])
        events.append([cur_customer.service_start_time, DEPARTURE])
    
    events.sort(key=lambda x: x[0])

    for x in events:
        if(cur_line_len > max_q_len):
            max_q_len = cur_line_len
        avg_line_length += cur_line_len * ((x[0] - clock) / total_simulation_time)
        cur_line_len += x[1] 
        clock = x[0]
        
    print("avg length of server " + str(s_num + 1) +"'s queue: " + str(avg_line_length))
print("max queue length: " + str(max_q_len))



    
    

        
        
    
        
      
