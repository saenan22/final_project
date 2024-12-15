import streamlit as st
import folium
import geopandas as gpd
import pandas as pd
import json
from streamlit_folium import st_folium
import plotly.express as px


# Sidebar 메뉴 생성
st.sidebar.title("교통사고 대시보드🚗💥")


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
    st.title('OECD국가별 교통사고 현황')
    st.subheader("2021년도 기준 OECD국가별 자동차1만대당 사망 현황🗺️")

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
    st.write("""그러나 가장높은 교통사고지역을 확인할수있음.""")

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

    

    # Streamlit 앱 설정
    st.title('OECD 국가🌍 교통사고 현황🚨')

    st.subheader("선택된 국가에 따른 교통사고 통계")

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


    st.subheader("2023년도 기준 대한민국의 교통사고수,사망수,부상자수가 서울,경기도 쪽에서 현저히 높음을 확인할수있다.")


    

   # 사고 빈도가 높은 국가 Top 10 버튼
    st.write("버튼을 눌러주세요👆")
    if st.button("자동차1만대당 사망수가 높은 국가 Top 10"):
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
        st.write("2021년기준 OECD국가중 자동차1만대당 사망수가 가장 높은국가는 콜롬비아로 확인핤우있다. ")

    # 사고 빈도가 낮은 국가 Top 10 버튼
    st.write("버튼을 눌러주세요👆")
    if st.button("자동차1만대당 사망수가 낮은 국가 Top 10"):
        top_low_freq = df0_cleaned.nsmallest(10, "자동차1만대당 사망(명)")
        top_low_freq['순위'] = range(1, len(top_low_freq) + 1)
        top_low_freq = top_low_freq.reset_index(drop=True)
        top_low_freq = top_low_freq[['국가', '사고(건)', '사망(명)', '자동차1만대당 사망(명)']]
        st.subheader("사고 빈도가 낮은 국가 Top 10")
        st.write(top_low_freq)

        # 그래프 생성
        fig_low = px.bar(top_low_freq, x="국가", y="자동차1만대당 사망(명)", 
                     title="자동차1만대당 사망수가 낮은 국가 Top 10", 
                     labels={"자동차1만대당 사망(명)": "자동차1만대당 사망(명)"})

        # 범례 
        fig_low.update_layout(
        showlegend=True,  # 범례 표시
        width=1600,       # 그래프 너비
        height=600        # 그래프 높이
    )
        st.plotly_chart(fig_low)








# Page 2 내용
elif page == "Page 2":
    st.title("대한민국 교통사고 분석")
      # 사이드바 옵션 추가
    st.sidebar.title("교통사고 분석")
    option = st.sidebar.selectbox(
        "분석 항목 선택",
        ["시도및 시군구별 교통사고","부문별 교통사고(최근5년)","시간대별 교통사고", "요일별 교통사고","사고유형별 교통사고","월별 교통사고"]
    )
    if option == "시도및 시군구별 교통사고":
        # 교통사고 데이터 불러오기
        file_path = r"https://raw.githubusercontent.com/saenan22/final_project/main/Report.csv"
        df = pd.read_csv(file_path, header=3)
        # GeoJSON 파일 URL
        geojson_url = "https://raw.githubusercontent.com/saenan22/final_project/main/BND_SIGUNGU_PG.json"

        # GeoJSON 읽기
        geojson_data = gpd.read_file(geojson_url)

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

    # 막대그래프 생성
        fig = px.bar(grouped_data, x="시도", y="사고[건]", title="2023년 기준 시도및 시군구별 사고 건수", labels={"사고[건]": "사고 건수"})

    # 그래프 표시
        st.plotly_chart(fig, key="unique_plot_key")



    # 필터링된 데이터에 대한 차트 출력2
        st.subheader("선택된 지역에 따른 사망 통계")

        grouped_data = df_filtered.groupby("시도")["사망[명]"].sum().reset_index()

    # 막대그래프 생성
        fig = px.bar(grouped_data, x="시도", y="사망[명]", title="2023년 기준 시도및 시군구별 사망 수", labels={"사망[명]": "명"},color_discrete_sequence=["#FFCDD2"])

    # 그래프 표시
        st.plotly_chart(fig, key="deaths_plot_key")


    # 필터링된 데이터에 대한 차트 출력3
        st.subheader("선택된 지역에 따른 부상 통계")

        grouped_data = df_filtered.groupby("시도")["부상[명]"].sum().reset_index()

    # 막대그래프 생성
        fig = px.bar(grouped_data, x="시도", y="부상[명]", title="2023년 기준 시도및 시군구별 부상 수", labels={"부상[명]": "명"},color_discrete_sequence=["#81C784"])

    # 그래프 표시
        st.plotly_chart(fig, key="injuries_plot_key")

    #데이터프레임형태로 나타냄 
        st.subheader("선택된 지역에 대한 교통사고 통계")
        st.write(df_filtered)

    # 제목선정
        st.title("지역별 교통사고 빈도")

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
                st.write("""교통사고 빈도가 높은 지역은 일반적으로 다음과 같은 특징을 가짐
- **상업적 중심지**: 상업 활동이 활발한 도심 지역에서 교통사고가 많이 발생함.
- **교차로 밀집**: 많은 교차로와 신호등이 있는 지역은 사고가 자주 발생하는 경향이 있음.
- **교통량이 많은 지역**: 많은 차량이 오가는 곳에서 사고 발생률이 높음.
""")
                




    # 시간대별 교통사고 관련 CSV 데이터 불러오기 (URL에서 데이터 읽기)
    def load_data():
        url = "https://raw.githubusercontent.com/saenan22/final_project/refs/heads/main/2023%EB%85%84%20%EC%8B%9C%EA%B0%84%EB%8C%80%EB%B3%84%20%EA%B5%90%ED%86%B5%EC%82%AC%EA%B3%A0.csv"
        df_t = pd.read_csv(url, encoding="utf-8")
        return df_t
    df_t = load_data()
        

    # 시간대별 교통사고 분석
    if option == "시간대별 교통사고":
        st.header("시간대별 교통사고 현황")

    # 시간대 선택 슬라이더 추가
        start_hour, end_hour = st.slider(
        "시간대를 선택하세요 (24시간 기준)",
        min_value=0, max_value=24, value=(0, 24), step=2
    )

        # 선택된 시간대 데이터 필터링
        selected_data = df_t.iloc[start_hour // 2:end_hour // 2]

        # 세 개의 열 생성
        col1, col2, col3 = st.columns(3)

        # 사고(건) 그래프
        with col1:
            st.subheader("사고(건)")
            fig_accidents = px.bar(
            selected_data,
            x="시간대",
            y="사고(건)",
            title="선택된 시간대 사고(건)",
            labels={"사고(건)": "사고 건수"})
            st.plotly_chart(fig_accidents, use_container_width=True)

    # 사망(명) 그래프
        with col2:
            st.subheader("사망(명)")
            fig_deaths = px.bar(
            selected_data,
            x="시간대",
            y="사망(명)",
            title="선택된 시간대 사망(명)",
            labels={"사망(명)": "사망자 수"}
        )
            st.plotly_chart(fig_deaths, use_container_width=True)

    # 부상(명) 그래프
        with col3:
            st.subheader("부상(명)")
            fig_injuries = px.bar(
            selected_data,
            x="시간대",
            y="부상(명)",
            title="선택된 시간대 부상(명)",
            labels={"부상(명)": "부상자 수"}
        )
            st.plotly_chart(fig_injuries, use_container_width=True)





    


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














