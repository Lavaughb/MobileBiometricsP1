import numpy as np
import math
import matplotlib.pyplot as plt

############ functions #############################################################

def dprime(gen_scores, imp_scores):
    spread_G = max(gen_scores)-min(gen_scores)
    spread_I = max(imp_scores)-min(imp_scores)
    x = np.sqrt(2)*abs(np.mean(gen_scores)-np.mean(imp_scores)) # replace 1 with the numerator
    y = np.sqrt(math.pow(spread_G, 2) + math.pow(spread_I, 2)) # replace 1 with the denominator
    return x / y

def plot_scoreDist(gen_scores, imp_scores, plot_title):
    plt.figure()
    plt.hist(gen_scores, color='green', lw=2, histtype='step', hatch='//', label='Genuine Scores')
    plt.hist(imp_scores, color='red', lw=2, histtype='step', hatch='\\', label='Impostor Scores')
    plt.xlim([-0.05,1.05])    
    plt.legend(loc='best')
    dp = dprime(gen_scores, imp_scores)    
    plt.title(plot_title + '\nD-prime= %.2f' % dp)
    plt.show()
    return

def get_EER(far, frr):
    eer = 0
    errorRate = []
    for x in range(len(far)):
        errorRate.append(abs(far[x]-frr[x]))
    
    min_value = min(errorRate)
    min_index = errorRate.index(min_value)
    eer = (far[min_index] +frr[min_index])/2
    return eer

def plot_det(far, frr, plot_title):
    eer = get_EER(far, frr)
    plt.figure()
    plt.plot(far, frr, lw=2)
    plt.plot([0,1], [0,1], lw=1, color='black')    
    plt.xlim([-0.05,1.05])
    plt.ylim([-0.05,1.05]) 
    plt.xlabel('FAR')    
    plt.ylabel('FRR')    
    plt.title(plot_title + '\nEER = %.3f' % eer)
    plt.show()
    return

def plot_roc(far, tpr, plot_title):
    plt.figure()
    plt.plot(far, tpr, lw=2)    
    plt.xlim([-0.05,1.05])    
    plt.ylim([-0.05,1.05])    
    plt.xlabel('FAR')    
    plt.ylabel('TAR')    
    plt.title(plot_title)
    plt.show()
    return

# Function to compute TPR, FAR, FRR
def compute_rates(gen_scores, imp_scores, num_thresholds):
    thresholds = np.linspace(0.00,1.00,num = num_thresholds) # use np.linspace to create n threshold values 
                 # between 0 and 1

    
    far = []
    frr = []
    tpr = []
    
    for t in thresholds:
        TP=0
        FP=0
        TN=0
        FN=0
        
        for g_s in gen_scores:
            if g_s >= t:
                TP += 1 
            else:
                FN += 1
                
        for i_s in imp_scores:
            if i_s >= t:
                FP+=1 
            else: 
                TN+=1 
                    
        far.append(FP/(FP+TN))
        frr.append(FN/(FN+TP))
        tpr.append(TP/(TP+FN))
        
    
    return far, frr, tpr

############ main code #############################################################

# Set the seed using np.random.seed
np.random.seed(1)
G_mu_A, G_sigma_A = 0.8100, 0.0100
I_mu_A, I_sigma_A = 0.6900, 0.0420
G_mu_B, G_sigma_B = 0.8100, 0.0100
I_mu_B, I_sigma_B = 0.4780, 0.0014
G_mu_C, G_sigma_C = 0.8100, 0.0100
I_mu_C, I_sigma_C = 0.4120, 0.1550


gen_means = [G_mu_A, G_mu_B, G_mu_C] # fill these in
gen_stds = [G_sigma_A,G_sigma_B, G_sigma_C] # fill these in
imp_means = [I_mu_A, I_mu_B, I_mu_C] # fill these in 
imp_stds = [I_sigma_A, I_sigma_B, I_sigma_C] # fill these in


titles = ['System A', 'System B', 'System C']
for i in range(len(gen_means)):
    gen_scores = np.random.normal(gen_means[i], gen_stds[i], 400) # use np.random.normal()
    imp_scores = np.random.normal(imp_means[i], imp_stds[i], 1600) # use np.random.normal()
    far, frr, tpr = compute_rates(gen_scores, imp_scores, 500)    
    plot_title = titles[i]
    plot_scoreDist(gen_scores, imp_scores, plot_title)
    plot_roc(far, tpr, plot_title)
    plot_det(far, frr, plot_title)