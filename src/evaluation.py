from sklearn.metrics import (accuracy_score,recall_score,f1_score,precision_score)

def evaluate_model(model,X_test,y_test):

    y_pred = model.predict(X_test)

    return {

        'Accuracy':
        accuracy_score(
            y_test,
            y_pred
        ),

        'Precision':
        precision_score(
            y_test,
            y_pred,
            average='macro'
        ),

        'Recall':
        recall_score(
            y_test,
            y_pred,
            average='macro'
        ),

        'F1':
        f1_score(
            y_test,
            y_pred,
            average='macro'
        )
    }