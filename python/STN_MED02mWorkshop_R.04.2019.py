# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 11:13:48 2019

@author: dougl
"""

# Protótipo RNA Haste de Âncora Campo Experimental UFPE - Revisão 01
#Treinamento e Detecção
# Haste de Âncora de 06m
# Author: Douglas Contente Pimentel Barbosa - Fev/2019

#------------------------------------------------------------------------------    
#Programa para Treinamento da RNA com a base de dados de 144 medições
#------------------------------------------------------------------------------
"""
Programa para treinamento da RNA. Utiliza a Base de Dados com 100 Amostras
medidas das haste de 02m e retorna o gráfico da função perda relativa ao treinamento
e um indicativo da taxa de erro obtida, sugerindo um novo treinamento quando 
um mínimo local sub-ótimo é encontrado.
"""
# Importando bibliotecas
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importando base de dados
dataset = pd.read_csv(os.path.dirname(os.path.abspath(__file__)))
ModS11 = dataset.iloc[:,:1001].values
FasS11 = dataset.iloc[:,1001:2002].values
ReZin = dataset.iloc[:,2002:3003].values
ImZin = dataset.iloc[:,3003:4004].values
VSWR = dataset.iloc[:,4004:5005].values

y = dataset.iloc[:, 5005].values

#Definindo parâmetro a ser analisado
X = ModS11

#Criando RNA
from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model

# =============================================================================
# # Iniciando RNA
# classifier = Sequential()
# # Hidden Layer #1
# classifier.add(Dense(output_dim = 14, init = 'uniform', activation = 'relu', input_dim = 1001))
# # Neurônios de Saída
# classifier.add(Dense(output_dim = 1, init = 'uniform', activation = 'sigmoid'))
# # Compilando RNA
# classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
# # Aplicando os dados de treino a RNA
# RNA = classifier.fit(X_train, y_train, batch_size = 10, nb_epoch = 100)
# 
# classifier.save("classifier_Haste2m_MDSC.h5")
# =============================================================================

classifier = load_model('classifier_Haste2m_MDSC.h5')

# Fazendo previsões dos dados de Teste
y_pred = classifier.predict(X_test)
y_pred = (y_pred > 0.5)
y_pred = np.int64(y_pred)
y_pred = y_pred.reshape((-1,))
    
# Calculando Desempenho
from sklearn.metrics import confusion_matrix
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import accuracy_score
cm = confusion_matrix(y_test, y_pred)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1score = (2*precision*recall)/(precision + recall)
    
#Plotando o treino
Fig1 = plt.figure(1)
plt.plot(RNA.history['loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.show()

if f1score < 0.95:
    print('\nATENÇÃO: Um mínimo local sub-ótimo foi encontrado! Considerar repetição do Treinamento.')
else:
    print('\nA RNA está treinada e pronta para classificar novas amostras com a função "Testa_Ancora()".')

#------------------------------------------------------------------------------
# Programa para uso da Feedforward Artificial Neural Network - FF-ANN
# na detecção de falhas nas hastes de âncora de 06m.
#------------------------------------------------------------------------------
def Converte_Arquivo(arquivo): 

    data = pd.read_csv(arquivo, sep="delimited", header=None)

    mod = []
    fase = []
    vswr = []
    imp = []
    
    #copia valores do módulo de S11 para mod[]
    for aux1 in range(len(data)):
        if (data[0][aux1]=="BEGIN"):
            aux2 = aux1 + 1
            while(data[0][aux2]!="END"):
                mod.append(data[0][aux2])
                aux2 = aux2 + 1
            break

    #deleta linhas com valores do módulo de S11
    for aux3 in range(len(data)):
        while (data[0][aux3]!="! CORRECTION2 ON U"):
            data = data.drop([aux3],axis=0)
            aux3 = aux3 + 1
        break

    #copia valores da fase de S11 para fase[]
    for aux4 in range(aux3,len(data)+aux3):
        if (data[0][aux4]=="BEGIN"):
            aux5 = aux4 + 1
            while(data[0][aux5]!="END"):
                fase.append(data[0][aux5])
                aux5 = aux5 + 1
            break

    #deleta linhas com valores da fase de S11
    for aux6 in range(aux3,len(data)):
        while (data[0][aux6]!="! CORRECTION3 ON U"):
            data = data.drop([aux6],axis=0)
            aux6 = aux6 + 1
        break

    #copia valores do vswr para vswr[]
    for aux7 in range(aux6,len(data)+aux6):
        if (data[0][aux7]=="BEGIN"):
            aux8 = aux7 + 1
            while(data[0][aux8]!="END"):
                vswr.append(data[0][aux8])
                aux8 = aux8 + 1
            break

    #deleta linhas com valores do vswr
    for aux9 in range(aux6,len(data)+aux6):
        while (data[0][aux9]!="! CORRECTION4 ON U"):
            data = data.drop([aux9],axis=0)
            aux9 = aux9 + 1
        break

    #copia valores da impedancia de entrada para imp[]
    for aux10 in range(aux9,len(data)+aux9):
        if (data[0][aux10]=="BEGIN"):
            aux11 = aux10 + 1
            while(data[0][aux11]!="END"):
                imp.append(data[0][aux11])
                aux11 = aux11 + 1
            break
        
        #deleta lista dos dados e os auxiliares
    del [arquivo, data, aux1, aux2, aux3, aux4, 
         aux5, aux6, aux7, aux8, aux9, aux10, aux11]

    #converte cada matriz em string para poder separar com as vírgulas
    modstr = ''.join(mod)
    modsplit = modstr.split(",")
    fasestr = ''.join(fase)
    fasesplit = fasestr.split(",")
    vswrstr = ''.join(vswr)
    vswrsplit = vswrstr.split(",")
    impstr = ''.join(imp)
    impsplit = impstr.split(",")
    
    del [modsplit[0], fasesplit[0],
         vswrsplit[0], impsplit[0],
         modstr, fasestr, vswrstr, impstr]

    #transforma todas as strings criadas em matriz
    mod = np.asarray(modsplit)
    fase = np.asarray(fasesplit)
    vswr = np.asarray(vswrsplit)
    imp = np.asarray(impsplit)
    
    del [modsplit, fasesplit,
         vswrsplit, impsplit]
    
    #transpõe matrizes
    mod = pd.DataFrame(data=mod)
    mod = mod.T
    fase = pd.DataFrame(data=fase)
    fase = fase.T
    vswr = pd.DataFrame(data=vswr)
    vswr = vswr.T
    imp = pd.DataFrame(data=imp)
    imp = imp.T
    
    #concatena
    dados=np.concatenate((mod,fase,vswr,imp),axis=1,out=None).astype(None)
    
    del [mod, fase, vswr, imp]
    
    #converte para DataFrame
    dados=pd.DataFrame(data=dados, index=None, columns=None, dtype=None, copy=False)
    
    return(dados)

def Testa_Ancora(arquivo):
    """
    Esta função recebe um arquivo excel com parâmetros de medição de hastes de âncora
    formatados conforme arquivo "BD - MedExpUFPE - 02Classes - HA6m.xlsx" e retorna 
    uma lista de strings contendo a classificação de cada uma das amostras contidas
    no arquivo de entrada.
    Importante: A RNA deve ser ter sido treinada anteriormente conforme programa principal.
    Entrada: Arquivo excel com os parâmetros medidos em campo para hastes de âncora de 6m.
    Saída: Lista com a classificação das medições de cada uma das linhas do arquivo Excel.
    """
    #Variável de Saída
    Status = []
    # Importando base de dados
#    dataset = pd.read_excel(arquivo)
    dataset = Converte_Arquivo(arquivo)
    ModS11 = dataset.iloc[:,:1001].values
    FasS11 = dataset.iloc[:,1001:2002].values
    ReZin = dataset.iloc[:,2002:3003].values
    ImZin = dataset.iloc[:,3003:4004].values
    VSWR = dataset.iloc[:,4004:5005].values
    
#    y = dataset.iloc[:, 5005].values
    
    #Selecionando o parâmetro
    X_detect = ModS11

    # Normalizando entradas
    X_detect = sc.transform(X_detect)
  
    # Fazendo a classificação dos dados de entrada
    y_detect = classifier.predict(X_detect)
    y_detect = (y_detect > 0.5)
    y_detect = np.int64(y_detect)
    y_detect = y_detect.reshape((-1,))
    
    #Associando o Status
    for i in range(len(y_detect)):
        if y_detect[i] == 0:
            Status.append(('Status haste de número %s: Defeituosa' %(i+1)))
        else:
            Status.append(('Status haste de número %s: Normal' %(i+1)))
    
    #imprimindo o resultado
    for i in range(len(Status)):
        print("\n" + str(Status[i]))
        
    #retornando o resultado   
#    return(Status)