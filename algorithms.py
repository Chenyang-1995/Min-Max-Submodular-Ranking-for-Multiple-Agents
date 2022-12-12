import data_utils
import numpy as np

def obj_value(agents_function_list,agents_function_weight_list,df,solution):
    agents_cover_time = []
    for agent_index in range(len(agents_function_list)):

        cover_time = []
        functions_per_agent,answers_per_agent = agents_function_list[agent_index]
        weights_per_agent = agents_function_weight_list[agent_index]

        for function_index in range(len(answers_per_agent)):
            tmp_df = df
            tmp_function_dict = functions_per_agent[function_index]
            tmp_answer = answers_per_agent[function_index]
            for column_index, column_id in enumerate(solution):
                tmp_df = tmp_df[(tmp_df[column_id]>=tmp_function_dict[column_id][0]) & (tmp_df[column_id]<=tmp_function_dict[column_id][1])]
                if tmp_df.shape[0] == tmp_answer:
                    cover_time.append((column_index+1)*weights_per_agent[function_index])
                    break
        cover_time = np.array(cover_time)
        agents_cover_time.append(cover_time)

    agents_cover_time = [np.average(x) for x in agents_cover_time]

    print(agents_cover_time)
    print(max(agents_cover_time))
    print(np.average(np.array(agents_cover_time)))
    return max(agents_cover_time), np.average(np.array(agents_cover_time))

def greedy(agents_function_list,agents_function_weight_list,df,column_id_list):
    total_functions = []
    total_answers = []
    total_ranges = []
    total_weights = []
    num_rows = df.shape[0]
    for agent_index in range(len(agents_function_list)):
        functions_per_agent,answers_per_agent = agents_function_list[agent_index]
        weights_per_agent = agents_function_weight_list[agent_index]
        total_weights += weights_per_agent
        total_functions += functions_per_agent
        total_answers += answers_per_agent
        for a in answers_per_agent:
            total_ranges.append(num_rows-a)

    tmp_dfs = [df[:] for _ in range(len(total_answers))]

    solution = []
    remaining_column_list = column_id_list
    while len(remaining_column_list)>0:
        max_contri = 0
        max_column = remaining_column_list[0]
        for column_id in remaining_column_list:
            tmp_contri = 0
            for function_index in range(len(total_answers)):
                tmp_function_dict = total_functions[function_index]
                tmp_answer = total_answers[function_index]
                tmp_contri += 1.0*total_weights[function_index]*(tmp_dfs[function_index].shape[0]-tmp_dfs[function_index][(tmp_dfs[function_index][column_id]>=tmp_function_dict[column_id][0]) & (tmp_dfs[function_index][column_id]<=tmp_function_dict[column_id][1])].shape[0] )/total_ranges[function_index]

            if tmp_contri>max_contri:
                max_contri = tmp_contri
                max_column = column_id
        solution.append(max_column)
        remaining_column_list.remove(max_column)
        for function_index in range(len(total_answers)):
            tmp_function_dict = total_functions[function_index]
            tmp_dfs[function_index]=tmp_dfs[function_index][(tmp_dfs[function_index][max_column]>=tmp_function_dict[max_column][0]) & (tmp_dfs[function_index][max_column]<=tmp_function_dict[max_column][1])]
    #print(solution)
    return solution

def normalized_greedy(agents_function_list,agents_function_weight_list,df,column_id_list):
    total_functions = []
    total_answers = []
    total_ranges = []
    total_weights = []
    num_rows = df.shape[0]
    #for functions_per_agent,answers_per_agent in agents_function_list:
    for agent_index in range(len(agents_function_list)):
        functions_per_agent,answers_per_agent = agents_function_list[agent_index]
        weights_per_agent = agents_function_weight_list[agent_index]
        total_weights += weights_per_agent
        total_functions += functions_per_agent
        total_answers += answers_per_agent
        for a in answers_per_agent:
            total_ranges.append(num_rows-a)

    tmp_dfs = [df[:] for _ in range(len(total_answers))]

    solution = []
    remaining_column_list = column_id_list
    #print(remaining_column_list)
    while len(remaining_column_list)>0:
        max_contri = 0
        max_column = remaining_column_list[0]
        for column_id in remaining_column_list:
            tmp_contri = 0
            for function_index in range(len(total_answers)):
                tmp_function_dict = total_functions[function_index]
                tmp_answer = total_answers[function_index]
                if tmp_dfs[function_index].shape[0] > tmp_answer:
                    tmp_contri += 1.0*total_weights[function_index]*(tmp_dfs[function_index].shape[0]-tmp_dfs[function_index][(tmp_dfs[function_index][column_id]>=tmp_function_dict[column_id][0]) & (tmp_dfs[function_index][column_id]<=tmp_function_dict[column_id][1])].shape[0] )/(tmp_dfs[function_index].shape[0]-tmp_answer)

            if tmp_contri>max_contri:
                max_contri = tmp_contri
                max_column = column_id
        solution.append(max_column)
        remaining_column_list.remove(max_column)
        for function_index in range(len(total_answers)):
            tmp_function_dict = total_functions[function_index]
            tmp_dfs[function_index]=tmp_dfs[function_index][(tmp_dfs[function_index][max_column]>=tmp_function_dict[max_column][0]) & (tmp_dfs[function_index][max_column]<=tmp_function_dict[max_column][1])]
    #print(solution)
    return solution


def our_algo_without_weight(agents_function_list,agents_function_weight_list,df,column_id_list,decrease_ratio=2.0/3):
    num_agents = len(agents_function_list)
    num_functions_per_agent = len(agents_function_list[0][0])
    baseline = num_functions_per_agent* decrease_ratio
    tmp_dfs = [[df[:] for _ in range(num_functions_per_agent)] for _ in range(num_agents)]
    solution = []
    remaining_column_list = column_id_list
    uncovered_agents = [i for i in range(num_agents)]
    while len(uncovered_agents)>0 and len(remaining_column_list)>0 :
        #print('len_uncovered = {}'.format(len(uncovered_agents)))
        #print(solution)
        while len(remaining_column_list)>0:
            unsatisfied_agents = []
            total_uncovered_function_indexes = {}
            for agent_id in uncovered_agents:
                uncovered_function_index_list = []
                for function_index in range(num_functions_per_agent):
                    if tmp_dfs[agent_id][function_index].shape[0] > agents_function_list[agent_id][1][function_index]:
                        uncovered_function_index_list.append(function_index)
                total_uncovered_function_indexes[agent_id]=uncovered_function_index_list
                if len(uncovered_function_index_list) > baseline:
                    unsatisfied_agents.append(agent_id)
            #print(len(unsatisfied_agents))
            if len(unsatisfied_agents) == 0:
                break

            max_contri = 0
            max_column = remaining_column_list[0]
            for column_id in remaining_column_list:
                tmp_contri = 0
                for agent_id in unsatisfied_agents:
                    for function_index in total_uncovered_function_indexes[agent_id]:
                        tmp_function_dict = agents_function_list[agent_id][0][function_index]
                        tmp_answer = agents_function_list[agent_id][1][function_index]
                        if tmp_dfs[agent_id][function_index].shape[0] > tmp_answer:
                            tmp_contri += 1.0*agents_function_weight_list[agent_id][function_index]*(tmp_dfs[agent_id][function_index].shape[0]-tmp_dfs[agent_id][function_index][(tmp_dfs[agent_id][function_index][column_id]>=tmp_function_dict[column_id][0]) & (tmp_dfs[agent_id][function_index][column_id]<=tmp_function_dict[column_id][1])].shape[0] )/(tmp_dfs[agent_id][function_index].shape[0]-tmp_answer)

                if tmp_contri > max_contri:
                    max_contri = tmp_contri
                    max_column = column_id
            solution.append(max_column)
            remaining_column_list.remove(max_column)

            removed_ids = []
            for agent_id in uncovered_agents:
                flag = 0
                for function_index in range(num_functions_per_agent):
                    tmp_function_dict = agents_function_list[agent_id][0][function_index]
                    tmp_dfs[agent_id][function_index]=tmp_dfs[agent_id][function_index][(tmp_dfs[agent_id][function_index][max_column]>=tmp_function_dict[max_column][0]) & (tmp_dfs[agent_id][function_index][max_column]<=tmp_function_dict[max_column][1])]
                    if tmp_dfs[agent_id][function_index].shape[0] > agents_function_list[agent_id][1][function_index]:
                        flag =1
                if flag == 0:
                    removed_ids.append(agent_id)
            for agent_id in removed_ids:
                    uncovered_agents.remove(agent_id)


        baseline = baseline * decrease_ratio

    #print(remaining_column_list)
    #print(solution+remaining_column_list)
    return solution+remaining_column_list


def our_algo_with_weight(agents_function_list,agents_function_weight_list,df,column_id_list,decrease_ratio=2.0/3):
    num_agents = len(agents_function_list)
    num_functions_per_agent = len(agents_function_list[0][0])
    sum_weights = [sum(x) for x in agents_function_weight_list]

    baseline = max(sum_weights)* decrease_ratio
    tmp_dfs = [[df[:] for _ in range(num_functions_per_agent)] for _ in range(num_agents)]
    solution = []
    remaining_column_list = column_id_list
    uncovered_agents = [i for i in range(num_agents)]
    while len(uncovered_agents)>0 and len(remaining_column_list)>0 :
        #print('len_uncovered = {}'.format(len(uncovered_agents)))
        #print(solution)
        while len(remaining_column_list)>0:
            unsatisfied_agents = []
            total_uncovered_function_indexes = {}
            for agent_id in uncovered_agents:
                uncovered_function_index_list = []
                for function_index in range(num_functions_per_agent):
                    if tmp_dfs[agent_id][function_index].shape[0] > agents_function_list[agent_id][1][function_index]:
                        uncovered_function_index_list.append(function_index)
                total_uncovered_function_indexes[agent_id]=uncovered_function_index_list
                #if len(uncovered_function_index_list) > baseline:
                if sum([agents_function_weight_list[agent_id][function_index] for function_index in uncovered_function_index_list]) > baseline:
                    unsatisfied_agents.append(agent_id)
            #print(len(unsatisfied_agents))
            if len(unsatisfied_agents) == 0:
                break

            max_contri = 0
            max_column = remaining_column_list[0]
            for column_id in remaining_column_list:
                tmp_contri = 0
                for agent_id in unsatisfied_agents:
                    for function_index in total_uncovered_function_indexes[agent_id]:
                        tmp_function_dict = agents_function_list[agent_id][0][function_index]
                        tmp_answer = agents_function_list[agent_id][1][function_index]
                        if tmp_dfs[agent_id][function_index].shape[0] > tmp_answer:
                            tmp_contri += 1.0*agents_function_weight_list[agent_id][function_index]*(tmp_dfs[agent_id][function_index].shape[0]-tmp_dfs[agent_id][function_index][(tmp_dfs[agent_id][function_index][column_id]>=tmp_function_dict[column_id][0]) & (tmp_dfs[agent_id][function_index][column_id]<=tmp_function_dict[column_id][1])].shape[0] )/(tmp_dfs[agent_id][function_index].shape[0]-tmp_answer)

                if tmp_contri > max_contri:
                    max_contri = tmp_contri
                    max_column = column_id
            solution.append(max_column)
            remaining_column_list.remove(max_column)

            removed_ids = []
            for agent_id in uncovered_agents:
                flag = 0
                for function_index in range(num_functions_per_agent):
                    tmp_function_dict = agents_function_list[agent_id][0][function_index]
                    tmp_dfs[agent_id][function_index]=tmp_dfs[agent_id][function_index][(tmp_dfs[agent_id][function_index][max_column]>=tmp_function_dict[max_column][0]) & (tmp_dfs[agent_id][function_index][max_column]<=tmp_function_dict[max_column][1])]
                    if tmp_dfs[agent_id][function_index].shape[0] > agents_function_list[agent_id][1][function_index]:
                        flag =1
                if flag == 0:
                    removed_ids.append(agent_id)
            for agent_id in removed_ids:
                uncovered_agents.remove(agent_id)


        baseline = baseline * decrease_ratio

    #print(remaining_column_list)
    #print(solution+remaining_column_list)
    return solution+remaining_column_list

