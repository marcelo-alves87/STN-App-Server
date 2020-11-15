# -*- coding: utf-8 -*-
"""
Criado Terça-feira, 13 de Outubro de 2020

@author: DCPB
"""

# Protótipo RNA Detecção - Campo Experimental UFPE
# Treinada com Base de Dados de 350 amostras disponível em 12/01/20 - Relatório 27
# Author: Douglas Contente Pimentel Barbosa - Out/2020


#------------------------------------------------------------------------------
# Programa para uso da Feedforward Artificial Neural Network - FF-ANN
# na detecção de falhas nas hastes de âncora de 06m com RNA pre Treinada.
#------------------------------------------------------------------------------

def CarregaRNA_Testa_Ancora(arquivo, stats = '/home/pi/Documents/STN_Server/python/Means_Variances.xls', classificador = '/home/pi/Documents/STN_Server/python/classifier.json', pesos = '/home/pi/Documents/STN_Server/python/model_weights.h5'):
    '''
    ### Função para classificação de hastes do Campo Experimental UFPE ###
    
    Entrada: Arquivo Excel (.xlsx) contendo os 1001 pontos do Mod S11 nas células A2-ALM2 em diante
    Saída: array numpy contendo 0 (zeros) para hastes normais e 1 (uns) para hastes defeituosas, ordenadamente
        
    IMPORTANTE: A Função necessita dos seguintes arquivos auxiliares:
    'Means_Variances.xls'; 'classifier.json', 'model_weights.h5'

    '''
    import pandas as pd
    import numpy as np
    from keras.models import load_model
#    from sklearn.metrics import confusion_matrix, precision_score, recall_score, accuracy_score, f1_score
    
    def scale_data(array,means,stds):
        return (array-means)/stds
        
    #Variável de Saída
    Status = []
    # Importando base de dados
    dataset = pd.read_excel(arquivo)
    ModS11 = dataset.iloc[:,:15].values
#    FasS11 = dataset.iloc[:,1001:2002].values
#    ReZin = dataset.iloc[:,2002:3003].values
#    ImZin = dataset.iloc[:,3003:4004].values
#    VSWR = dataset.iloc[:,4004:5005].values    
    
    #Selecionando o parâmetro
    X_detect = ModS11
    y_true = dataset.iloc[:, 5006].values

    #Carregando Estatísticas
    estatisticas = pd.read_excel(stats)
    estatisticas = estatisticas.T

    meansTreino = estatisticas.iloc[0,:1001].values
#    print(meansTreino)
    variancesTreino = estatisticas.iloc[1,:1001].values

    #Normalizando entradas
    X_detect_norm = (X_detect-meansTreino)/variancesTreino**0.5

    # load json and create model
    loaded_model = load_model('/home/pi/Documents/STN_Server/python/loaded_model.workshop')
    
    #loaded_model
  
    # Fazendo a classificação dos dados de entrada
    y_detect = loaded_model.predict(X_detect_norm)
    y_detect = (y_detect > 0.5)
    y_detect = np.int64(y_detect)
    y_detect = y_detect.reshape((-1,))
    
   
#    #Associando o Status
#    for i in range(len(y_detect)):
#        if y_detect[i] == 0:
#            Status.append(('Status haste número %s: Normal' %(i+1)))
#        else:
#            Status.append(('Status haste número %s: Defeituosa' %(i+1)))
#    
#    #imprimindo o resultado
#    for i in range(len(Status)):
#        print("\n" + str(Status[i]))
#        
#    #calculando os parâmetros
#    cm = confusion_matrix(y_true, y_detect)
#    print("")
#    print("Accuracy = " + str(round(100*accuracy_score(y_true, y_detect),2))+"%")
#    print("F1Score = " + str(round(100*f1_score(y_true, y_detect),2))+"%")
#    print("Precision = " + str(round(100*precision_score(y_true, y_detect),2))+"%")
#    print("Recall = " + str(round(100*recall_score(y_true, y_detect),2))+"%")
#    print("")
#    print(cm)
    
    #retornando o resultado   
    return(y_detect)
    

    
print(CarregaRNA_Testa_Ancora('/home/pi/Documents/STN_Server/python/Pi.xlsx')) 
