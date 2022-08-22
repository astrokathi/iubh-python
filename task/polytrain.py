from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt


class PolyTrain:

    def __init__(self):
        pass

    @staticmethod
    def polynomial_regression_df(df=None, feature_col=None, train_function_col=None, plot=True):
        """
        This will train the given function with (x,y) pair
        :param df: Dataframe with many training functions and x values
        :param feature_col: Feature column for the model training.
        :param train_function_col: column name of the df for which the model has to be evaluated
        :param plot: Boolean to specify whether to plot the curve
        :return: This returns polynomial transformer and the regression model
        """

        regression_model = LinearRegression()
        """
        Here the degree represents the degree of the polynomial for which the co-efficients are to be evaluated.
        y = a0 + a1.x^1 + a2.x^2 + a3.x^3 + .... + an.x^n
        The higher the degree, the better the accuracy of the model, it will have an optimum value.
        If we go beyond the optimum value, the model performance reduces, model gets saturated.
        which leads to the curse of dimensionality.
        """
        poly = PolynomialFeatures(degree=(1, 12), include_bias=False)

        # df shape would be initially, (len(df), ) which will be reshaped to (len(df), 1), to train the data.
        x_reg_train = df[feature_col].values.reshape(len(df), 1)
        y_reg_train = df[train_function_col].values.reshape(len(df), 1)

        # Transforming the x values with higher order values as features, and setting up a polynomial.
        poly_features = poly.fit_transform(x_reg_train)
        # Model training
        regression_model.fit(poly_features, y_reg_train)
        if plot:
            # scatter plot of the original (x,y) pair in black.
            plt.scatter(x_reg_train, y_reg_train, color='black')
            # scatter plot of the (x,y_predicted) pair for the predicted values in blue
            plt.plot(x_reg_train, regression_model.predict(poly_features), color='blue', linewidth=2)
            plt.show()
        return regression_model, poly
