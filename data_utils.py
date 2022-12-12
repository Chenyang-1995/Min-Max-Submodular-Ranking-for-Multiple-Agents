import pandas as pd
import csv
import numpy as np
import math
DEFAULT_LEVELS = 10

def read_data(FILENAME='MFCC.csv'):
    pd_reader = pd.read_csv(FILENAME)
    print("shape = {}".format(pd_reader.shape))
    print('column = {}'.format(pd_reader.columns.tolist()))
    function_list = pd_reader[1:]
    print("function_list_shape = {}".format(function_list.shape))
    level_dict = {}
    max_value_list = pd_reader.max()
    print(len(max_value_list))
    column_id_list = max_value_list.keys().tolist()
    min_value_list = pd_reader.min()
    print(len(min_value_list))
    for column_id in column_id_list:
        tmp_len = max_value_list[column_id]-min_value_list[column_id]
        tmp_step = 1.0*tmp_len/DEFAULT_LEVELS
        level_dict[column_id]=np.arange(min_value_list[column_id],max_value_list[column_id]+tmp_step,tmp_step)
        level_dict[column_id][0]=-1.0*abs(min_value_list[column_id])*2
        level_dict[column_id][-1]= abs(max_value_list[column_id])*2


    return function_list, column_id_list, level_dict

def random_instance_generate(df,column_id_list, level_dict,num_function_per_agent=10,num_agent=10):
    agents_function_list = []
    agents_function_weight_list = []
    for agent_id in range(num_agent):
        functions_per_agent = []
        answers_per_agent = []
        weights_per_agent = []
        for function_index in range(num_function_per_agent):
            function_dict = {}
            function_weight = np.random.randint(100)

            selected_index = np.random.randint(df.shape[0])
            selected_row = df.iloc[selected_index]
            for column_id in column_id_list:
                #randomized_index = np.random.randint(DEFAULT_LEVELS)
                for picked_index in range(len(level_dict[column_id])-1):
                    if selected_row[column_id] >= level_dict[column_id][picked_index] and selected_row[column_id] <= level_dict[column_id][picked_index+1]:
                        function_dict[column_id] = [level_dict[column_id][picked_index],level_dict[column_id][picked_index+1]]

                if column_id not in function_dict.keys():
                    print(column_id)
                    print(selected_row[column_id])
                    print(level_dict[column_id])

            functions_per_agent.append(function_dict)
            weights_per_agent.append(function_weight)

            tmp_df = df


            for column_id in column_id_list:
                tmp_df = tmp_df[(tmp_df[column_id]>=function_dict[column_id][0]) & (tmp_df[column_id]<=function_dict[column_id][1])]

            answers_per_agent.append(tmp_df.shape[0])

        agents_function_list.append([functions_per_agent,answers_per_agent])
        agents_function_weight_list.append(weights_per_agent)

    return agents_function_list,agents_function_weight_list

def convex_instance_generate(df,column_id_list, level_dict,num_function_per_agent=10,num_agent=100,num_point=10):
    agents_function_list = []
    agents_function_weight_list = []
    functions_per_agent = []
    answers_per_agent = []
    for function_index in range(num_function_per_agent):
        function_dict = {}
        #function_weight = np.random.randint(100)

        selected_index = np.random.randint(df.shape[0])
        selected_row = df.iloc[selected_index]
        for column_id in column_id_list:
            #randomized_index = np.random.randint(DEFAULT_LEVELS)
            for picked_index in range(len(level_dict[column_id])-1):
                if selected_row[column_id] >= level_dict[column_id][picked_index] and selected_row[column_id] <= level_dict[column_id][picked_index+1]:
                    function_dict[column_id] = [level_dict[column_id][picked_index],level_dict[column_id][picked_index+1]]

            if column_id not in function_dict.keys():
                print(column_id)
                print(selected_row[column_id])
                print(level_dict[column_id])

        functions_per_agent.append(function_dict)

        tmp_df = df

        for column_id in column_id_list:
            tmp_df = tmp_df[(tmp_df[column_id]>=function_dict[column_id][0]) & (tmp_df[column_id]<=function_dict[column_id][1])]

        answers_per_agent.append(tmp_df.shape[0])

    for agent_id in range(num_point):
        functions_per_agent = []
        answers_per_agent = []
        #weights_per_agent = []

        weights_per_agent = [np.random.randint(100) for _ in range(num_function_per_agent)]

        agents_function_list.append([functions_per_agent,answers_per_agent])
        agents_function_weight_list.append(weights_per_agent)

    for agent_id in range(num_point,num_agent):
        a1,a2 = np.random.choice(agent_id,2)
        lam = 1.0*np.random.uniform(0,1)
        weights_per_agent = [agents_function_weight_list[a1][function_index]*lam+(1.0-lam)*agents_function_weight_list[a2][function_index] for function_index in range(num_function_per_agent) ]

        agents_function_list.append([functions_per_agent,answers_per_agent])
        agents_function_weight_list.append(weights_per_agent)

    return agents_function_list,agents_function_weight_list
