import pandas as pd # CSV読み込み
import matplotlib # グラフの表示
import matplotlib.pyplot as plt

from datetime import datetime
matplotlib.rcParams["font.sans-serif"] = "MS Gothic" # グラフに表示する文字のエンコード形式
def main():
  # 為替データ読み込み
  Timeline_Data = pd.read_csv("multiTimeline.csv", # 読み込むファイル
                            header=3, # データ読み込み開始位置
                            index_col=0, # 項目の位置
                            parse_dates=True) # インデックスをdatetime型

  min_date = datetime(2004, 1, 1)
  max_date = datetime.now()
  
  #plt.subplot(1, 1, 1) # プロットの作成 3行中1列1行目
  plt.plot(Timeline_Data.index, Timeline_Data, label="件") # グラフの作成
  plt.xlim(min_date, max_date) # X軸(年)の範囲を指定
  plt.ylim(0, 130) # Y軸(実際の数値)の範囲
  plt.legend(loc="best") # 凡例の作成
  
  plt.savefig("timeline_data.png") # グラフの保存
  
if __name__ == "__main__":
  main()
  