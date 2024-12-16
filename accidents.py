import streamlit as st
import folium
import geopandas as gpd
import pandas as pd
import json
from streamlit_folium import st_folium
import plotly.express as px
import numpy as np
import requests
# Sidebar 메뉴 생성
st.sidebar.title("교통사고 대시보드🚗💥")
st.sidebar.markdown("[My Streamlit Dashboard](https://finalproject-kepgmfers6jvwdtelxf9k4.streamlit.app/)", unsafe_allow_html=True)

st.sidebar.markdown("하단의 화살표를 눌러 해당 Page의 내용을 확인해보세요.😊")


# 사이드바에서 페이지 선택
page = st.sidebar.selectbox("페이지 선택", ["Page 1", "Page 2", "Page 3"])





# Page 1 내용
if page == "Page 1":
    # 국가 이름을 ISO 3166-1 alpha-3 코드로 변환하는 딕셔너리
    country_to_iso3 = {
    '그리스': 'GRC','네덜란드': 'NLD','노르웨이': 'NOR','뉴질랜드': 'NZL','대한민국': 'KOR','덴마크': 'DNK','독일': 'DEU',
    '라트비아': 'LVA','룩셈부르크': 'LUX','리투아니아': 'LTU','멕시코': 'MEX','미국': 'USA','벨기에': 'BEL','스웨덴': 'SWE',
    '스위스': 'CHE','스페인': 'ESP','슬로바키아': 'SVK','슬로베니아': 'SVN','아이슬란드': 'ISL','아일랜드': 'IRL',
    '에스토니아': 'EST','영국': 'GBR','오스트리아': 'AUT','이스라엘': 'ISR','이탈리아': 'ITA','일본': 'JPN','체코': 'CZE',
    '칠레': 'CHL','캐나다': 'CAN','코스타리카': 'CRI','콜롬비아': 'COL','튀르키예': 'TUR','포르투갈': 'PRT','폴란드': 'POL',
    '프랑스': 'FRA','핀란드': 'FIN','헝가리': 'HUN','호주': 'AUS'}


    # Streamlit 앱 제목
    st.title('OECD 국가🌍 교통사고 현황🚨')
    st.subheader("2021년도 기준 OECD국가별 자동차1만대당 사망 현황")
    st.write('''이때 "자동차1만대당 사망"은 특정 지역에서 운행 중인 자동차 1만 대당 발생하는 교통사고 사망자의 수를 의미합니다.''')

    # CSV 파일 불러오기
    url = 'https://raw.githubusercontent.com/saenan22/final_project/refs/heads/main/2021%EB%85%84%20OECD%EA%B5%AD%EA%B0%80%EA%B5%90%ED%86%B5%EC%82%AC%EA%B3%A0%20%ED%98%84%ED%99%A9.csv'
    df0 = pd.read_csv(url)

    # 국가 이름을 ISO3 코드로 변환한 새로운 열 'ISO3' 추가
    df0['ISO3'] = df0['국가'].map(country_to_iso3)


    # '-' 값은 NaN으로 변환하고 NaN 값 제거
    df0['자동차1만대당 사망(명)'] = pd.to_numeric(df0['자동차1만대당 사망(명)'], errors='coerce')
    df0_cleaned = df0.dropna(subset=['자동차1만대당 사망(명)'])


    # Plotly 지도 시각화 (Mapbox 스타일 사용)
    fig = px.choropleth(df0_cleaned,
                    locations="ISO3",  # ISO3 코드 사용
                    color="자동차1만대당 사망(명)",  # 색상은 '자동차1만대당 사망(명)'을 기준으로
                    hover_name="국가",  # 툴팁에 국가 이름을 표시
                    hover_data=["자동차1만대당 사망(명)"],  # 툴팁에 자동차 1만대당 사망자 수 추가
                    color_continuous_scale=px.colors.sequential.Plasma,  # 색상 스케일
                    labels={"자동차1만대당 사망(명)": "자동차 1만대당 사망(명)"},  # 레이블 설정
                    title="2021년도 기준 OECD국가별 자동차1만대당 사망 현황",  # 제목 설정
                    template="plotly_dark" ) # 다크 테마


    # 지도 출력
    fig.update_geos(showcoastlines=True, coastlinecolor="Black", projection_type="natural earth")

    # Streamlit으로 지도 시각화 출력
    st.plotly_chart(fig)
    
    st.write("""📌참고""")
    st.write("""가져온 데이터셋에서 OECD국가 중 "자동차1만대당 사망(명)" 열이 없는 국가는 모두 행 제거 처리를 했음으로 모든 OECD국가가 시각화되지 않을수 있음.""")
    st.write("""그러나 교통사고 빈도가 가장 높은 국가를 확인할수있음.""")

    st.write("""📌참고""")
    st.write("k=1000단위로 해석하시면 됩니다.")
    st.write("ex) 10k명=10000명")


    
    # OECD국가별 교통사고관련데이터 가져오기
    url = 'https://raw.githubusercontent.com/saenan22/final_project/refs/heads/main/2021%EB%85%84%20OECD%EA%B5%AD%EA%B0%80%EA%B5%90%ED%86%B5%EC%82%AC%EA%B3%A0%20%ED%98%84%ED%99%A9.csv'
    df0 = pd.read_csv(url)


    # '-' 값은 NaN으로 변환하고 NaN 값 제거
    df0['자동차1만대당 사망(명)'] = pd.to_numeric(df0['자동차1만대당 사망(명)'], errors='coerce')
    df0_cleaned = df0.dropna(subset=['자동차1만대당 사망(명)'])


    # '-' 값은 NaN으로 변환하고 NaN 값 제거
    df0['자동차1만대당 사망(명)'] = pd.to_numeric(df0['자동차1만대당 사망(명)'], errors='coerce')
    df0_cleaned = df0.dropna(subset=['자동차1만대당 사망(명)'])

     # 사이드바에서 국가 선택
    countries = df0_cleaned['국가'].unique()
    st.sidebar.subheader("국가 선택")
    selected_country = st.sidebar.multiselect("국가를 선택하세요:", countries,default=[])

    # 선택된 지역에 맞춰 데이터 필터링
    if selected_country:
        df0_cleaned = df0_cleaned[df0_cleaned["국가"].isin(selected_country)]
    else:
        df0_cleaned = df0_cleaned  # 선택된 국가가 없으면 전체 데이터 출력

    

    #막대그래프 
    st.subheader("선택된 국가에 따른 교통사고 통계📊 ")

    # Plotly를 이용한 수평 막대그래프 그리기
    fig = px.bar( df0_cleaned, 
                 x='자동차1만대당 사망(명)',  # x축을 '자동차1만대당 사망(명)'으로 설정
                 y='국가',  # y축을 국가로 설정
                 hover_data={'국가': True, '자동차1만대당 사망(명)': True},
                 labels={'명': '자동차1만대당 사망(명)', '국가': '국가'},
                 title='자동차 1만대당 사망(명) 국가별 비교')

    # 그래프 크기 조정
    fig.update_layout(width=1000, height=800)
    # 그래프 보여주기
    st.plotly_chart(fig, use_container_width=False,key="oecd_plot_key")

    st.write("2021년기준 OECD국가중 자동차1만대당 사망수가 가장 높은국가는 콜롬비아로 확인할 수있다.")
    st.write("그이유는 다음과 같습니다.")

    st.title("콜롬비아 자동차 사망률 분석🔍")


    st.header("교통사고 사망률의 주요 원인")
    st.write("1. 도로 인프라와 상태 부족")
    st.write("""
콜롬비아의 도로는 많은 부분이 좁고 울퉁불퉁하며, 일부 지역은 아스팔트가 아닌 비포장 도로가 많습니다. 특히 교외 지역에서는 도로 품질이 낮아 사고 위험이 증가합니다.
""")

    st.write("2. 차량 상태 부족")
    st.write("""
콜롬비아에서는 오래되고 안전 기능이 부족한 차량들이 많이 운행되고 있습니다. 많은 차량들이 정기적인 점검을 받지 않거나, 기본적인 안전 장치(예: 에어백, ABS)가 부족한 경우가 많아 사고 시 치명적일 수 있습니다.
""")

    st.write("3. 교통 법규 준수 부족")
    st.write("""
과속, 음주운전, 신호 위반 등 교통법규를 지키지 않는 운전자가 많습니다. 이러한 교통법규 위반은 사고를 일으킬 확률을 높입니다.
""")

    st.write("4. 불충분한 응급 구조 시스템")
    st.write("""
사고 발생 시 빠른 응급 구조가 어려운 경우가 많습니다. 특히, 시외 지역에서는 의료 지원을 받기 어려운 상황이 많아 사고로 인한 피해가 더 클 수 있습니다.
""")

    st.write("5. 교통 밀집과 과다한 차량 수")
    st.write("""
도시 지역에서는 차량 수가 급증하고, 이에 맞춘 도로 확장이나 교통 관리 시스템이 부족해 사고 위험이 증가합니다.
""")
    

    
    st.title('자동차1만대당 사망수 빈도 분석')
   # 사고 빈도가 높은 국가 Top 10 버튼
    st.write("버튼을 눌러주세요👆")
    if st.button("자동차1만대당 사망수가 높은 국가 Top 10🔺"):
        top_high_freq = df0_cleaned.nlargest(10, "자동차1만대당 사망(명)")
        top_high_freq['순위'] = range(1, len(top_high_freq) + 1)
        top_high_freq = top_high_freq.reset_index(drop=True)
        top_high_freq = top_high_freq[['국가', '사고(건)', '사망(명)', '자동차1만대당 사망(명)']]
        st.subheader("자동차1만대당 사망수가 높은 국가 Top 10")
        st.write(top_high_freq)
        color_map = {국가: '#FF5733' if 국가 == '대한민국' else '#1f77b4' for 국가 in top_high_freq['국가']}


        # 그래프 생성
        fig_high = px.bar(top_high_freq, x="국가", y="자동차1만대당 사망(명)", 
                      title="자동차1만대당 사망수가 높은 국가 Top 10", 
                      labels={"자동차1만대당 사망(명)": "자동차1만대당 사망(명)"},
                         color='국가', color_discrete_map=color_map)
        
        st.plotly_chart(fig_high)

         # 특징정리내용
        st.write("콜롬비아, 칠레, 코스타리카, 미국, 헝가리, 대한민국 순으로 정렬된 그래프에서, 상대적으로 지리적 규모가 작은 대한민국의 교통사고율이 높다는 점을 확인할 수 있습니다.")
        st.subheader("교통사고 사망률이 높은 국가들의 공통 요인")
        st.write("""
교통사고 사망률이 높은 국가들의 주요 원인은 다음 세 가지로 요약할 수 있습니다:

1. **도로 인프라와 차량 상태**: 도로 상태가 열악하거나, 오래되고 안전 기능이 부족한 차량이 많이 운행됩니다.
2. **운전 습관과 법 집행 부족**: 과속, 음주운전, 신호 위반 등 운전자의 법규 미준수와 느슨한 법 집행이 사고 위험을 높입니다.
3. **응급 구조 체계와 교육 부족**: 사고 후 빠른 응급 구조 체계가 미비하며, 교통안전 교육이 부족해 사고율 감소에 어려움을 겪고 있습니다.
""")



    # 사고 빈도가 낮은 국가 Top 10 버튼
    st.write("버튼을 눌러주세요👆")
    if st.button("자동차1만대당 사망수가 낮은 국가 Top 10🛡️"):
        top_low_freq = df0_cleaned.nsmallest(10, "자동차1만대당 사망(명)")
        top_low_freq['순위'] = range(1, len(top_low_freq) + 1)
        top_low_freq = top_low_freq.reset_index(drop=True)
        top_low_freq = top_low_freq[['국가', '사고(건)', '사망(명)', '자동차1만대당 사망(명)']]
        st.subheader("자동차1만대당 사망수가 낮은 국가 Top 10")
        st.write(top_low_freq)

        # 그래프 생성
        fig_low = px.bar(top_low_freq, x="국가", y="자동차1만대당 사망(명)", 
                     title="자동차1만대당 사망수가 낮은 국가 Top 10", 
                     labels={"자동차1만대당 사망(명)": "자동차1만대당 사망(명)"})

        st.plotly_chart(fig_low)
        st.write("노르웨이,스웨덴,스위스,아이슬란드,네덜란드순으로 정롈되어있으며 노르웨이의 교통사고율이 가장 적음을 확인할 수있습니다.")
        # 특징정리내용 
        st.subheader("교통사고 사망률이 낮은 국가들의 공통 요인")
        st.write("""
교통사고 사망률이 낮은 국가들의 주요 공통점은 다음과 같습니다:

1. **우수한 도로 인프라**: 잘 관리된 도로와 선진 교통 시스템으로 사고 위험을 낮춥니다.
2. **엄격한 교통법규와 운전자 교육**: 법규 준수율이 높고 운전자들이 충분한 교육을 받습니다.
3. **신속한 응급 구조 시스템**: 사고 발생 시 빠르고 효율적인 응급 구조와 의료 지원이 가능합니다.
""")







# Page 2 내용
elif page == "Page 2":
    st.title("대한민국 교통사고 분석")
      # 사이드바 옵션 추가
    st.sidebar.title("교통사고 분석")
    option = st.sidebar.selectbox(
        "분석 항목 선택",
        ["시도및 시군구별 교통사고","부문별 교통사고(최근5년)","시간대별 교통사고", "요일별 교통사고","월별 교통사고","사고유형별 교통사고"]
    )
    if option == "시도및 시군구별 교통사고":
        file_path = r"https://raw.githubusercontent.com/saenan22/final_project/main/Report.csv"
        df = pd.read_csv(file_path, header=3)
        # GeoJSON URL
        geojson_url = "https://raw.githubusercontent.com/saenan22/final_project/main/BND_SIGUNGU_PG.json"
# URL에서 GeoJSON 파일을 다운로드
        response = requests.get(geojson_url)

# 다운로드한 파일을 로컬에 저장
        with open("BND_SIGUNGU_PG.json", "wb") as f:
            f.write(response.content)

# 로컬 파일 읽기
        geojson_data = gpd.read_file("BND_SIGUNGU_PG.json")
       

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
        st.subheader("⚠️2023년 기준 대한민국 교통사고지역 지도⚠️ ")
        st_folium(m, width=700, height=500)


        # 사이드바에 지역 선택 추가
        st.sidebar.subheader("지역 선택")
        selected_regions = st.sidebar.multiselect(
        "원하는 지역들을 선택하실 수 있습니다.",
        df['시도'].unique(),
        default=[]  # 기본적으로 아무것도 선택하지 않도록 설정
    )

    # 선택된 지역에 맞춰 데이터 필터링
        if selected_regions:
            df_filtered = df[df["시도"].isin(selected_regions)]
        else:
            df_filtered = df  # 선택된 지역이 없으면 전체 데이터 출력


    # 필터링된 데이터에 대한 차트 출력
        st.write("""📌참고""")
        st.write("k=1000단위로 해석하시면 됩니다.")
        st.write("ex) 10k건=10000건")
    #reset_index()를 통해 데이터프레임화시키기기
        grouped_data = df_filtered.groupby("시도")["사고[건]"].sum().reset_index()

        st.subheader("선택된 지역에 따른 시도별 사고 통계")

    # 막대그래프 생성
        fig = px.bar(grouped_data, x="시도", y="사고[건]", title="2023년 기준 시도및 시군구별 사고 건수", labels={"사고[건]": "사고 건수"})

    # 그래프 표시
        st.plotly_chart(fig, key="unique_plot_key")



    # 필터링된 데이터에 대한 차트 출력2
        st.subheader("선택된 지역에 따른 시도별 사망 통계")

        grouped_data = df_filtered.groupby("시도")["사망[명]"].sum().reset_index()

    # 막대그래프 생성
        fig = px.bar(grouped_data, x="시도", y="사망[명]", title="2023년 기준 시도및 시군구별 사망 수", labels={"사망[명]": "사망자수"},color_discrete_sequence=["#FFCDD2"])

    # 그래프 표시
        st.plotly_chart(fig, key="deaths_plot_key")


    # 필터링된 데이터에 대한 차트 출력3
        st.subheader("선택된 지역에 따른 시도별 부상 통계")

        grouped_data = df_filtered.groupby("시도")["부상[명]"].sum().reset_index()

    # 막대그래프 생성
        fig = px.bar(grouped_data, x="시도", y="부상[명]", title="2023년 기준 시도및 시군구별 부상 수", labels={"부상[명]": "부상자수"},color_discrete_sequence=["#81C784"])

    # 그래프 표시
        st.plotly_chart(fig, key="injuries_plot_key")

    #인사이트 도출
        st.write("2023년도 기준 대한민국의 교통사고수,사망수,부상자수가 서울,경기도 쪽에서 현저히 높음을 확인할수있다.")

    #데이터프레임형태로 나타냄 
        st.subheader("선택된 지역에 대한 교통사고 통계")
        st.write(df_filtered)
        

    # 다음 새로운 제목선정
        st.title("시군구별 교통사고 빈도")
        st.write("""2023년 기준,좀 더 세분화된 지역의 교통사고건 현황을 파악하실 수 있습니다.""")

    # 두 개의 컬럼 생성
        col1, col2 = st.columns(2)
    # 각 컬럼에 다른 콘텐츠 추가

    
        with col1:
            top_5 = df.nlargest(5, '사고[건]')  # 사고[건]이 가장 높은 5개 지역
            top_5['순위'] = range(1, len(top_5) + 1)
            bottom_5 = df.nsmallest(5, '사고[건]')  # 사고[건]이 가장 낮은 5개 지역
            bottom_5['순위'] = range(1, len(bottom_5) + 1) 
                #index 삭제 
            top_5 = top_5.reset_index(drop=True)
            bottom_5 = bottom_5.reset_index(drop=True)
            top_5 = top_5[['순위', '시도', '시군구', '사고[건]']]
            bottom_5 = bottom_5[['순위', '시도', '시군구', '사고[건]']]
        
   
            st.write('체크박스를 클릭해 주세요 ✔️')
            st.write('분석결과를 확인하실수 있어요!')
            if st.checkbox("교통사고 빈도가 낮은 지역 Top 5🛡️"):
                st.dataframe(bottom_5)
                fig_bottom = px.bar(bottom_5, 
                     x='사고[건]', 
                     y='시군구',
                     title='TOP5 지역',
                     color='사고[건]',
                     labels={'사고[건]': '사고[건]', '시군구': '지역'},
                     hover_data=['시도','시군구', '사고[건]'])# Hover시 시도와 사고[건]을 표시
                   
                fig_bottom.update_layout(coloraxis_colorbar=dict(title="사고[건]"),width=1000,height=500)
                st.plotly_chart(fig_bottom)  # Plotly 차트를 Streamlit에 출력
                st.header('지역적 특징🔍')
                st.write("""가장 교통사고건수가 낮은 지역으로는 경북-울릉군이 선정되었었다. 그다음으로는 인천-옹진군,전북-장수군순으로 지역이 선정되었다. """)
                st.write("""교통사고 빈도가 낮은 지역은 주로 다음과 같은 특징을 가짐
- **인구 밀도가 낮은 지역**: 인구가 적고 차량의 통행량이 적은 지역에서 사고 발생이 적음.
- **교통량이 적은 시골 지역**: 차량의 통행량이 적고, 도로가 상대적으로 넓고 직선적인 시골 지역에서 사고 발생이 적음.
""")

        
        with col2:
            st.write('체크박스를 클릭해 주세요 ✔️')
            st.write('분석결과를 확인하실수 있어요!')
            if st.checkbox("교통사고 빈도가 높은 지역 Top 5🚨🔺"):
                st.dataframe(top_5)

         # 상위 5개 지역 막대그래프 시각화 (Plotly 사용)

                fig_top = px.bar(top_5, 
                     x='사고[건]',
                     y='시군구', 
                     title='TOP5 지역',
                     color='사고[건]',
                     labels={'사고[건]': '사고[건]', '시군구': '지역'},
                     hover_data=['시도','시군구', '사고[건]'],
                    color_continuous_scale=px.colors.sequential.Reds)# Hover시 시도와 사고[건]을 표시
                
                fig_top.update_layout(coloraxis_colorbar=dict(title="사고[건]"),width=1000,height=500)
                st.plotly_chart(fig_top)  # Plotly 차트를 Streamlit에 출력

                st.header('지역적 특징🔍')
                st.write("""가장 교통사고건수가 높은 지역으로는 경기-수원시 선정되었었다. 그다음으로는 충북-청주,서울-강남구순으로 지역이 선정되었다. """)
                st.write("""교통사고 빈도가 높은 지역은 일반적으로 다음과 같은 특징을 가짐
- **상업적 중심지**: 상업 활동이 활발한 도심 지역에서 교통사고가 많이 발생함.
- **교차로 밀집**: 많은 교차로와 신호등이 있는 지역은 사고가 자주 발생하는 경향이 있음.
- **교통량이 많은 지역**: 많은 차량이 오가는 곳에서 사고 발생률이 높음.
""")

    
    if option == "부문별 교통사고(최근5년)":
        def load_data():
            url = "https://raw.githubusercontent.com/saenan22/final_project/refs/heads/main/%EB%B6%80%EB%AC%B8%EB%B3%84%EC%82%AC%EA%B3%A0%EC%9C%A0%ED%98%95.csv"
            df_c = pd.read_csv(url, encoding="utf-8")
            return df_c
            
        df_c = load_data()

        # 최근 5년 데이터만 필터링
        recent_years = ['2019년', '2020년', '2021년', '2022년', '2023년']
        df_c_recent = df_c[['구분', '유형'] + recent_years]


        # 데이터를 Tidy format으로 변환
        tidy_df = pd.melt(df_c_recent, id_vars=["구분", "유형"], var_name="연도", value_name="건수")
        accident_types = ['사고(건)', '사망(건)', '부상(건)']
        tidy_df = tidy_df[tidy_df['유형'].isin(accident_types)]


        # Streamlit UI 구성
        st.subheader("📊 부문별 교통사고(최근 5년) 추세확인")

        # 필터링 섹션  
        st.subheader("⚙️ 필터 설정") 
        accident_category = st.selectbox("💥 사고 구분 선택", tidy_df['구분'].unique(), index=0)

        # 선택한 사고 구분에 맞는 데이터 필터링
        filtered_data = tidy_df[tidy_df['구분'] == accident_category]
        
        # Streamlit에서 열을 3개로 나누기
        col1, col2, col3 = st.columns(3)

    # 첫 번째 열 (사고(건) 그래프)
        with col1:
            accident_data = filtered_data[filtered_data['유형'] == '사고(건)']
            fig1 = px.bar(accident_data, x="연도", y="건수", title="전체 교통사고(건)",
                      labels={"연도": "연도", "건수": "교통사고 건수"})

            st.plotly_chart(fig1)

    # 두 번째 열 (사망(건) 그래프)
        with col2:
            death_data = filtered_data[filtered_data['유형'] == '사망(건)']
            fig2 = px.bar(death_data, x="연도", y="건수", title="사망 교통사고(건)",
                      labels={"연도": "연도", "건수": "교통사고 사망 건수"})
            fig2.update_traces(marker_color='red')
            st.plotly_chart(fig2)

    # 세 번째 열 (부상(건) 그래프)
        with col3:
            injury_data = filtered_data[filtered_data['유형'] == '부상(건)']
            fig3 = px.bar(injury_data, x="연도", y="건수", title="부상 교통사고(건)",
                      labels={"연도": "연도", "건수": "교통사고 부상 건수"})
            fig3.update_traces(marker_color='green')
            st.plotly_chart(fig3)

        # 데이터 확인
        if st.button("📋 데이터 미리보기"):
            st.dataframe(filtered_data)
            
        st.subheader("분석결과🔍")
        st.write("""최근5년간 교통사고 사건수, 사망자수, 부상자수의 동향을 분석한 결과, 전체적으로는 사고 발생 건수와 사망자 수, 부상자 수가 감소하는 추세를 보였으나 
        어린이와 노인 사고에서는 예외적으로 사건수가 약간 증가한 것으로 나타났습니다. """)
        st.write("""이는 특정 연령대에서의 교통사고 예방과 안전 강화에 대한 추가적인 노력이 필요함을 시사합니다. 
        이러한 경향은 사회적, 경제적으로 중요한 문제로, 취약 계층을 대상으로 한 보다 세밀한 교통사고 예방 대책과 교육이 요구된다는 점을 강조합니다.""")

    
    # 시간대별 교통사고 관련 CSV 데이터 불러오기 (URL에서 데이터 읽기)
    def load_data():
        url = "https://raw.githubusercontent.com/saenan22/final_project/refs/heads/main/2023%EB%85%84%20%EC%8B%9C%EA%B0%84%EB%8C%80%EB%B3%84%20%EA%B5%90%ED%86%B5%EC%82%AC%EA%B3%A0.csv"
        df_t = pd.read_csv(url, encoding="utf-8")
        return df_t
    df_t = load_data()
        

    # 시간대별 교통사고 분석
    if option == "시간대별 교통사고":
        st.header("2023년 기준 시간대별 교통사고 ")

    # 시간대 선택 슬라이더 추가
        start_hour, end_hour = st.slider(
        "보고싶은 시간대를 선택하세요 (24시간 기준)",
        min_value=0, max_value=24, value=(0, 24), step=2
    )

        # 선택된 시간대 데이터 필터링-> 2시간
        selected_data = df_t.iloc[start_hour // 2:end_hour // 2]

        # 세 개의 열 생성
        col1, col2, col3 = st.columns(3)

        # 사고(건) 그래프
        with col1:
            st.subheader("🚗사고 건수")
            fig_accidents = px.bar(
            selected_data,
            x="시간대",
            y="사고(건)",
            title="선택된 시간대 사고(건)",
            labels={"사고(건)": "사고 건수"})
            st.plotly_chart(fig_accidents, use_container_width=True)

    # 사망(명) 그래프
        with col2:
            st.subheader("☠️사망자")
            fig_deaths = px.bar(
            selected_data,
            x="시간대",
            y="사망(명)",
            title="선택된 시간대 사망(명)",
            labels={"사망(명)": "사망자 수"}
        )
            fig_deaths.update_traces(marker_color='lightcoral')  # 연한 그린 색상으로 설정
            st.plotly_chart(fig_deaths, use_container_width=True)

    # 부상(명) 그래프
        with col3:
            st.subheader("🤕 부상자")
            fig_injuries = px.bar(
            selected_data,
            x="시간대",
            y="부상(명)",
            title="선택된 시간대 부상(명)",
            labels={"부상(명)": "부상자 수"}
        )
            fig_injuries.update_traces(marker_color='lightgreen')  # 연한 그린 색상으로 설정
            st.plotly_chart(fig_injuries, use_container_width=True)

        st.subheader("분석결과🔍")
        st.write(""" 1. 시간대별 교통사고 사건 수에 대해 분석한 결과, 저녁 6시에서 8시 사이에 가장 높은 비율로 교통사고가 발생하는 경향을 확인할 수 있었습니다.""")
        st.write("""   이는 퇴근 시간과 맞물려 발생하는 교통 혼잡과 밀접한 연관이 있을 것으로 추측됩니다. 
        퇴근 시간대는 많은 사람들이 일상적인 이동을 하기 때문에 도로에 많은 차량이 집중되며, 이로 인해 사고 발생 가능성이 증가할 수 있습니다.
        또한, 피로감이나 집중력 저하와 같은 요인이 사고를 유발하는 주요 원인으로 작용할 수 있음을 시사합니다.   """)
        st.write("""이러한 분석은 특정 시간대에 집중적인 교통사고 예방을 위한 전략을 수립하는 데 중요한 기초 자료가 될 수 있습니다.""")


        st.write(""" 2. 시간대별 교통사고 부상자 수를 분석한 결과, 사건 수와 유사한 추세를 보임을 확인할 수 있었습니다. 
        부상자 수는 오후 4시에서 6시 사이에 가장 높은 비율을 차지하는 것으로 나타났습니다.   """)
        



    
    if option == "요일별 교통사고":
        def load_data():
            url = "https://raw.githubusercontent.com/saenan22/final_project/refs/heads/main/2023%EB%85%84%20%EC%9A%94%EC%9D%BC%EB%B3%84%20%EA%B5%90%ED%86%B5%EC%82%AC%EA%B3%A0.csv"
            df_y = pd.read_csv(url, encoding="utf-8")
            return df_y
        df_y = load_data()
        # 요일별 교통사고 데이터
        # Streamlit UI 구성
        st.title("2023년기준 요일별 교통사고 현황")

        # 데이터 확인
        st.subheader("📅 요일별 교통사고 데이터")
        st.dataframe(df_y)


        # 막대그래프 생성
        def create_bar_chart(df, column, title):
            fig = px.bar(df, x='요일', y=column, labels={'요일': '요일', column: title}, title=title)
            fig.update_layout(xaxis_title='요일', yaxis_title=title, xaxis_tickmode='array', xaxis_tickvals=[0, 1, 2, 3, 4, 5, 6], xaxis_ticktext=['일', '월', '화', '수', '목', '금', '토'])
            return fig


# 사고(건) 막대그래프 
        fig1 = create_bar_chart(df_y, '사고(건)', '🚗 사고(건) 요일별 분포')
        st.plotly_chart(fig1)

       # 사망(명) 막대그래프 
        fig2 = create_bar_chart(df_y, '사망(명)', '☠️ 사망(명) 요일별 분포')
        fig2.update_traces(marker_color='lightcoral')
        st.plotly_chart(fig2)

       # 부상(명) 막대그래프
        fig3 = create_bar_chart(df_y, '부상(명)', '🤕 부상(명) 요일별 분포')
        fig3.update_traces(marker_color='lightgreen')
        st.plotly_chart(fig3)

        st.subheader("분석결과🔍")
        st.write("""
요일별 교통사고 분석 결과, 모든 부문에서 금요일이 가장 높은 사고 비율을 보였습니다. 
이는 주말을 앞두고 사람들이 외출과 이동이 증가하는 경향과 관련이 있을 수 있습니다. """)
        st.write("""특히, 금요일의 '불금' 문화가 사회적 활동 및 음주를 촉진시켜 교통사고 발생률을 높이는 주요 요인으로 작용할 가능성이 큽니다.
따라서, 금요일에 대한 사고 예방을 위한 강화된 교통 안전 대책이 필요합니다.
""")





    

    if option == "월별 교통사고":
        def load_data():
            url = "https://raw.githubusercontent.com/saenan22/final_project/refs/heads/main/2023%EB%85%84%20%EC%9B%94%EB%B3%84%20%EA%B5%90%ED%86%B5%EC%82%AC%EA%B3%A0.csv"
            df_m = pd.read_csv(url, encoding="utf-8")
            return df_m
        df_m = load_data()

        st.title("📊 월별 교통사고 데이터 시각화")
        st.subheader("📅 월별 교통사고 데이터")
        st.dataframe(df_m)


    # 막대그래프 생성 함수
        def create_bar_chart(df, column, title):
            fig = px.bar(df, x='월', y=column, labels={'월': '월', column: title}, title=title)
            fig.update_layout(xaxis_title='월', yaxis_title=title, xaxis_tickmode='array', xaxis_tickvals=list(range(1, 13)))
            return fig

    # 사고(건) 시각화
        st.subheader("🚗 사고(건) 월별 분석")
        fig1_bar = create_bar_chart(df_m, '사고(건)', '사고(건) 월별 분포')
        st.plotly_chart(fig1_bar)

# 사망(건) 시각화
        st.subheader("☠️ 사망(건) 월별 분석")
        fig2_bar = create_bar_chart(df_m, '사망(명)', '사망(명) 월별 분포')
        fig2_bar.update_traces(marker_color='lightcoral') 
        st.plotly_chart(fig2_bar)

# 부상(건) 시각화
        st.subheader("🤕 부상(건) 월별 분석")
        fig3_bar = create_bar_chart(df_m, '부상(명)', '부상(명) 월별 분포')
        fig3_bar.update_traces(marker_color='lightgreen') 
        st.plotly_chart(fig3_bar)

        st.subheader("분석결과🔍")
        st.write("""월별 교통사고 수를 비교한 결과, 전반적으로 비슷한 경향을 보였지만, 8월에 사고 수가 가장 높았습니다.""")
        st.write("""이는 여러 가지 요인에 의해 설명될 수 있습니다.""")
        st.write("""우선, 8월은 여름철 휴가철로 많은 사람들이 여행을 떠나면서 교통량이 급증하는 시기입니다. 이에 따라 교통사고 발생 가능성이 높아질 수 있습니다.""")
        st.write("""또한, 여름철에는 장마나 폭우로 인한 도로 상황이 위험해지기 때문에 사고를 유발할 가능성도 큽니다. 
        장마와 홍수는 도로 미끄럼, 시야 부족, 침수된 도로 등 여러 가지 위험 요소를 동반하며, 이로 인해 사고가 증가할 수 있습니다.
        이러한 요인들이 결합되어 8월에 사고가 많이 발생하는 것으로 추정됩니다.""")
    


    
    if option == "사고유형별 교통사고":
        def load_data():
            url = "https://raw.githubusercontent.com/saenan22/final_project/refs/heads/main/2023%EB%85%84%20%EC%82%AC%EA%B3%A0%EC%9C%A0%ED%98%95%EB%B3%84%20%EA%B5%90%ED%86%B5%EC%82%AC%EA%B3%A0.csv"
            df_k = pd.read_csv(url, encoding="utf-8")
            return df_k
        df_k = load_data()
        df_k = df_k[df_k["사고유형"] != "계"]

        st.title("📊 사고 유형별 교통사고 통계")
        st.subheader("📅 사고 유형별 교통사고 데이터")
        st.dataframe(df_k)


        # 정제후 데이터 준비함함
        data = {
    '사고유형': ['차대사람', '차대차', '차량단독', '철길건널목'],
    '사고(건)': [36996, 152935, 8363, 2],
    '사망(명)': [859, 1041, 650, 1],
    '부상(명)': [38263, 236287, 9248, 1]
}

        df_k = pd.DataFrame(data)

# 각 사고유형에 대한 비중 계산 함수
        def calculate_percentage(df, column):
            total = df[column].sum()  # 전체 합계 구하기
            df[f'{column}_비중'] = (df[column] / total) * 100  # 각 값의 비중 계산
            return df

       # 사고(건) 비중 계산
        df_k = calculate_percentage(df_k, '사고(건)')
# 사망(명) 비중 계산
        df_k = calculate_percentage(df_k, '사망(명)')
# 부상(명) 비중 계산
        df_k = calculate_percentage(df_k, '부상(명)')

# 막대그래프 생성 함수
        def create_bar_chart(df, column, title):
            fig = px.bar(df, x='사고유형', y=f'{column}_비중', 
                 text=f'{column}_비중',  # 비중 텍스트 표시
                 labels={'사고유형': '사고 유형', f'{column}_비중': title},
                 title=title)
            fig.update_traces(texttemplate='%{text:.2f}%', textposition='inside')  # 비중 텍스트 내부 표시
            return fig

# 도넛차트 생성 함수
        def create_donut_chart(df, column, title):
            fig = px.pie(df, names='사고유형', values=column, title=title, hole=0.3)
            fig.update_traces(textinfo='label+percent',textposition='inside',insidetextorientation='radial', pull=[0.1, 0.1, 0.1, 0.1])  # 텍스트안쪽 배치함 및 퍼센트 표시
            return fig

# 사고(건) 막대그래프 및 도넛차트
        st.subheader("🚗 사고(건) 유형별 비중")
        col1, col2, col3 = st.columns(3)

        with col1:
            fig1_bar = create_bar_chart(df_k, '사고(건)', '사고(건) 유형별 비중')
            st.plotly_chart(fig1_bar, use_container_width=True)

        with col2:
            fig1_donut = create_donut_chart(df_k, '사고(건)', '사고(건) 유형별 비중 도넛차트')
            st.plotly_chart(fig1_donut, use_container_width=True)

     # 사망(명) 막대그래프 및 도넛차트
        st.subheader("☠️ 사망(명) 유형별 비중")
        col4, col5, col6 = st.columns(3)

        with col4:
            fig2_bar = create_bar_chart(df_k, '사망(명)', '사망(명) 유형별 비중')
            st.plotly_chart(fig2_bar, use_container_width=True)
        with col5:
            fig2_donut = create_donut_chart(df_k, '사망(명)', '사망(명) 유형별 비중 도넛차트')
            st.plotly_chart(fig2_donut, use_container_width=True)

# 부상(명) 막대그래프 및 도넛차트
        st.subheader("🤕 부상(명) 유형별 비중")
        col7, col8, col9 = st.columns(3)

        with col7:
            fig3_bar = create_bar_chart(df_k, '부상(명)', '부상(명) 유형별 비중')
            st.plotly_chart(fig3_bar, use_container_width=True)

        with col8:
            fig3_donut = create_donut_chart(df_k, '부상(명)', '부상(명) 유형별 비중 도넛차트')
            st.plotly_chart(fig3_donut, use_container_width=True)
        

        st.subheader("분석결과🔍")

        st.write("""사고유형별 교통사고 사건수를 분석한 결과 차대차 비율이 가장 높았으며 
        이는 교차로와 도로에서 차량 간 충돌이 주요 원인임을 시사합니다. 
        또한 운전자의 안전 거리 확보와 신호 준수 등의 안전 운전 습관 강화가 필요하며 도로 설계 개선과 같은 예방적 조치가 중요함을 시사한다.   """)
        st.write("""사고유형별 교통사고 사망자수를 분석한 결과 차대차 비율이 높았다.  """)
        st.write("""차대차 사고에서 가장 높은 사망률을 보인 것은 차량 간 충돌이 다른 사고 유형에 비해 더욱 치명적일 수 있음을 의미한다.
        이는 차량의 속도와 충돌 강도가 크기 때문에 사고 발생 시 사망자가 많다는 것을 시사하며, 
        이에 따라 차량 안전성 향상, 특히 충돌 완화 기술과 도로 설계 개선이 필요함을 강조한다.""")
        






# Page 3 내용
elif page == "Page 3":
    st.title("교통사고 예방 정보")
    
    # 선택할 수 있는 옵션 생성 (라디오 버튼)
    choice = st.radio("교통사고 예방법을 확인하세요:", 
                      ["기술적 측면", "사회적 측면", "개인적 측면"])
    
    # 기술적 측면 설명
    if choice == "기술적 측면":
        st.subheader("1. 기술적 측면")
        
        st.markdown("""
        **1-1. 🚗자동차 안전 기술🛡️**  
        자동차에 자동비상브레이크, 차선 이탈 경고, 후측방 경고 시스템 등 최신 안전 기술을 탑재하여 사고를 예방합니다. 
        이러한 기술들은 운전자의 실수나 부주의를 보완하고 사고를 미연에 방지할 수 있습니다.
        
        **1-2. 💻스마트 교통 시스템🚦**  
        지능형 교통 시스템(ITS)을 활용해 교통 흐름을 실시간으로 관리하고 사고 발생 가능성을 예측합니다. 교차로와 도로의 실시간 정보를 반영해 신호등 주기를 조정하거나 사고 다발 지역에 경고 시스템을 설치하여 사고를 예방할 수 있습니다.
        
        **1-3. 🚗차량 유지 관리🛠️**  
        자동차의 정기적인 점검과 유지 관리가 사고를 예방하는 데 중요한 역할을 합니다. 타이어, 브레이크, 조향 장치 등 차량의 주요 부품을 정기적으로 점검하고, 고장이 발생하지 않도록 관리해야 합니다.
        """)
    
    # 사회적 측면 설명
    elif choice == "사회적 측면":
        st.subheader("2. 사회적 측면 (제도 및 정책)")
        
        st.markdown("""
        **2-1. 교통 법규 강화⚖️**  
        교통 법규를 강화하고 음주운전, 과속 등 불법 운전 행위를 철저히 단속합니다. 사고 다발 지역에 대한 집중 개선 작업을 통해 사고를 줄일 수 있으며, 법적 처벌을 통해 운전자의 경각심을 높입니다.
        
        **2-2. 🚦교통 안전 교육 및 캠페인🏫**  
        대중의 교통 안전 의식을 높이기 위한 교육과 캠페인이 필요합니다. 특히 어린이, 노인 등을 대상으로 한 교통 안전 교육은 사고 예방에 효과적이며, 교통사고에 대한 경각심을 고취시킬 수 있습니다.
        
        **2-3. 사고 다발 지역 개선🚗💥**  
        사고가 빈번하게 발생하는 지역에 대해 교차로 개선, 속도 제한 조정, 신호 시스템 강화 등 구체적인 대책을 수립하고 실행합니다. 또한, 교차로 및 보행로에 대한 안전 점검을 강화하여 사고를 미연에 방지합니다.
        """)

    # 개인적 측면 설명
    else:
        st.subheader("3. 개인적 측면")
        
        st.markdown("""
        **3-1. ⚠️운전자의 안전 의식⚠✋**  
        운전자는 과속과 음주운전, 스마트폰 사용을 자제하고, 안전운전 습관을 기르는 것이 중요합니다. 특히 피로운전, 불법 주정차, 주정차된 차량을 피하기 위한 주의 깊은 운전이 사고를 예방하는 데 큰 역할을 합니다.
        
        **3-2. 보행자 및 자전거 이용자 안전🚥🚶‍♀️**  
        보행자는 신호를 준수하고 도로를 횡단할 때 주의를 기울여야 하며, 자전거 이용자는 헬멧을 착용하고 안전하게 주행해야 합니다. 특히 도로에서의 안전한 주행을 위해 자전거 도로와 보행자 보호구역의 중요성이 강조됩니다.
        
        **3-3. 🚗안전 장비 착용🪢**  
        모든 운전자는 차량에 탑승할 때 안전벨트를 착용하고, 자전거 이용자는 헬멧과 보호 장비를 착용해야 합니다. 이는 사고 발생 시 부상을 줄이는 중요한 방법입니다.
        """)










