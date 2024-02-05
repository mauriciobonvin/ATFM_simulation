# ATFM_simulation

**Python framework for ATFM Simulation**

This chapter demonstrates how the user can operate the simulation framework in Python.

1.  **Overview**

The structure of the simulation framework consist in 17 modules:

\|- main.py

\| Main file. This script runs the simulation with given parameters.

\|- setup.py

\| Contains functions to instantiate Airlines Agent objects, Platform Agent object, create the flight schedule. Also, receives the parameters to feed the simulation.

\|- ATFMSimulation.py

\| Contains classes and functions to rule the simulation model.

\|- MesaScheduler.py

\| Contains classes and functions to instantiate the Scheduler required by Mesa (framework for Agent Based Modelling simulations).

\|- AirlineAgent.py

\| Contains classes and functions of an Airline Agent.

\|- PlatformAgent.py

\| Contains classes and functions of a Platform Agent.

\|- Regulation.py

\| Contains classes and functions of a Regulation.

\|- Flight.py

\| Contains classes for Scheduled flight and Actual flight.

\|- TimeAssignmentStrategy.py

\| Contains classes for assigning scheduled flights to times.

\|- WindowStrategy.py

\| Contains classes to determine the span of the window of a regulation.

\|- RegulationStrategy.py

\| Contains classes to determine the capacity reduction of a regulation.

\|- PriorityAssignmentStrategy.py

\| Contains classes to determine which flights will be prioritized by an airline during simulation.

\|- DesiredTimeStrategy.py

\| Contains classes to determine the desired time of a priority flight.

\|- AssignMarginsStrategy.py

\| Contains classes to determine the time not before and time not after margins of a flight.

\|- optimization_strategy.py

\| Contains classes and functions to execute the optimization algorithm.

\|- equity_handler.py

\| Contains classes and functions to handle the equity mechanism.

\|- credits_clearing.py

\| Contains classes and functions to handle the equity mechanism from [C.G. Schuetz; S. Ruiz; E. Gringinger, C. Fabianek, T. Loruenser; “An auction-based mechanism for a privacy-preserving marketplace for ATFM slots”, 33rd Congress of the International Council of the Aeronautical Sciences, 2022].

1.  **Dependencies**

The package is run on Python version 3.10.9.

The following packages are required to install before running the code:

**numpy:** A powerful library for numerical computations in Python.

Version: 1.24.2

Official documentation: <https://numpy.org/doc/>

**random:** A module for generating random numbers and making random selections in Python.

Official documentation: <https://docs.python.org/3/library/random.html>

**copy:** A module providing support for shallow and deep copying operations in Python.

Official documentation: <https://docs.python.org/3/library/copy.html>

**docplex.mp.model**: A module from the \`docplex\` library, which is an optimization modeling library for Python provided by IBM Decision Optimization.

Version: 2.25.236

Official documentation: <https://ibmdecisionoptimization.github.io/docplex-doc/mp/docplex.mp.model.html>

The free version of this package is limited and it is recommended to obtain an academic license for its use.

Website of academic license: <https://community.ibm.com/community/user/ai-datascience/blogs/xavier-nodet1/2020/07/09/cplex-free-for-students>

**mesa**: is an agent-based modeling (or ABM) framework in Python.

Version: 2.1

Official documentation: <https://mesa.readthedocs.io/en/stable/>

1.  **Parameter configuration**

In file “setup.py” the following parameters have to be provided:

| **Parameter**                     | **Data type**                                                                     | **Meaning and example**                                                                                                                               |
|-----------------------------------|-----------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| Steps                             | Data type: integer                                                                | Number of consecutive iterations the simulation will perform. E.g. “steps”: 5, will run the simulation 5 times.                                       |
| n_times\_                         | Data type: integer                                                                | Number of available times in a day for flight arrivals at the airport.                                                                                |
| starting_seed\_                   | Data type: integer                                                                | Starting seed to reproduce results. Seed will be incremented by 1 every step.                                                                         |
| capacity\_                        | Data type: integer                                                                | Indicates the capacity reduction in the regulation window. E.g. A capacity of 2 is equal to every other slot being removed.                           |
| airlines_flights\_                | Data structure: Dictionary Data type for key: string Data type for value: integer | A dictionary where the key term is the name of the airline and the value term is the number of flights that were delayed. E.g. “Austrian Airlines”: 5 |
| base_value_weight_map\_           | Data type: integer                                                                | Maximum value assigned to the weight map.                                                                                                             |
| percentage_reduction_weight_map\_ | Data type: float                                                                  | Percentage reduction of the base value weight map.                                                                                                    |
| bonus\_                           | Data type: float                                                                  | Percentage of bonus to share between market creators for the equity mechanism presented in credits_clearing.py                                        |

1.  **Strategies**

In file “setup.py” the following strategies have to be instantiated. There can be one or more possible strategies to choose from:

| **Strategy**               | **Meaning**                                                                                                                                        | **Strategies**                                                                                                                                                                                                                                                                                                |
|----------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|  TimeAssignmentStrategy    | Imported from “TimeAssignmentStrategy.py”. Define the strategy for assigning scheduled flights to times.                                           | RandomTimeAssignmentStrategy: assigns flights to times randomly following a uniform distribution. SequentialTimeAssignmentStrategy: assigns flights to times sequentially.                                                                                                                                    |
|  WindowStrategy            | Imported from “WindowStrategy.py”. Define the strategy to determine the span of the window of a regulation.                                        | RandomWindowStrategy: assigns window start time and end time randomly following a uniform distribution.                                                                                                                                                                                                       |
| RegulationStrategy         | Imported from “RegulationStrategy.py”. Define the strategy to determine the capacity reduction of a regulation.                                    | ReducedCapacityStrategy: reduce available slots in the regulation window according to the capacity parameter.                                                                                                                                                                                                 |
| PriorityAssignmentStrategy | Imported from “PriorityAssignmentStrategy.py”. Define the strategy to determine which flights will be prioritized by an airline during simulation. | PriorityRandomAssignmentStrategy: priority randomly following a uniform distribution.                                                                                                                                                                                                                         |
| DesiredTimeStrategy        | Imported from “DesiredTimeStrategy.py”. Define the strategy to determine the desired time of a priority flight.                                    | DesiredTimeRandomAssignmentStrategy: assigns desired time randomly following a uniform distribution.                                                                                                                                                                                                          |
| AssignMarginsStrategy      | Imported from “AssignMarginsStrategy.py”. Define the strategy to determine the time not before and time not after margins of a flight.             | MarginsRandomAssignmentStrategy: assigns time not after and time not before randomly following a uniform distribution.                                                                                                                                                                                        |
| Optimization_strategy      | Imported from “Optimization_strategy.py”. Define the strategy to execute the optimization algorithm.                                               | LinearAssignmentStrategy: defines the optimization solver as a Linear Assignment problem to maximize the utility.                                                                                                                                                                                             |
| Equity_handler             | Imported from “equity_handler.py”. Define the strategy to handle the equity mechanism.                                                             | CreditsCLearingStrategy: defines the EquityHandler to be as described in [C.G. Schuetz; S. Ruiz; E. Gringinger, C. Fabianek, T. Loruenser; “An auction-based mechanism for a privacy-preserving marketplace for ATFM slots”, 33rd Congress of the International Council of the Aeronautical Sciences, 2022].  |

1.  **Creating objects**
    1.  **Creating Airline objects**

When running the file “setup.py” the file “AirlineAgent.py” is imported. This file contains the class Airline that represents an airline with its name and number of flights. To create an airline object the following strategies have to be instantiated previously:

-   priority_assignment_strategy,
-   desired_time_strategy,
-   assign_margins_strategy

Here is an example on how to initialize an airline in the setup file: With the following function create a list to contain the Airline objects, then with a “for loop” iterate over the dictionary items provided in the parameters to obtain the name of airlines and number of flights.

**Function to create airline agents.**

*\# Create ariline agents*

*def airline_agents(airlines_flights,*

*priority_assignment_strategy,*

*desired_time_strategy,*

*assign_margins_strategy*

*):*

*airline_list = []*

*counter = 1 \#ID for scheduler*

*for airline_name, number_of_flights in airlines_flights.items():*

*\# Create an AirlineAgent with the specified attributes*

*airline\_ = AirlineAgent.AirlineAgent(counter,*

*None, \# initialize without model*

*airline_name,*

*number_of_flights,*

*priority_assignment_strategy,*

*desired_time_strategy,*

*assign_margins_strategy*

*)*

*airline_list.append(airline_)*

*\# Increase the counter for agent IDs*

*counter += 1*

*return airline_list*

**Instanciate airlines agents in a list data structure.**

*list_airline_agents\_ = airline_agents(airlines_flights,*

*priority_assignment_strategy,*

*desired_time_strategy,*

*assign_margins_strategy*

*)*

1.  **Creating Platform object**

When running the file “setup.py” the file “PlatformAgent.py” is imported. This file contains the class Platform that represents the platform that contains the optimizer and the equity handler. To create this object the following strategies have to be instantiated previously:

-   Optimization strategy,
-   Equity handler

Here is an example on how to initialize a platform agent in the setup file:

*platform_agent_= PlatformAgent.PlatformAgent(len(airlines_flights) +1,*

*None, \# initialize without model*

*base_value_weight_map_,*

*percentage_reduction_weight_map_,*

*optimization_strategy_,*

*bonus_,*

*equity_strategy\_*

*)*

1.  **Create Flight schedule**

In the “setup.py” file the flight schedule have to be provided. An example of how to create the schedule is given by the following function.

**Function:**

*def flights_schedule(list_of_airlines, n_times, seed):*

*\# Group airlines flight objects in a list*

*scheduled_flights_object_list = [scheduled_flight for airline in list_of_airlines for scheduled_flight in airline.scheduled_flights_objects_list]*

*scheduled_flights_object_list = time_assignment_strategy.assign_time(scheduled_flights_object_list,*

*n_times,*

*seed)*

*return scheduled_flights_object_list*

**variable with flight schedule:**

*flight_schedule\_ = flights_schedule(list_airline_agents_,n_times_, starting_seed_)*

1.  **Instantiate remaining strategies**

The following strategies must be instantiated in the “setup.py” file and given as parameter to the simulation model as they are used to create the regulation at every step:

-   WindowStrategy
-   RegulationStrategy

Example:

*window_strategy\_ = WindowStrategy.RandomWindowStrategy()*

*regulation_strategy\_ = RegulationStrategy.ReducedCapacityStrategy()*

1.  **Run simulation**

After the “setup.py” file was populated with the required parameters, instantiated the strategies and the agents and created the flight schedule, the file “main.py” can be run to perform the simulations.
