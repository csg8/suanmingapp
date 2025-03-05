import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
from lunar_python import Lunar
from utils.bazi_calculator import calculate_bazi, get_five_elements
from utils.zodiac_utils import get_zodiac_sign, get_zodiac_compatibility
from utils.name_analysis import analyze_name
from utils.daily_fortune import DailyFortune
import time
import numpy as np
import random

# Corrected imports
from utils.tarot import TarotReader
from utils.lunar_festival import LunarFestival

# Page config
st.set_page_config(
    page_title="中国传统命理分析",
    page_icon="🏮",
    layout="wide"
)

# Custom CSS
with open('styles/custom.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Background image
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("https://images.unsplash.com/photo-1518170083561-dfe8df27dc61");
        background-size: cover;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.title("🏮 中国传统命理分析")

# 获取每日运势
daily_fortune = DailyFortune.get_daily_fortune()

# 显示每日运势卡片
with st.container():
    st.subheader("📅 今日运势")
    cols = st.columns(4)

    # 运势等级对应的emoji
    fortune_emojis = {"大吉": "🌟", "吉": "⭐", "平": "⚪", "凶": "⚠️", "大凶": "❌"}

    with cols[0]:
        st.metric("总运势", f"{fortune_emojis[daily_fortune['overall']]} {daily_fortune['overall']}")
    with cols[1]:
        st.metric("感情运", f"{fortune_emojis[daily_fortune['love']]} {daily_fortune['love']}")
    with cols[2]:
        st.metric("事业运", f"{fortune_emojis[daily_fortune['career']]} {daily_fortune['career']}")
    with cols[3]:
        st.metric("财运", f"{fortune_emojis[daily_fortune['wealth']]} {daily_fortune['wealth']}")

# 生成运势趋势图
dates = pd.date_range(start=datetime.now(), periods=7, freq='D')
fortune_levels = {"大吉": 5, "吉": 4, "平": 3, "凶": 2, "大凶": 1}

# 生成随机运势数据
fortune_data = {
    "日期": dates,
    "总运势": [random.choice(list(fortune_levels.keys())) for _ in range(7)],
    "感情运": [random.choice(list(fortune_levels.keys())) for _ in range(7)],
    "事业运": [random.choice(list(fortune_levels.keys())) for _ in range(7)],
    "财运": [random.choice(list(fortune_levels.keys())) for _ in range(7)]
}

df = pd.DataFrame(fortune_data)

# 转换运势等级为数值
for col in ["总运势", "感情运", "事业运", "财运"]:
    df[f"{col}_值"] = df[col].map(fortune_levels)

# 创建运势趋势图
st.subheader("📈 七日运势趋势")
fig = go.Figure()

for col in ["总运势", "感情运", "事业运", "财运"]:
    fig.add_trace(go.Scatter(
        x=df["日期"],
        y=df[f"{col}_值"],
        name=col,
        mode='lines+markers',
        hovertemplate=col + ": %{text}<br>日期: %{x|%Y-%m-%d}<extra></extra>",
        text=df[col]
    ))

fig.update_layout(
    xaxis_title="日期",
    yaxis_title="运势指数",
    hovermode="x unified",
    yaxis=dict(
        ticktext=list(fortune_levels.keys()),
        tickvals=list(fortune_levels.values()),
        range=[0.5, 5.5]
    )
)

st.plotly_chart(fig, use_container_width=True)

# 显示吉凶提示
st.markdown("### 📝 今日提示")
for tip in daily_fortune['tips']:
    st.info(tip)

# 显示幸运信息
cols = st.columns(3)
with cols[0]:
    st.write("🎨 幸运颜色：", "、".join(DailyFortune.get_lucky_colors()))
with cols[1]:
    st.write("🔢 幸运数字：", "、".join(map(str, DailyFortune.get_lucky_numbers())))
with cols[2]:
    st.write("🧭 吉利方位：", "、".join(DailyFortune.get_lucky_directions()))

# 显示智慧语录和情感语录
st.markdown("### 📖 今日箴言")
st.success(daily_fortune['wisdom'])
st.markdown("### 💝 情感语录")
st.success(daily_fortune['love_quote'])

# Sidebar
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1517471305133-eebd52130784", width=300)
    analysis_type = st.selectbox(
        "选择分析类型",
        ["八字分析", "生肖运势", "姓名学分析", "紫薇斗数", "塔罗牌占卜", "节日运势"]
    )
    try:
        with open('assets/celestial_compass.svg', encoding="utf-8") as f:
            compass_svg = f.read()
        st.markdown(f'<div style="text-align: center;">{compass_svg}</div>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("Error: celestial_compass.svg not found in assets folder.")

# Main content
if analysis_type == "八字分析":
    st.header("八字分析")

    col1, col2 = st.columns(2)
    with col1:
        birth_date = st.date_input(
            "选择出生日期",
            min_value=datetime(1900, 1, 1),
            max_value=datetime.now(),
            value=datetime.now()
        )
        birth_time = st.time_input("选择出生时间", datetime.now().time())

    with col2:
        gender = st.radio("性别", ["男", "女"])

    if st.button("开始分析", key="bazi_analysis"):
        with st.spinner("正在计算八字..."):
            # 将日期和时间合并为datetime对象
            birth_datetime = datetime.combine(birth_date, birth_time)

            # Calculate lunar date
            lunar = Lunar.fromDate(birth_datetime)

            # Get BaZi
            bazi_result = calculate_bazi(birth_date, birth_time, gender)
            five_elements = get_five_elements(bazi_result)

            # Display results
            st.success("分析完成！")

            # Display BaZi chart
            st.subheader("八字排盘")
            st.write(f"农历: {lunar.getYearInChinese()}年{lunar.getMonthInChinese()}月{lunar.getDayInChinese()}")
            st.write(f"八字: {bazi_result}")

            # Five Elements Chart
            five_elements_df = pd.DataFrame(five_elements.items(), columns=['Element', 'Value'])
            fig = px.pie(five_elements_df, values='Value', names='Element', title='五行分布')
            st.plotly_chart(fig)

elif analysis_type == "生肖运势":
    st.header("生肖运势分析")

    birth_year = st.number_input("出生年份", min_value=1900, max_value=2100, value=2000)

    if st.button("查看运势", key="zodiac_analysis"):
        with st.spinner("正在分析生肖运势..."):
            zodiac_sign = get_zodiac_sign(birth_year)
            compatibility = get_zodiac_compatibility(zodiac_sign)

            # Display results
            st.success("分析完成！")

            col1, col2 = st.columns(2)
            with col1:
                st.subheader(f"你的生肖: {zodiac_sign}")
                st.image(f"https://images.unsplash.com/photo-1517327832109-76f52a6c5eab", width=200)

            with col2:
                st.subheader("相配生肖")
                for animal, score in compatibility.items():
                    st.write(f"{animal}: {'⭐' * score}")

elif analysis_type == "姓名学分析":
    st.header("姓名学分析")

    name = st.text_input("输入姓名（简体中文）")

    if st.button("分析姓名", key="name_analysis"):
        if len(name) < 2:
            st.error("请输入完整姓名")
        else:
            with st.spinner("正在分析姓名..."):
                name_analysis = analyze_name(name)

                st.success("分析完成！")

                # 展示五行分析
                st.subheader("姓名五行分析")

                # 创建五行分布图
                element_data = name_analysis['element_analysis']
                elements_df = pd.DataFrame([
                    {"Element": element, "Count": data["count"], "Percentage": data["percentage"]}
                    for element, data in element_data.items()
                ])

                fig1 = px.pie(
                    elements_df,
                    values='Percentage',
                    names='Element',
                    title='五行分布',
                    color='Element',
                    color_discrete_map={
                        "木": "#4CAF50",
                        "火": "#FF5722",
                        "土": "#795548",
                        "金": "#9E9E9E",
                        "水": "#2196F3"
                    }
                )
                st.plotly_chart(fig1)

                # 显示笔画分析
                st.subheader("笔画分析")
                strokes_data = pd.DataFrame(name_analysis['strokes'].items(), columns=['Character', 'Strokes'])
                fig2 = go.Figure(data=[
                    go.Bar(
                        name='笔画',
                        x=strokes_data['Character'],
                        y=strokes_data['Strokes'],
                        text=strokes_data['Strokes'],
                        textposition='auto',
                    )
                ])
                fig2.update_layout(title='姓名笔画分布')
                st.plotly_chart(fig2)

                # 显示总评
                st.subheader("姓名总评")
                st.write(f"总分: {name_analysis['overall_score']}分")
                st.write(name_analysis['description'])

elif analysis_type == "紫薇斗数":
    st.header("🏮 紫薇斗数命盘分析")

    col1, col2 = st.columns(2)
    with col1:
        birth_date = st.date_input(
            "选择出生日期",
            min_value=datetime(1900, 1, 1),
            max_value=datetime.now(),
            value=datetime.now()
        )
        birth_time = st.time_input("选择出生时间", datetime.now().time())

    with col2:
        gender = st.radio("性别", ["男", "女"])

    if st.button("生成命盘", key="ziwei_analysis"):
        with st.spinner("正在生成紫薇斗数命盘..."):
            # 创建命盘实例
            birth_datetime = datetime.combine(birth_date, birth_time)
            ziwei = ZiWeiCalculator(birth_datetime, gender)
            chart_data = ziwei.generate_chart_data()

            # 显示命盘
            st.subheader("📜 命盘显示")
            try:
                with open('assets/ziwei_chart.svg') as f:
                    ziwei_svg = f.read()
                st.markdown(f'<div style="text-align: center;">{ziwei_svg}</div>', unsafe_allow_html=True)
            except FileNotFoundError:
                st.error("Error: ziwei_chart.svg not found in assets folder.")

            # 显示运势分析
            st.subheader("🔮 命盘解读")

            # 使用expander显示主星分布
            with st.expander("查看主星分布详情", expanded=True):
                cols = st.columns(4)
                main_stars = chart_data["main_stars"]
                for i, (star, position) in enumerate(main_stars.items()):
                    with cols[i % 4]:
                        st.markdown(f"""
                        <div style='padding: 10px; border-radius: 5px; border: 1px solid #CD0000; margin: 5px; text-align: center;'>
                            <div style='color: #CD0000; font-weight: bold;'>{star}</div>
                            <div>{position}宫</div>
                        </div>
                        """, unsafe_allow_html=True)

            # 显示宫位预测
            st.subheader("🎴 宫位详解")
            predictions = chart_data["predictions"]

            # 使用三列布局展示预测结果
            for i in range(0, len(predictions), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(predictions):
                        palace, prediction = list(predictions.items())[i + j]
                        with cols[j]:
                            st.markdown(f"""
                            <div style='padding: 15px; border-radius: 10px; background-color: rgba(255,245,238,0.9); margin: 5px;'>
                                <h4 style='color: #CD0000; margin: 0;'>{palace}</h4>
                                <p style='margin: 5px 0;'>{prediction}</p>
                            </div>
                            """, unsafe_allow_html=True)

            # 显示出生信息
            birth_info = chart_data["birth_info"]
            st.markdown("---")
            st.markdown(f"""
            <div style='text-align: center; padding: 10px;'>
                <p>农历 {birth_info['year']}年 {birth_info['month']}月 {birth_info['day']}日 {birth_info['hour']}时</p>
                <p style='color: #666;'>本命盘仅供参考，不作为人生决策依据</p>
            </div>
            """, unsafe_allow_html=True)

elif analysis_type == "塔罗牌占卜":
    st.header("🎴 塔罗牌占卜")

    # 选择牌阵
    spread_type = st.radio(
        "选择牌阵",
        ["三张牌阵（过去-现在-未来）", "五张牌阵（完整解读）"]
    )

    num_cards = 5 if "五张" in spread_type else 3

    if st.button("开始占卜", key="tarot_reading"):
        with st.spinner("正在抽取塔罗牌..."):
            # 抽牌并解读
            cards = TarotReader.draw_cards(num_cards)
            interpretation = TarotReader.interpret_reading(cards)
            summary = TarotReader.get_reading_summary(cards)

            # 显示结果
            st.subheader("🔮 塔罗牌阵解读")

            # 使用列显示每张牌
            cols = st.columns(num_cards)
            for i, (card, col) in enumerate(zip(cards, cols)):
                with col:
                    st.markdown(f"""
                    <div style='padding: 15px; border-radius: 10px; background-color: rgba(255,245,238,0.9); text-align: center;'>
                        <h4 style='color: #CD0000;'>{card['position']}</h4>
                        <h3>{card['name']}</h3>
                        <p>{'逆位' if card['reversed'] else '正位'}</p>
                    </div>
                    """, unsafe_allow_html=True)

            # 显示详细解读
            st.markdown("### 详细解读")
            st.markdown(interpretation)

            # 显示总体建议
            st.markdown("### 总体启示")
            st.info(summary['overall_tendency'])
            st.success(summary['suggestion'])

elif analysis_type == "节日运势":
    st.header("🏮 农历节日运势")

    # 获取当前节日信息
    current_festival = LunarFestival.get_current_festival()

    if current_festival:
        st.subheader(f"近期节日：{current_festival['name']}")
        st.write(f"距离节日还有 {current_festival['days_until']} 天")
        st.write(current_festival['info']['description'])

        if st.button("查看节日运势", key="festival_fortune"):
            with st.spinner("正在解读节日运势..."):
                fortune = LunarFestival.get_festival_fortune(current_festival['name'])

                # 显示运势
                st.markdown("### 节日运势解读")
                st.markdown(f"""
                <div style='padding: 20px; border-radius: 10px; background-color: rgba(255,245,238,0.9);'>
                    <h4 style='color: #CD0000;'>总体运势：{fortune['overall']}</h4>
                    <p style='font-size: 1.2em;'>{fortune['fortune']}</p>
                </div>
                """, unsafe_allow_html=True)

                # 显示建议
                st.subheader("🎋 节日指引")
                for suggestion in fortune['suggestions']:
                    st.info(suggestion)


# Footer
st.markdown("---")
st.markdown("📜 本分析仅供娱乐参考，不作为人生决策依据")