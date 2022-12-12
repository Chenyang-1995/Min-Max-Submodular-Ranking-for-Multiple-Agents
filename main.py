# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
import data_utils
import algorithms as algo
import random
import numpy as np

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

def test(num_function_per_agent=10,num_agent=10):
    df, column_id_list, level_dict=data_utils.read_data("MFCC.csv")
    agents_function_list, agents_function_weight_list = data_utils.random_instance_generate(df, column_id_list, level_dict,num_function_per_agent,num_agent)

    random_solution = column_id_list.copy()
    random.shuffle(random_solution)
    print('Random:')
    random_sol,random_sol_avg = algo.obj_value(agents_function_list,agents_function_weight_list,df,random_solution)

    print('Greedy:')
    greedy_solution = algo.greedy(agents_function_list,agents_function_weight_list,df,column_id_list.copy())
    greedy_sol,greedy_sol_avg = algo.obj_value(agents_function_list,agents_function_weight_list,df,greedy_solution)

    print('Normalized Greedy:')
    normalized_greedy_solution = algo.normalized_greedy(agents_function_list,agents_function_weight_list,df,column_id_list.copy())
    normalized_greedy_sol, normalized_greedy_sol_avg = algo.obj_value(agents_function_list,agents_function_weight_list,df,normalized_greedy_solution)

    print('Ours:')
    our_values = []
    our_values_avg = []
    for decrease_ratio in np.arange(0,1,0.05):
        print(decrease_ratio)
        our_solution = algo.our_algo_with_weight(agents_function_list,agents_function_weight_list,df,column_id_list.copy(),decrease_ratio=decrease_ratio)
        our_value, our_value_avg = algo.obj_value(agents_function_list,agents_function_weight_list,df,our_solution)

        our_values.append(our_value)
        our_values_avg.append(our_value_avg)
    our_sol = min(our_values)
    our_sol_avg = min(our_values_avg)

    return random_sol,greedy_sol,normalized_greedy_sol,our_sol,random_sol_avg,greedy_sol_avg,normalized_greedy_sol_avg,our_sol_avg

# Press the green button in the gutter to run the script.

def KM_test():

    num_agent_list = [10,20,30,40,50,60,70,80,90,100]
    num_function_per_agent_list = [10,20,30,40,50,60,70,80,90,100]

    different_agents_list = []
    different_agents_list_avg = []
    for num_agent in num_agent_list:
        num_function_per_agent=10
        random_sol_list = []
        greedy_sol_list = []
        normalized_greedy_sol_list = []
        our_sol_list = []
        random_sol_list_avg = []
        greedy_sol_list_avg = []
        normalized_greedy_sol_list_avg = []
        our_sol_list_avg = []
        for _ in range(4):
            print('---------num_agent = {0}, num_function = {1}-------------'.format(num_agent,num_function_per_agent))
            random_sol,greedy_sol,normalized_greedy_sol,our_sol,random_sol_avg,greedy_sol_avg,normalized_greedy_sol_avg,our_sol_avg = test(num_function_per_agent,num_agent)
            random_sol_list.append(random_sol)
            greedy_sol_list.append(greedy_sol)
            normalized_greedy_sol_list.append(normalized_greedy_sol)
            our_sol_list.append(our_sol)

            random_sol_list_avg.append(random_sol_avg)
            greedy_sol_list_avg.append(greedy_sol_avg)
            normalized_greedy_sol_list_avg.append(normalized_greedy_sol_avg)
            our_sol_list_avg.append(our_sol_avg)
        different_agents_list.append([random_sol_list,greedy_sol_list,normalized_greedy_sol_list,our_sol_list])
        print(different_agents_list)

        different_agents_list_avg.append([random_sol_list_avg,greedy_sol_list_avg,normalized_greedy_sol_list_avg,our_sol_list_avg])
        print(different_agents_list_avg)


    different_functions_list = []
    different_functions_list_avg = []
    for num_function_per_agent in num_function_per_agent_list:
        num_agent=10
        random_sol_list = []
        greedy_sol_list = []
        normalized_greedy_sol_list = []
        our_sol_list = []
        random_sol_list_avg = []
        greedy_sol_list_avg = []
        normalized_greedy_sol_list_avg = []
        our_sol_list_avg = []
        for _ in range(4):
            print('---------num_agent = {0}, num_function = {1}-------------'.format(num_agent,num_function_per_agent))
            random_sol,greedy_sol,normalized_greedy_sol,our_sol,random_sol_avg,greedy_sol_avg,normalized_greedy_sol_avg,our_sol_avg  = test(num_function_per_agent,num_agent)
            random_sol_list.append(random_sol)
            greedy_sol_list.append(greedy_sol)
            normalized_greedy_sol_list.append(normalized_greedy_sol)
            our_sol_list.append(our_sol)

            random_sol_list_avg.append(random_sol_avg)
            greedy_sol_list_avg.append(greedy_sol_avg)
            normalized_greedy_sol_list_avg.append(normalized_greedy_sol_avg)
            our_sol_list_avg.append(our_sol_avg)


        different_functions_list.append([random_sol_list,greedy_sol_list,normalized_greedy_sol_list,our_sol_list])
        print(different_functions_list)

        different_functions_list_avg.append([random_sol_list_avg,greedy_sol_list_avg,normalized_greedy_sol_list_avg,our_sol_list_avg])
        print(different_functions_list_avg)


    with open('Performance.txt',"w") as file:

        #for index in range(len(CR_Name_list)):
        file.write('different_agents = {}\n'.format(different_agents_list))
        file.write('different_functions = {}\n'.format(different_functions_list))

        file.write('different_agents_avg = {}\n'.format(different_agents_list_avg))
        file.write('different_functions_avg = {}\n'.format(different_functions_list_avg))






if __name__ == '__main__':
    print_hi('PyCharm')
    KM_test()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
