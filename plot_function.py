import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator


def PlotSeq (K, threshold, dirct, ids, outdirct, note, plot_path, flag):
    outpath = os.path.join(outdirct + '_' + str(K))

    for i in range(len(ids)):
        s = os.path.join(dirct, str(ids[i]) + '.npy')
        signal = np.load(s)

        p2 = os.path.join(outpath, str(ids[i])+'.npy')
        result = np.load(p2)

        result2 = []
        for j in range(len(result)):
                if j==0:
                    data = signal[0:result[j]]
                    result2.append(np.mean(data)) 
                else:
                    data = signal[result[j-1]:result[j]]
                    result2.append(np.mean(data)) 

        # 判断有无变点是candidate
        t = 0
        event = []
        for j in range(len(result2)):
            if j>0:
                if result2[j]-result2[j-1] >= threshold:
                    t = t + 1
                    event.append(result[j-1])

        fig = plt.figure(figsize=(20, 3), dpi=400)
        plt.xlabel("Frame",fontsize=25)
        plt.ylabel("PBP",fontsize=25)
        plt.title("Positive_"+str(id[i]),fontsize=25)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        y_major_locator=MultipleLocator(0.2)
        plt.plot(signal,linewidth=3)
        ax=plt.gca()
        ax.yaxis.set_major_locator(y_major_locator)
        plt.xlim(0,len(signal))
        plt.ylim(0,1)

        # 垂直填充
        col = (['#d9e6fc','#fcd9e3'])
        sgn = -1
        plt.axvspan(0, result[0], facecolor=col[0], alpha=1)
        for j in range(len(result)-1):
            sgn = -sgn
            idx = int(sgn/2 + 0.5)
            plt.axvspan(result[j], result[j+1], facecolor=col[idx], alpha=1)
        if flag=='positive':
            l = note[i]
            plt.axvline(l,color='red')
        if len(event)>0:
            for j in range(len(event)):
                plt.axvline(event[j],color='blue',linestyle='--')
        
        p1 = os.path.join(plot_path, flag + '_' + str(id[i])+'.png')
        plt.savefig(p1,dpi=400)
        plt.show()
