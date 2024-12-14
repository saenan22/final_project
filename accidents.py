import streamlit as st
import folium
import geopandas as gpd
import pandas as pd
import json
from streamlit_folium import st_folium
import plotly.express as px

col1, col2, col3 = st.columns(3)
# Sidebar 메뉴 생성
st.sidebar.title("교통사고 대시보드🚗💥")


st.sidebar.markdown("하단의 화살표를 눌러 해당 Page의 내용을 확인해보세요.😊")


# 사이드바에서 페이지 선택
page = st.sidebar.selectbox("페이지 선택", ["Page 1", "Page 2", "Page 3"])

# Page 1 내용
if page == "Page 1":
    # CSV 파일을 불러오기
    url = 'https://raw.githubusercontent.com/saenan22/final_project/refs/heads/main/2021%EB%85%84%20OECD%EA%B5%AD%EA%B0%80%EA%B5%90%ED%86%B5%EC%82%AC%EA%B3%A0%20%ED%98%84%ED%99%A9.csv'
    df0 = pd.read_csv(url)

    # '-' 값은 NaN으로 변환하고 NaN 값 제거
    df0['자동차1만대당 사망(명)'] = pd.to_numeric(df0['자동차1만대당 사망(명)'], errors='coerce')
    df0_cleaned = df0.dropna(subset=['자동차1만대당 사망(명)'])

    # Streamlit 앱 설정
    st.title('자동차 1만대당 사망(명) 국가별 비교')

    # Plotly를 이용한 수평 막대그래프 그리기
    fig = px.bar(df0_cleaned, 
                 x='자동차1만대당 사망(명)',  # x축을 '자동차1만대당 사망(명)'으로 설정
                 y='국가',  # y축을 국가로 설정
                 hover_data={'국가': True, '자동차1만대당 사망(명)': True},
                 labels={'자동차1만대당 사망(명)': '자동차 1만대당 사망(명)', '국가': '국가'},
                 title='자동차 1만대당 사망(명) 국가별 비교')

    # 그래프 크기 조정
    fig.update_layout(width=1000, height=800)

    # 그래프 보여주기
    st.plotly_chart(fig, use_container_width=False)

    # '자동차1만대당 사망(명)' 기준으로 상위 10개 국가 추출
    top10_df = df0_cleaned.nlargest(10, '자동차1만대당 사망(명)')

    # '대한민국'을 red로 표시하고 나머지는 skyblue로 표시
    색상_dict = {'대한민국': 'red'}
    top10_df['색상'] = top10_df['국가'].map(색상_dict).fillna('skyblue')

    # '자동차1만대당 사망(명)'을 기준으로 내림차순 정렬
    top10_df = top10_df.sort_values(by='자동차1만대당 사망(명)', ascending=False)

    # Streamlit 앱 설정
    st.title('자동차 1만대당 사망(명) 상위 10개 국가')

    # Plotly를 이용한 막대그래프 그리기
    fig = px.bar(top10_df, 
                 x='자동차1만대당 사망(명)', 
                 y='국가', 
                 color='색상',  # 색상 열을 기준으로 색상 지정
                 hover_data={'국가': True, '자동차1만대당 사망(명)': True},
                 labels={'자동차1만대당 사망(명)': '자동차 1만대당 사망(명)', '국가': '국가'},
                 title='상위 10개 국가의 자동차 1만대당 사망(명)')

    # 범례 숨기기
    fig.update_layout(showlegend=False)

    # 그래프 보여주기
    st.plotly_chart(fig)

# Page 2 내용
elif page == "Page 2":
    st.title("대한민국 교통사고 분석")
    # 교통사고 분석 시작
    
    # 사고 데이터 불러오기
    file_path = r"https://raw.githubusercontent.com/saenan22/final_project/main/Report.csv"
    df = pd.read_csv(file_path, header=3)
    
    # 데이터 전처리
    df = df.dropna(subset=['시군구'])
    df['시군구'] = df['시군구'].replace({
        '창원시(통합)': '창원시',
        '진구': '부산진구'
    })
    
    # 시군구를 시 단위로 변환
    def map_to_city(region):
        if isinstance(region, str):
            city_mapping = {
                '청주시 서원구': '청주시',
                '청주시 상당구': '청주시',
                '청주시 청원구': '청주시',
                '청주시 흥덕구': '청주시',
                '수원시 팔달구': '수원시',
                '수원시 장안구': '수원시',
                '수원시 권선구': '수원시',
                '수원시 영통구': '수원시',
                '포항시 남구': '포항시',
                '포항시 북구': '포항시',
                '고양시 일산서구': '고양시',
                '고양시 덕양구': '고양시',
                '고양시 일산동구': '고양시',
                '성남시 중원구': '성남시',
                '성남시 분당구': '성남시',
                '성남시 수정구': '성남시',
                '성남시 성남구': '성남시',
                '안양시 동안구': '안양시',
                '안양시 만안구': '안양시',
                '용인시 처인구': '용인시',
                '용인시 수지구': '용인시',
                '창원시 진해구': '창원시',
                '창원시 마산합포구': '창원시',
                '창원시 의창구': '창원시',
                '창원시 성산구': '창원시',
                '전주시 덕진구': '전주시',
                '전주시 완산구': '전주시',
                '안산시 단원구': '안산시',
                '안산시 상록구': '안산시',
                '천안시 서북구': '천안시',
                '천안시 동남구': '천안시',
            }
            return city_mapping.get(region, region.split()[0])
        return region
    
    df['시군구_시단위'] = df['시군구'].apply(map_to_city)

    # 시간대별 교통사고 분석
    st.subheader("시간대별 교통사고 분석")
    # 데이터에 시간대 컬럼이 있다면, 예를 들어 '사고발생시간' 컬럼을 기준으로 시간대별 교통사고 건수를 분석
    if '사고발생시간' in df.columns:
        df['시간대'] = df['사고발생시간'].apply(lambda x: str(x)[:2])  # 사고 발생 시간의 첫 두 자리를 시간대 구분
        accident_by_time = df.groupby('시간대')['사고[건]'].sum().reset_index()
        st.write(accident_by_time)

        # 시간대별 사고 건수 그래프
        fig = px.bar(accident_by_time, x='시간대', y='사고[건]', title="시간대별 교통사고 건수")
        st.plotly_chart(fig)
    
    # 요일별 교통사고 분석
    st.subheader("요일별 교통사고 분석")
    # 요일별 사고 분석 (사고일자 컬럼 기준)
    if '사고일자' in df.columns:
        df['요일'] = pd.to_datetime(df['사고일자'], errors='coerce').dt.day_name()
        accident_by_day = df.groupby('요일')['사고[건]'].sum().reset_index()
        accident_by_day = accident_by_day[['요일', '사고[건]']].set_index('요일').reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).reset_index()
        
        st.write(accident_by_day)

        # 요일별 사고 건수 그래프
        fig = px.bar(accident_by_day, x='요일', y='사고[건]', title="요일별 교통사고 건수")
        st.plotly_chart(fig)
    
    # 연령층별 교통사고 분석
    st.subheader("연령층별 교통사고 분석")
    if '연령대' in df.columns:  # '연령대' 컬럼이 있을 경우
        age_group_accidents = df.groupby('연령대')['사고[건]'].sum().reset_index()
        st.write(age_group_accidents)

        # 연령대별 사고 건수 그래프
        fig = px.bar(age_group_accidents, x='연령대', y='사고[건]', title="연령대별 교통사고 건수")
        st.plotly_chart(fig)
    
    # 기상상태별 교통사고 분석
    st.subheader("기상상태별 교통사고 분석")
    if '기상상태' in df.columns:  # '기상상태' 컬럼이 있을 경우
        weather_accidents = df.groupby('기상상태')['사고[건]'].sum().reset_index()
        st.write(weather_accidents)

        # 기상상태별 사고 건수 그래프
        fig = px.bar(weather_accidents, x='기상상태', y='사고[건]', title="기상상태별 교통사고 건수")
        st.plotly_chart(fig)
    
    # 교통사고 데이터 시각화
    st.subheader("교통사고 지역별 시각화")
    # 지도에서 교통사고 발생 지역을 시각화
    import folium
    from streamlit_folium import st_folium

    # 지도 생성 및 데이터 시각화 추가
    map_center = [36.5, 127.8]
    m = folium.Map(location=map_center, zoom_start=7)

    # Choropleth 맵 추가
    folium.Choropleth(
        geo_data=geojson_data,
        name="choropleth",
        data=df,
        columns=['시군구', '사고[건]'],
        key_on="feature.properties.시군구_시단위",
        fill_color="YlGn",
        fill_opacity=0.7,
        line_opacity=0.3,
        legend_name="교통사고 건수"
    ).add_to(m)

    # 툴팁 추가
    folium.GeoJson(
        geojson_data,
        name="지역 정보",
        tooltip=folium.GeoJsonTooltip(fields=['시군구_시단위'], aliases=["시군구:"], localize=True),
        style_function=lambda x: {"color": "transparent", "weight": 0}
    ).add_to(m)

    # Folium 지도 출력
    st_folium(m, width=700, height=500)




# Page 3 내용
elif page == "Page 3":
    st.title("교통사고 예방 정보")
    # Page 3 관련 코드 추가


import streamlit as st

# 1. 버튼
if st.button("Click Me"):
    st.write("Button Clicked!")

# 2. 체크박스
checked = st.checkbox("I agree")
if checked:
    st.write("Checkbox is checked!")

# 3. 라디오 버튼
choice = st.radio("Choose an option:", ["Option 1", "Option 2", "Option 3"])
st.write(f"You selected: {choice}")

# 4. 슬라이더
value = st.slider("Pick a number:", 0, 100, 50)
st.write(f"Slider value is: {value}")

# 5. 드롭다운 (selectbox)
dropdown = st.selectbox("Select an item:", ["Item 1", "Item 2", "Item 3"])
st.write(f"You selected: {dropdown}")

# 6. 텍스트 입력
text_input = st.text_input("Enter some text:")
st.write(f"You entered: {text_input}")

# 7. 파일 업로드
uploaded_file = st.file_uploader("Upload a file")
if uploaded_file:
    st.write("File uploaded successfully!")


import streamlit as st

# 세 개의 컬럼 생성
col1, col2, col3 = st.columns(3)

# 각 컬럼에 다른 콘텐츠 추가
with col1:
    st.header("Column 1")
    st.write("This is the content of column 1.")

with col2:
    st.header("Column 2")
    st.write("This is the content of column 2.")

with col3:
    st.header("Column 3")
    st.write("This is the content of column 3.")


