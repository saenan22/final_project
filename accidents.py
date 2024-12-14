import streamlit as st
import folium
import geopandas as gpd
import pandas as pd
import json
from streamlit_folium import st_folium

st.sidebar.title("교통사고 대시보드🚗💥")
# Sidebar 메뉴 생성
# 페이지별 내용 출력
if menu == "Page 1":
    st.title("Welcome to Page 1")
    st.write("This is Page 1 content.")

elif menu == "Page 2":
    st.title("Welcome to Page 2")
    st.write("This is Page 2 content.")

elif menu == "Page 3":
    st.title("Welcome to Page 3")
    st.write("This is Page 3 content.")
# 사이드바 메뉴 구현
with st.sidebar:
    # 확장 가능한 메뉴 만들기 (화살표처럼 보이게)
    with st.expander("Page 1"):
        st.write("OECE국가 교통사고 건수 현황")
        # Page 1 관련 코드 추가
    
    with st.expander("Page 2"):
        st.write("대한민국 교통사고 ")
        # Page 2 관련 코드 추가

    with st.expander("Page 3"):
        st.write("This is Page 3 content.")
        # Page 3 관련 코드 추가


# 1. 교통사고 데이터 불러오기
file_path = r"https://raw.githubusercontent.com/saenan22/final_project/main/Report.csv"
df = pd.read_csv(file_path, header=3)

# 2. GeoJSON 파일 불러오기
import geopandas as gpd

# GeoJSON 파일 URL
geojson_url = "https://raw.githubusercontent.com/saenan22/final_project/main/BND_SIGUNGU_PG.json"

# GeoJSON 읽기
geojson_data = gpd.read_file(geojson_url)

# geojson_data는 GeoDataFrame으로, 이후에 사용할 수 있습니다.


# 데이터 처리
# 1. NaN 값 제거 (시군구 열에서 NaN이 있는 행 삭제)
df = df.dropna(subset=['시군구'])

# 2. 특정 시군구 값 변경
df['시군구'] = df['시군구'].replace({
'창원시(통합)': '창원시',
'진구': '부산진구'
    })

# 시군구를 시 단위로 변환하는 함수
def map_to_city(region):
    if isinstance(region, str):  # Check if the value is a string
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
            '성남시 성남구': '성남시',  # 구가 아니라 시로 처리
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
        # If the region is not in the city_mapping, take the first part of the string (before the space)
        return city_mapping.get(region, region.split()[0])
    else:
        return region  # Return the value as-is if it's not a string (e.g., NaN or float)



# 3. GeoJSON의 시군구를 시 단위로 변환
geojson_data['시군구_시단위'] = geojson_data['SIGUNGU_NM'].apply(map_to_city)

# 4. 데이터프레임의 시군구도 시 단위로 변환
df['시군구_시단위'] = df['시군구'].apply(map_to_city)

# 5. Folium 지도 만들기
map_center = [36.5, 127.8]  # 대한민국 중심
m = folium.Map(location=map_center, zoom_start=7)

# Choropleth 추가
folium.Choropleth(
    geo_data=geojson_data,
    name="choropleth",
    data=df,
    columns=['시군구', '사고[건]'],  # 시군구와 사고 건수
    key_on="feature.properties.시군구_시단위",  # GeoJSON의 시군구 이름과 연결
    fill_color="YlGn",  # 색상
    fill_opacity=0.7,
    line_opacity=0.3,
    legend_name="교통사고 건수"
).add_to(m)

# GeoJson 툴팁 추가
folium.GeoJson(
    geojson_data,
    name="지역 정보",
    tooltip=folium.GeoJsonTooltip(
        fields=['시군구_시단위'],
        aliases=["시군구:"],
        localize=True
    ),
    style_function=lambda x: {
        "color": "transparent", 
        "weight": 0
    }
).add_to(m)

# 지도 출력 (Streamlit에서 folium 지도 출력)
st.title("⚠️대한민국 교통사고지역 지도⚠️ ")
st_folium(m, width=700, height=500)

# 사이드바 옵션 추가
st.sidebar.title("교통사고 분석")
option = st.sidebar.selectbox(
    "분석 항목 선택",
    ["시간대별 교통사고", "부문별 교통사고", "요일별 교통사고","연령층별 교통사고","기상상태별 교통사고"]
)












# 제목
st.title("교통사고 데이터 분석")

# 메인 화면에서 필터링 옵션 추가 (사이드바가 아닌 일반 화면)
st.subheader("데이터 필터링")
filter_option = st.selectbox(
    "지역 선택",
     df['시도'].unique()
)

# 필터 옵션에 따라 데이터 출력 (예시로만 출력)
st.write(f"선택된 지역: {filter_option}")

# 선택된 지역에 따라 필터링된 데이터 보여주기
if filter_option != "전체":
    df_filtered = df[df["시도"] == filter_option]
else:
    df_filtered = df

st.write(df_filtered)

# 선택된 필터 옵션과 관련된 다른 분석 추가 (예시)
# 마지막 행 삭제 (시도 열의 마지막 행)
import altair as alt
import streamlit as st
import pandas as pd
import plotly.express as px
# 시도별 사고 건수 시각화
# 그룹화된 데이터 생성
# 시도별 사고 건수 합산
grouped_data = df_filtered.groupby("시도")["사고[건]"].sum().reset_index()

# 막대그래프 생성
fig = px.bar(grouped_data, x="시도", y="사고[건]", title="시도별 사고 건수", labels={"사고[건]": "사고 건수"})

# 그래프 표시
st.plotly_chart(fig)



# 사이드바에 지역 선택 추가
st.sidebar.subheader("지역 선택")
selected_regions = st.sidebar.multiselect(
    "지역을 선택하세요",
    df['시도'].unique(),
    default=["서울"]  # 기본적으로 서울을 선택하도록 설정
)

# 선택된 지역에 맞춰 데이터 필터링
if selected_regions:
    df_filtered = df[df["시도"].isin(selected_regions)]
else:
    df_filtered = df  # 선택된 지역이 없으면 전체 데이터 출력

# 필터링된 데이터 출력
st.write("선택된 지역에 대한 교통사고 데이터:")
st.write(df_filtered)




# 필터링된 데이터에 대한 차트 출력
st.subheader("선택된 지역에 따른 사고 통계")

grouped_data = df_filtered.groupby("시도")["사고[건]"].sum().reset_index()

# 막대그래프 생성
fig = px.bar(grouped_data, x="시도", y="사고[건]", title="시도별 사고 건수", labels={"사고[건]": "사고 건수"})

# 그래프 표시
st.plotly_chart(fig, key="unique_plot_key")


# Sidebar 메뉴 생성
menu = st.sidebar.selectbox(
    "Select a Page",
    ["Page 1", "Page 2", "Page 3"]
)




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


