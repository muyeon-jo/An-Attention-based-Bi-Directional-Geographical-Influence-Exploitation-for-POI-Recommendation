def save_experiment_result(directory, results,k_list,epoch):
    f=open(directory+"/results.txt","w")
    recall = results[0]
    precision = results[1]
    hitrate = results[2]

    f.write("epoch:{}\n".format(epoch))
    for i in range(len(k_list)):
        f.write(str(k_list[i])+"\t")
    f.write("\n")
    for i in range(len(recall)):
        f.write(str(recall[i])+"\t")
    f.write("\n")
    for i in range(len(precision)):
        f.write(str(precision[i])+"\t")
    f.write("\n")
    for i in range(len(hitrate)):
        f.write(str(hitrate[i])+"\t")
    f.write("\n")
    f.close()
