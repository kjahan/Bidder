from sklearn import linear_model
import pickle, parser, feature, encoder

class Model:
    def __init__(self):
        self.lr = None
        self.model_fn = '/var/www/bidengine/models/lr'
        self.enc = encoder.Encoder()

    #this method stores builds an lr model
    def build_lr_model(self, X, Y):
        print "start building lr model ..."
        lr = linear_model.LogisticRegression()
        lr.fit(X, Y)
        print "built done!"
        self.lr = lr

    #serialize model
    def save_model(self):
        with open(self.model_fn, 'wb') as fp:
            pickle.dump(self.lr, fp)

    #deserialize ml model
    def load_model(self):
        #print "get lr model"
        with open(self.model_fn,'rb') as fp:
            self.lr = pickle.load(fp)

    #this method takes one test point and returns y_pred, y and predicted label
    def predict(self, payload):
        data = parser.parse(payload) #parse payload
        fets = feature.extract_features(data)   #extract fet
        array, x = self.enc.encode(fets)  #encode fet
        # The output is always 1 or 0, not a probability number.
        y_pred = self.lr.predict(x)
        prob = self.lr.predict_proba(x)
        return {"prob": prob[0][1], "y_pred": y_pred} #store label and pr(y=1)
