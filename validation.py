from batches import *
import torch.cuda
import eval_metrics
import math

def validation(model, num_users, test_positive, val_positive, train_matrix,k_list, nearPOI):
    model.eval() 
    batch_size =1024 
    recommended_list = []
    for user_id in range(num_users):
        user_history, target_list, _ = test_batch(train_matrix,user_id)
        n = math.ceil(len(target_list)/batch_size)
        temp = user_history.repeat(batch_size,1)
        temp_n = user_history.repeat(len(target_list[batch_size*(n-1):]),1)
        for i in range(n):
            if(i == n-1):
                pred = torch.cat((pred,model(temp_n,target_list[batch_size*i:],nearPOI)),dim=-1)
            elif i == 0:
                pred = model(temp,target_list[batch_size*i:batch_size*(i+1)],nearPOI)
            else:
                pred = torch.cat((pred,model(temp,target_list[batch_size*i:batch_size*(i+1)],nearPOI)),dim=-1)
    
        _, indices = torch.topk(pred, 50)
        recommended_list.append([target_list[i].item() for i in indices])
    # torch.cuda.empty_cache()
    precision_v, recall_v, hit_v = eval_metrics.evaluate_mp(val_positive,recommended_list,k_list)
    precision_t, recall_t, hit_t = eval_metrics.evaluate_mp(test_positive,recommended_list,k_list)
    return precision_v, recall_v, hit_v, precision_t, recall_t, hit_t
