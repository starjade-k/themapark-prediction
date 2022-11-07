import pandas as pd
import numpy as np

# 입력받은 df의 마지막부터, 정한 날짜(date)만큼의 날짜값을 갖는 데이터프레임 생성하는 함수
def date_df_maker(df, date):
    index_list = []
    for i in range(date):
        #index_list.append(df.index[-1] + pd.DateOffset(days=i+1))
        index_list.append(df.iloc[-1]["STD_DATE"] + pd.DateOffset(days=i+1))
    return index_list


# 입력받은 df의 마지막부터 원하는 날짜까지 하차총 승객수의 예측값을 반환시켜주는 함수
def predict(df, date, model, in_col, out_col):
    last_days = df.iloc[-11:][in_col].values.reshape(1, 11, 1)

    predict_entrance = []

    for i in range(1, date + 1):
        i = i + 1
        last_day = model.predict(last_days)
        predict_entrance.append(list(last_day[0]))
        last_days = np.delete(last_days[0], 0, 0)
        last_days = np.append(last_days, last_day)
        last_days = last_days.reshape(1, 11, 1)

    pred_pred_df = pd.DataFrame(predict_entrance, columns=[out_col], index=date_df_maker(df, date))

    return pred_pred_df

# 리스케일
def rescaler(df1, df2, in_col, out_col):
    df2[out_col] = df2[out_col].apply(lambda x: (max(df1[in_col]) - min(df1[in_col])) * x + min(df1[in_col]))
    df2[out_col] = df2[out_col].apply(lambda x: round(x, 0))
    return df2