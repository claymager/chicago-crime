import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support
import seaborn as sns
import matplotlib.pyplot as plt

class ModelTest:
    def __init__(self, model, X_train, X_test, y_train,
                 y_test, id_ = 0,logfile="model_results"):
        """
        Tests a classification model against data, records the results.
        """
        model.fit(X_train, np.ravel(y_train))
        train_preds = model.predict(X_train)
        y_pred = model.predict(X_test)
        p,r,f,_ = precision_recall_fscore_support(y_test, y_pred)
        self.id = str(id_)
        self.description = str(model)
        self.train_acc = accuracy_score(y_train, train_preds)
        self.accuracy = accuracy_score(y_test, y_pred)
        self.precision = p.mean()
        self.recall = r.mean()
        self.f1_score = f.mean() 
        self.conf_mat = confusion_matrix(y_test, y_pred)
        self.logfile = "log/"+logfile
        
        
    def __str__(self):
        return """
################################################################
MODEL {}:
{}
test/train accuracy: {}
accuracy: {}
mean precision: {}
mean recall: {}
mean fscore: {}
""".format(self.id,
        self.description,
        self.accuracy/self.train_acc,
        self.accuracy,
        self.precision,
        self.recall,
        self.f1_score)
    
    def _to_csv(self):
        return "{},{},{},{},{},{}\n".format(
                    self.id, 
                    self.accuracy,
                    self.accuracy/self.train_acc,
                    self.precision,
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
            plt.savefig("plots/"+self.logfile+self.id+".png")
