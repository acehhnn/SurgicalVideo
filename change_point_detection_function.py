import os
import ruptures as rpt
import numpy as np
from sklearn.model_selection import train_test_split

# Detect change point
# parameter
## dirct: pbp seq directory
## outpath: change point seq directory
## list_n: file names of pbp sequences
## label: positive or negative
## K_list: list of values of parameter K
# output: .npy files of change point sequences

def ChangePoint (dirct, outpath, list_n, label, K_list):
    for K in K_list:
        outpath = os.path.join(outpath, label + str(K),"result")
        
        for i in range(len(list_n)):
            s = os.path.join(dirct, list_n[i])
            signal = np.load(s)
            print(len(signal))
            algo = rpt.Pelt(model="rbf").fit(signal)
            result = algo.predict(pen = K)
            print(np.array(result))
            outK = os.path.join(outpath, str(list_n[i])+'.npy')
            np.save(outK, result, allow_pickle = True, fix_imports = True)

##############################
# Verify candidates
def test(threshold,K,index_n,index_p,path1,path2,out1,out2,note,TopK):
    # -------------------------改
    # out1 = os.path.join('F:\\result\\chosen\\negative_'+str(K),'result')
    # 无出血的视频
    # out1 = os.path.join("E:\\fake_blood\\sample\\fake_data\\result\\negative_"+str(K),"result")
    index_increase = [] # 有candidate的视频编号
    index_no = [] # 无candidate的视频编号
    # increase = []
    for i in range(len(index_n)):
        f = index_n[i]
        s = os.path.join(path1, str(f)+'.npy')
        signal = np.load(s)
        
        p2 = os.path.join(out1, str(f)+'.npy')
        result = np.load(p2)
        
        result2 = []
        # number of changepoints
        for j in range(len(result)):
            if j==0:
                data = signal[0:result[j]]
                result2.append(np.mean(data)) 
            else:
                data = signal[result[j-1]:result[j]]
                result2.append(np.mean(data)) 
               
        # 判断有无变点是candidate
        t = 0
        for j in range(len(result2)):
            if j>0:
                if result2[j]-result2[j-1] >= threshold:
                    t = t + 1
                    # increase.append(result2[j]-result2[j-1])
    
        if t>0:
            index_increase.append(f)
        else:
            index_no.append(f)   
    
    print("K=",K,"threshold=",threshold,"index_no=",index_no)
    print("index_increase=",index_increase)
    TN = len(index_no)
    FP = len(index_increase)
    # if len(increase)>0:
    #     max_increase = max(increase)
    # else:
    #     max_increase = np.nan

    # 有出血的视频  
    # out2 = os.path.join("E:\\fake_blood\\sample\\fake_data\\result\\positive_"+str(K),"result")
    
    # 假设只用前TopK个candidate
    increase_point = []
    # min_increase = []
    wrong_pos = []
    right_can = 0 # 总的正确candidate数
    wrong_can = 0 # 总的错误candidate数
    TP = 0 # TP: 有至少一个在容忍范围内candidate的出血视频
    TP1 = 0 # TP1: 有candidate的出血视频
    FN = 0 # FN: 没有在容忍范围内candidate的出血视频
    FN1 = 0 # FN1: 没有candidate的出血视频
    for i in range(len(index_p)):
        f = index_p[i]
        
        s = os.path.join(path2, str(f)+'.npy')
        signal = np.load(s)
        
        p2 = os.path.join(out2, str(f)+'.npy')
        result = np.load(p2)
            
        result2 = []
        # number of changepoints
        for j in range(len(result)):
            if j==0:
                data = signal[0:result[j]]
                result2.append(np.mean(data)) 
            else:
                data = signal[result[j-1]:result[j]]
                result2.append(np.mean(data)) 
        # pbp 最大增量的最小值
        # dif0 = []
        # for j in range(len(result2)):
        #     if j>0:
        #         dif0.append(result2[j]-result2[j-1])
        # min_increase.append(max(dif0))
        
        t = 0
        increase = [] # candidate的位置
        # in_diff = []
        for j in range(len(result2)):
            if j>0:
                if result2[j]-result2[j-1] >= threshold:
                    # in_diff.append(result2[j]-result2[j-1])
                    t = t + 1
                    increase.append(result[j-1])
        # path_out = os.path.join('C:\\Users\\abc\\Desktop\\test',str(f)+'.txt')
        # np.savetxt(path_out,in_diff,fmt='%.18e')

        # in_diff = np.array(in_diff)
        # seq = np.argsort(-in_diff) # pbp增量从大到小排的序号
        # increase = np.array(increase)[seq[0:TopK]] # 只用前TopK个candidate
        
        # 只看前两个candidate
        increase = increase[0:TopK-1]
        # increase: candidate 
        # Candidates that within note[i]+-50 is correct
        if len(increase)>0:
            TP1 = TP1 + 1 
            increase = np.array(increase)
            dif = increase-note[i]
            dif = np.abs(dif)
            count1 = 0  # 该视频中正确的candidate数
            for count in range(len(dif)):
                if dif[count] <= 50:
                    right_can = right_can + 1
                    count1 = count1 + 1
                    print("Recognized:",f, note[i], increase[count])
                elif dif[count] > 50:
                    wrong_can = wrong_can + 1 
                    print("Unrecognized:",f, note[i], increase[count])
            if count1 > 0: # 至少一个candidate在note周围，保存距离最小的为increase_point
                TP = TP + 1 
                dif = list(dif)
                pos = dif.index(min(dif))
                increase_point.append(increase[pos]) # 误差最小的那个candidate
            else: # 没有candidate在note周围
                increase_point.append(np.nan)
                FN = FN + 1 
                wrong_pos.append(f)
        else: # 没有candidate
            FN1 = FN1 + 1 
            FN = FN + 1 
            increase_point.append(np.nan)
            wrong_pos.append(f)
    
    # increase_point 是note周围一定范围内的、且距离最小的candidate
    # candidate 是正确的出血事件
    # na: 非nan的increase_point的编号
    na = np.array(1-np.isnan(increase_point),dtype='bool')
    print("na=",na) # test
    increase_point = np.array(increase_point)
    # print("increase_point=",increase_point)
    increase_point = increase_point[na] # 离note足够近且距离最小的candidate的编号
    print("increase_point=",increase_point)
    
    CTP = right_can # 此candidate距离note足够近，是出血，真阳性
    CFP = wrong_can # candidate离note很远，非出血，假阳性，误报
    
    note = note[na]
    dif = np.array(increase_point)-np.array(note)
    err = np.mean(np.abs(dif))
    err_max = max(np.abs(dif))
    # min_increase = min(min_increase)
    recall = TP1/(TP1+FN1)
    specificity = TN/(TN+FP)
    missing_report = FN/len(index_p)
    error_report = CFP/(CFP + CTP)
    
    result = dict()
    result['K']=K
    result['threshold']=threshold
    result['TN']=TN
    result['FP']=FP
    result['TP1']=TP1
    result['FN1']=FN1
    result['TP']=TP
    result['FN']=FN
    result['CTP']=CTP
    result['CFP']=CFP
    # result['neg_max_increase']=max_increase
    # result['pos_min_increase']=min_increase
    result['error']=err
    result['err_max']=err_max
    result['dif']=dif
    result['recall']=recall # sensitivity
    result['specificity']=specificity
    result['index_increase']=index_increase
    result['wrong_pos']=wrong_pos
    result['missing_report']=missing_report
    result['error_report']=error_report
    result['recog'] = increase_point
    return(result)

##################################
# Compute accuracy
def CompuRes (K_list, threshold_list, dirct_n, dirct_p, dirctout_n, dirctouot_p, txtdirct, id_p, note, id_n, test_size=0.3, random_state=1):
    id_p_train, id_p_test, note_train, note_test = train_test_split(id_p, note, test_size=test_size, random_state=random_state)
    id_n_train, id_n_test = train_test_split(id_n, test_size=test_size, random_state=random_state)
    TopK = 2

    # training data
    sensitivity_train = []
    specificity_train = []
    missing_report_train = []
    error_report_train = []
    for K in K_list:
        for threshold in threshold_list:
            result1 = test(threshold=threshold, K=K, index_n=id_n_train, index_p=id_p_train, 
                           path1=dirct_n, path2=dirct_p, out1=dirctout_n, out2=dirctouot_p,
                            note=note_train, TopK=TopK) 
            error_report_train.append(result1['error_report'])
            missing_report_train.append(result1['missing_report'])
            specificity_train.append(result1['specificity'])
            sensitivity_train.append(result1['recall'])

    txtpath = os.path.join(txtdirct, 'train\\error_report.txt')
    np.savetxt(txtpath,error_report_train,fmt='%.4f')
    txtpath = os.path.join(txtdirct, 'train\\missing report.txt')
    np.savetxt(txtpath,missing_report_train,fmt='%.4f')  
    txtpath = os.path.join(txtdirct, 'train\\sensitivity.txt')
    np.savetxt(txtpath,sensitivity_train,fmt='%.4f')  
    txtpath = os.path.join(txtdirct, 'train\\specificity.txt')
    np.savetxt(txtpath,specificity_train,fmt='%.4f') 

    # test data
    sensitivity_test = []
    specificity_test = []
    missing_report_test = []
    error_report_test = []
    for K in K_list:
        for threshold in threshold_list:
            result1 = test(threshold=threshold, K=K, index_n=id_n_test, index_p=id_p_test, 
                           path1=dirct_n, path2=dirct_p, out1=dirctout_n, out2=dirctouot_p,
                            note=note_test, TopK=TopK) 
            error_report_test.append(result1['error_report'])
            missing_report_test.append(result1['missing_report'])
            specificity_test.append(result1['specificity'])
            sensitivity_test.append(result1['recall'])

    txtpath = os.path.join(txtdirct, 'test\\error_report.txt')
    np.savetxt(txtpath,error_report_test,fmt='%.4f')
    txtpath = os.path.join(txtdirct, 'test\\missing report.txt')
    np.savetxt(txtpath,missing_report_test,fmt='%.4f')  
    txtpath = os.path.join(txtdirct, 'test\\sensitivity.txt')
    np.savetxt(txtpath,sensitivity_test,fmt='%.4f')  
    txtpath = os.path.join(txtdirct, 'test\\specificity.txt')
    np.savetxt(txtpath,specificity_test,fmt='%.4f') 

    # total
    sensitivity = []
    specificity = []
    missing_report = []
    error_report = []
    for K in K_list:
        for threshold in threshold_list:
            result1 = test(threshold=threshold, K=K, index_n=id_n, index_p=id_p, 
                           path1=dirct_n, path2=dirct_p, out1=dirctout_n, out2=dirctouot_p,
                            note=note, TopK=TopK) 
            error_report_test.append(result1['error_report'])
            missing_report_test.append(result1['missing_report'])
            specificity_test.append(result1['specificity'])
            sensitivity_test.append(result1['recall'])

    txtpath = os.path.join(txtdirct, 'total\\error_report.txt')
    np.savetxt(txtpath,error_report,fmt='%.4f')
    txtpath = os.path.join(txtdirct, 'total\\missing report.txt')
    np.savetxt(txtpath,missing_report,fmt='%.4f')  
    txtpath = os.path.join(txtdirct, 'total\\sensitivity.txt')
    np.savetxt(txtpath,sensitivity,fmt='%.4f')  
    txtpath = os.path.join(txtdirct, 'total\\specificity.txt')
    np.savetxt(txtpath,specificity,fmt='%.4f') 
