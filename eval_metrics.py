import multiprocessing as mp
def evaluate_mp(positive_list, recommended_list, k_list):
    input_list = []
    for i in range(len(k_list)):
        input_list.append((positive_list,recommended_list,k_list[i]))
    pool = mp.Pool(processes=len(k_list))
    recall = pool.starmap(recall_at_k, input_list)
    pool.close()
    pool.join()
    print("recall: ", recall)

    pool = mp.Pool(processes=len(k_list))
    precision = pool.starmap(precision_at_k, input_list)
    pool.close()
    pool.join()
    print("prec: ",precision)

    pool = mp.Pool(processes=len(k_list))
    hit = pool.starmap(hitrate_at_k, input_list)
    pool.close()
    pool.join()
    print("hit: ", hit)
    print("--------")
    return precision,recall,hit

def precision_at_k(actual, predicted, topk):
    sum_precision = 0.0
    num_users = len(predicted)
    for i in range(num_users):
        act_set = set(actual[i])
        pred_set = set(predicted[i][:topk])
        sum_precision += len(act_set & pred_set) / float(topk)

    return sum_precision / num_users

def recall_at_k(actual, predicted, topk):
    sum_recall = 0.0
    num_users = len(predicted)
    true_users = 0
    for i in range(num_users):
        act_set = set(actual[i])
        pred_set = set(predicted[i][:topk])
        if len(act_set) != 0:
            sum_recall += len(act_set & pred_set) / float(len(act_set))
            true_users += 1
    return sum_recall / true_users

def hitrate_at_k(actual, predicted, topk):
    sum_hit = 0.0
    num_users = len(predicted)
    true_users = 0
    for i in range(num_users):
        act_set = set(actual[i])
        pred_set = set(predicted[i][:topk])
        if len(act_set) != 0:
            if len(act_set & pred_set) > 0:
                sum_hit += 1
            true_users += 1
    return sum_hit / true_users