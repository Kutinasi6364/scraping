# グラフ描画サンプル
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["font.sans-serif"] = "MS Gothic"
import matplotlib.pyplot as plt

plt.plot([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], "bx-", label="1次元関数")
plt.plot([1, 2, 3, 4, 5], [1, 4, 9, 16, 25], "ro--", label="2次元関数")
plt.xlabel("Xの値")
plt.ylabel("Yの値")
plt.title("matplotlibのサンプル")
plt.legend(loc="best")
plt.xlim(0, 6)
plt.savefig("advancedgraph.png", dpi=300)