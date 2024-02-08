import streamlit as st

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import scipy.stats as stats

# アプリのタイトルと説明を表示
st.title("人生の羅針盤")
st.markdown("金融情報を入力すると、最適なライフプランを提案してくれるアプリです。")

# サイドバーに金融情報の入力欄を作成
st.sidebar.header("金融情報の入力")
# 年収の入力
income = st.sidebar.number_input("年収（万円）", min_value=0, max_value=10000, value=500, step=10)
# 貯金の入力
savings = st.sidebar.number_input("貯金（万円）", min_value=0, max_value=100000, value=1000, step=10)
# 支出の入力
expenses = st.sidebar.number_input("支出（万円/月）", min_value=0, max_value=1000, value=20, step=1)
# 投資の入力
investment = st.sidebar.number_input("投資（万円）", min_value=0, max_value=100000, value=0, step=10)
# 投資の利回りの入力
return_rate = st.sidebar.slider("投資の利回り（％/年）", min_value=0.0, max_value=20.0, value=5.0, step=0.1)
# ローンの入力
loan = st.sidebar.number_input("ローン（万円）", min_value=0, max_value=100000, value=0, step=10)

# ローンの利率の入力
interest_rate = st.sidebar.slider("ローンの利率（％/年）", min_value=0.0, max_value=20.0, value=2.0, step=0.1)

# サイドバーに個人情報の入力欄を作成
st.sidebar.header("個人情報の入力")
# 年齢の入力
age = st.sidebar.number_input("年齢（歳）", min_value=0, max_value=120, value=25, step=1)
# 性別の入力
gender = st.sidebar.radio("性別", ["男性", "女性"])
# 家族構成の入力
family = st.sidebar.multiselect("家族構成", ["配偶者", "子供", "親", "兄弟姉妹"], default=["配偶者"])

# メイン画面に金融情報と個人情報の入力内容を表示
st.header("入力内容の確認")
st.subheader("金融情報")
st.write(f"年収：{income}万円")
st.write(f"貯金：{savings}万円")
st.write(f"支出：{expenses}万円/月")
st.write(f"投資：{investment}万円")
st.write(f"投資の利回り：{return_rate}％/年")
st.write(f"ローン：{loan}万円")
st.write(f"ローンの利率：{interest_rate}％/年")
st.subheader("個人情報")
st.write(f"年齢：{age}歳")
st.write(f"性別：{gender}")
st.write(f"家族構成：{', '.join(family)}")

# メイン画面に将来の収入や支出のシミュレーションの結果を表示
st.header("将来の収入や支出のシミュレーション")
# シミュレーションの期間（年）を入力
years = st.number_input("シミュレーションの期間（年）", min_value=1, max_value=100, value=10, step=1)
# シミュレーションの回数を入力
trials = st.number_input("シミュレーションの回数", min_value=1, max_value=1000, value=100, step=1)
# シミュレーションの実行ボタンを作成
if st.button("シミュレーションを実行"):
    # シミュレーションの実行中のメッセージを表示
    st.write("シミュレーションを実行中です...")
    # シミュレーションの結果を格納するDataFrameを作成
    df = pd.DataFrame()
    # シミュレーションの回数分繰り返す
    for i in range(trials):
        # 収入のシミュレーション
        # 収入は正規分布に従うと仮定し、平均は年収、標準偏差は年収の10％とする
        income_sim = stats.norm.rvs(loc=income, scale=income*0.1, size=years)
        # 支出のシミュレーション
        # 支出は正規分布に従うと仮定し、平均は支出、標準偏差は支出の10％とする
        expenses_sim = stats.norm.rvs(loc=expenses, scale=expenses*0.1, size=years)
        # 投資のシミュレーション
        # 投資の利回りは正規分布に従うと仮定し、平均は投資の利回り、標準偏差は投資の利回りの10％とする
        return_rate_sim = stats.norm.rvs(loc=return_rate, scale=return_rate*0.1, size=years)
        # ローンのシミュレーション
        # ローンの利率は正規分布に従うと仮定し、平均はローンの利率、標準偏差はローンの利率の10％とする
        interest_rate_sim = stats.norm.rvs(loc=interest_rate, scale=interest_rate*0.1, size=years)
        # 貯金のシミュレーション
        # 貯金は初期値に収入と支出の差額を加え、投資の利回りで増減させる
        savings_sim = [savings]
        for j in range(years):
            savings_sim.append(savings_sim[-1] + (income_sim[j] - expenses_sim[j]*12) * (1 + return_rate_sim[j]/100))
            # ローンの残高のシミュレーション
        # ローンの残高は初期値にローンの利率で増加させ、支払い額で減少させる
        # 支払い額はローンの10％とする
        loan_sim = [loan]
        for j in range(years):
            loan_sim.append(loan_sim[-1] * (1 + interest_rate_sim[j]/100) - loan*0.1)
        # シミュレーションの結果をDataFrameに追加
        df[f"trial_{i+1}"] = np.array(savings_sim) - np.array(loan_sim)

    # シミュレーションの結果の平均と標準偏差を計算
    df["mean"] = df.mean(axis=1)
    df["std"] = df.std(axis=1)
    df

    # シミュレーションの結果をプロットする
    fig = px.line(df, x=df.index, y="mean", error_y="std", labels={"index": "年数", "mean": "貯金とローンの差額（万円）"})
    st.plotly_chart(fig)

    # シミュレーションの結果の要約を表示する
    st.subheader("シミュレーションの結果の要約")
    st.write(f"シミュレーションの期間：{years}年")
    st.write(f"シミュレーションの回数：{trials}回")
    st.write(f"初期の貯金とローンの差額：{savings - loan}万円")
    st.write(f"最終的な貯金とローンの差額の平均：{df['mean'].iloc[-1]:.2f}万円")
    st.write(f"最終的な貯金とローンの差額の標準偏差：{df['std'].iloc[-1]:.2f}万円")

    # 最適なライフプランを提案する
    st.header("最適なライフプランの提案")
    # 最適なライフプランを決めるための基準を入力
    target = st.number_input("目標とする貯金とローンの差額（万円）", min_value=0, max_value=100000, value=10000, step=10)
    probability = st.slider("目標を達成する確率（％）", min_value=0.0, max_value=100.0, value=90.0, step=0.1)

    # 最適なライフプランを計算ボタンを作成
    if st.button("最適なライフプランを計算"):
        # 目標を達成するために必要な年数を計算
        # 目標を達成する確率に対応するパーセンタイルを求める
        percentile = 100 - (100 - probability) / 2
        # パーセンタイルに対応する貯金とローンの差額を求める
        target_sim = np.percentile(df.drop("mean", axis=1), percentile, axis=1)
        # 貯金とローンの差額が目標を超える最初の年数を求める
        years_needed = np.argmax(target_sim >= target)

        # 最適なライフプランを表示する
        if years_needed == 0:
            st.success(f"おめでとうございます！あなたはすでに目標を達成しています。")
        elif years_needed < years:
            st.success(f"あなたの目標は{years_needed}年後に達成できると予測されます。")
        else:
            st.warning(f"あなたの目標は{years}年以内には達成できないと予測されます。")
            st.write(f"目標を達成するためには、以下の方法が考えられます。")
            st.write(f"- 年収を増やす")
            st.write(f"- 支出を減らす")
            st.write(f"- 投資額や投資の利回りを増やす")
            st.write(f"- ローン額やローンの利率を減らす")
