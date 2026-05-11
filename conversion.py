import pandas as pd
import io
import holidays

# 실제 파일이 있다면 pd.read_csv('파일명.csv')로 불러오세요.
df_hum = pd.read_csv("monthly_humidity_results_2022.csv")
df_temp = pd.read_csv("monthly_temp_results_2022.csv")

# 2. 데이터 병합 (월 기준으로 병합)
# '월' 컬럼에서 '월' 글자 제거 및 정수 변환
df_hum['month'] = df_hum['월'].str.replace('월', '').astype(int)
df_temp['month'] = df_temp['월'].str.replace('월', '').astype(int)

df_merged = pd.merge(df_temp, df_hum, on='month')

def get_holiday_count(year, month):
    kr_holidays = holidays.KR(years=year)
    count = 0
    # 해당 연도/월의 모든 날짜를 순회하며 공휴일 확인
    for date in pd.date_range(start=f'{year}-{month}-01', end=pd.Period(f'{year}-{month}', freq='M').end_time):
        if date in kr_holidays or date.weekday() >= 5:
            count += 1
    return count

# 3. 목표 형식에 맞게 컬럼 재구성 및 추가
# 2024년 데이터라고 가정
target_year = 2022
final_data =[]

for _, row in df_merged.iterrows():
    month = int(row['month'])
    final_data.append({
        'year': target_year,
        'month': month,
        'usage': 0,  # 예측 데이터이므로 0 또는 추정치 입력
        'temp_mean': row['온도_평균'],
        'temp_min': row['온도_최저'],
        'temp_max': row['온도_최고'],
        'hum_mean': row['습도_평균'],
        'tropical_night': row['열대야일수'],
        'cdd': row['냉방도일'],
        'holiday_cnt': get_holiday_count(target_year, month)
    })

final_df = pd.DataFrame(final_data)

# 결과 출력 및 저장
print(final_df)
final_df.to_csv('prediction_data_2022.csv', index=False)