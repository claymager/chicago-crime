import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support
import seaborn as sns
import matplotlib.pyplot as plt

class ModelTest:
    def __init__(self, model, X_train, X_test, y_train,
                 y_test, id_ = 0,logfile="model_results"):
        model.fit(X_train, np.ravel(y_train))
        y_pred = model.predict(X_test)
        p,r,f,_ = precision_recall_fscore_support(y_test, y_pred)
        self.precision = p.mean()
        self.recall = r.mean()
        self.f1_score = f.mean() 
        self.accuracy = accuracy_score(y_test, y_pred)
        self.model_str = str(model)
        self.conf_mat = confusion_matrix(y_test, y_pred)
        self.id = str(id_)
        self.logfile = logfile
        
        
    def __str__(self):
        return """
################################################################
MODEL {}:
{}
accuracy: {}
mean precision: {}
mean recall: {}
mean fscore: {}
""".format(self.id, self.model_str, self.accuracy,
                   self.precision, self.recall, self.f1_score)
    
    def _to_csv(self):
        return "{},{},{},{},{}\n".format(self.id, 
                       self.accuracy, self.precision,
                       self.recall, self.f1_score)
    
    def log(self, txt = True, csv = True, png = True):
        if txt:
            f = open(self.logfile+".txt", "a+")
            f.write( str(self) )
            f.close()
        if csv:
            f = open(self.logfile+".csv", "a+")
            f.write( self._to_csv() )
            f.close()
        if png:
            plt.figure(dpi=350)
            sns.heatmap(self.conf_mat)
            plt.savefig("plots/"+self.id+".png")
