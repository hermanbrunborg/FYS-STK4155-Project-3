import config
from tqdm import tqdm
from data import FrankeData
import matplotlib.pyplot as plt
from regression import OrdinaryLeastSquares
from bias_variance import bootstrap_bias_variance
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import GradientBoostingRegressor


# TODO: REMOVE?
def plot(mses_train, mses_test, biases, variances, title=""):
    plt.plot(mses_train, label="mse train")
    plt.plot(mses_test, label="mse test")
    if title:
        plt.title(title)
    plt.legend()
    plt.show()

    plt.plot(biases, label="bias")
    plt.plot(variances, label="variance")
    if title:
        plt.title(title)
    plt.legend()
    plt.show()


def write_to_file(filename, x, mses_train, mses_test, biases, variances, x_label):
    with open(f"output/data/{filename}", "w") as f:
        f.write(f"{x_label},mse_train,mse_test,bias,variance\n")
        for i in range(len(x)):
            f.write(
                f"{x[i]},{mses_train[i]},{mses_test[i]},{biases[i]},{variances[i]}\n"
            )


def bias_variance_analysis_ols():
    mses_train, mses_test, biases, variances = [], [], [], []
    #  degrees = list(range(1, 11))
    degrees = list(range(1, 16))
    for degree in degrees:
        data = FrankeData(
            config.DATA_SIZE, degree=degree, test_size=config.BIAS_VARIANCE_TEST_SIZE
        )
        bias, variance, mse_train, mse_test = bootstrap_bias_variance(
            OrdinaryLeastSquares(), data, config.BIAS_VARIANCE_BOOTSTRAP_SIZE
        )
        mses_train.append(mse_train)
        mses_test.append(mse_test)
        biases.append(bias)
        variances.append(variance)
        #  print(bias, variance, mse)

    write_to_file(
        "bias_variance_ols.csv",
        degrees,
        mses_train,
        mses_test,
        biases,
        variances,
        "degree",
    )


def bias_variance_analysis_mlp_layer_size():
    mses_train, mses_test, biases, variances = [], [], [], []
    data = FrankeData(config.DATA_SIZE, test_size=config.BIAS_VARIANCE_TEST_SIZE)
    layer_sizes = list(range(10, 100, 10))
    for layer_size in tqdm(layer_sizes):
        bias, variance, mse_train, mse_test = bootstrap_bias_variance(
            MLPRegressor(
                hidden_layer_sizes=(layer_size for _ in range(3)), max_iter=1000
            ),
            data,
            config.BIAS_VARIANCE_BOOTSTRAP_SIZE,
        )
        mses_train.append(mse_train)
        mses_test.append(mse_test)
        biases.append(bias)
        variances.append(variance)

    write_to_file(
        "bias_variance_mlp_layer_size.csv",
        layer_sizes,
        mses_train,
        mses_test,
        biases,
        variances,
        "layer size",
    )


def bias_variance_analysis_mlp_number_of_layers():
    mses_train, mses_test, biases, variances = [], [], [], []
    data = FrankeData(config.DATA_SIZE, test_size=config.BIAS_VARIANCE_TEST_SIZE)
    number_of_layers_list = list(range(1, 6))
    for number_of_layers in tqdm(number_of_layers_list):
        bias, variance, mse_train, mse_test = bootstrap_bias_variance(
            MLPRegressor(
                hidden_layer_sizes=(50 for _ in range(number_of_layers)), max_iter=1000
            ),
            data,
            config.BIAS_VARIANCE_BOOTSTRAP_SIZE,
        )
        mses_train.append(mse_train)
        mses_test.append(mse_test)
        biases.append(bias)
        variances.append(variance)

    write_to_file(
        "bias_variance_mlp_number_of_layers.csv",
        number_of_layers_list,
        mses_train,
        mses_test,
        biases,
        variances,
        "number of layers",
    )


def bias_variance_analysis_mlp():
    bias_variance_analysis_mlp_layer_size()
    bias_variance_analysis_mlp_number_of_layers()
    #  plot(mses, biases, variances)


def bias_variance_analysis_ensamble():
    mses_train, mses_test, biases, variances = [], [], [], []
    data = FrankeData(config.DATA_SIZE, test_size=config.BIAS_VARIANCE_TEST_SIZE)
    depths = list(range(1, 11))
    for depth in tqdm(depths):
        bias, variance, mse_train, mse_test = bootstrap_bias_variance(
            GradientBoostingRegressor(max_depth=depth),
            data,
            config.BIAS_VARIANCE_BOOTSTRAP_SIZE,
        )
        mses_train.append(mse_train)
        mses_test.append(mse_test)
        biases.append(bias)
        variances.append(variance)

        #  tqdm.write(f"{depth} {bias} {variance} {mse_train} {mse_test}")

    write_to_file(
        "bias_variance_ensamble.csv",
        depths,
        mses_train,
        mses_test,
        biases,
        variances,
        "depth",
    )
    #  plot(mses, biases, variances, "A")


def main():
    print(f"Running with boostrap size: {config.BIAS_VARIANCE_BOOTSTRAP_SIZE}")

    bias_variance_analysis_ols()
    #  bias_variance_analysis_mlp()
    #  bias_variance_analysis_ensamble()
