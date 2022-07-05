import pandas as pd
import matplotlib # グラフの表示
import matplotlib.pyplot as plt

from datetime import datetime
matplotlib.use("Agg")
matplotlib.rcParams["font.sans-serif"] = "MS Gothic" # グラフに表示する文字のエンコード形式
def main():
  # 為替データ読み込み
  df_exchange = pd.read_csv("exchange.csv", # 読み込むファイル
                            encoding="cp932", # エンコード形式
                            header=1, # データ読み込み開始位置
                            names=["date", "USD", "rate"], # 項目名を設定
                            index_col=0, # インデックスの列指定(日付)
                            parse_dates=True) #インデックスをdatetime型
  # 金利データ読み込み
  df_jgbcm = pd.read_csv("jgbcm_all.csv",
                          encoding="cp932",
                          header=1, # データ読み込み開始位置
                          index_col=0, # 項目の位置
                          parse_dates=True,
                          date_parser=parse_japanese_date,
                          na_values=["-"])
  # 有効求人倍率取り込み
  df_jobs = pd.read_excel("第3表.xlsx", # 読み込みファイル
                          skiprows=3, # 上から3行は無視
                          skipfooter=3, # 下から3行は無視
                          usecols="A, U:AF", # 指定した列を抽出
                          index_col=0) # インデックスの列指定
  df_jobs.columns = [c.split(".")[0] for c in df_jobs.columns]
  s_jobs = df_jobs.stack()
  s_jobs.index = [parse_year_and_month(y, m) for y, m in s_jobs.index]
  
  min_date = datetime(1973, 1, 1)
  max_date = datetime.now()
  
  plt.subplot(3, 1, 1) # プロットの作成 3行中1列1行目
  plt.plot(df_exchange.index, df_exchange.USD, label="ドル・円") # グラフの作成
  plt.xlim(min_date, max_date) # X軸(年)の範囲を指定
  plt.ylim(50, 250) # Y軸(実際の数値)の範囲
  plt.legend(loc="best") # 凡例の作成
  
  plt.subplot(3, 1 ,2) # プロットの作成 3行中1列2行目
  plt.plot(df_jgbcm.index, df_jgbcm["1年"], label="1年国債金利") # グラフの作成
  plt.plot(df_jgbcm.index, df_jgbcm["5年"], label="5年国債金利")
  plt.plot(df_jgbcm.index, df_jgbcm["10年"], label="10年国債金利")
  plt.xlim(min_date, max_date) # X軸(年)の範囲を指定
  plt.legend(loc="best") # 凡例の作成
  
  plt.subplot(3, 1, 3) # プロットの作成 3行中1列3行目
  plt.plot(s_jobs.index, s_jobs, label="有効球威人倍率(季節調整値)") # グラフの作成
  plt.xlim(min_date, max_date)  # X軸(年)の範囲を指定
  plt.ylim(0.0, 2.0) # Y軸(実際の数値)の範囲
  plt.axhline(y=1, color="gray") # 水平ライン
  plt.legend(loc="best") # 凡例の作成
  
  plt.savefig("historical_data.png", dpi=300)

# 和暦から西暦に変更
def parse_japanese_date(s: str) -> datetime:
  base_years = {"S": 1925, "H": 1988, "R": 2018}
  era = s[0]
  year, month, day = s[1:].split(".")
  year = base_years[era] + int(year)
  return datetime(year, int(month), int(day))

# 年月から西暦の数値に変換
def parse_year_and_month(year: str, month: str) -> datetime:
  year = int(year[:-1])
  month = int(month[:-1])
  #year += (1900 if year >= 63 else 2000)
  return datetime(year, month, 1)

if __name__ == "__main__":
  main()
  