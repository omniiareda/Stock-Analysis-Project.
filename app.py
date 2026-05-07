import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# إعداد الصفحة (UI Developer Task)
st.set_page_config(page_title="Stock Analysis", layout="wide")
st.title('📈 نظام تحليل بيانات البورصة')

# القائمة الجانبية (Sidebar)
st.sidebar.header("إعدادات البحث")
symbol = st.sidebar.text_input('اكتبي رمز السهم:', 'AAPL')
period = st.sidebar.selectbox('اختر الفترة الزمنية:', ['1mo', '3mo', '6mo', '1y'])

if symbol:
    try:
        # جلب البيانات (Backend Developer Task)
        stock = yf.Ticker(symbol)
        df = stock.history(period=period)
        info = stock.info

        # عرض اسم الشركة والسعر الحالي
        st.header(f"شركة: {info.get('longName', symbol)}")
        
        # توزيع البيانات في أعمدة (UI Developer Task)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("السعر الحالي", f"${df['Close'].iloc[-1]:.2f}")
        col2.metric("أعلى سعر اليوم", f"${df['High'].iloc[-1]:.2f}")
        col3.metric("أقل سعر اليوم", f"${df['Low'].iloc[-1]:.2f}")
        col4.metric("حجم التداول", f"{df['Volume'].iloc[-1]:,}")

        # رسم بياني تفاعلي (Visualization Task)
        st.subheader("تحركات السهم")
        fig = go.Figure(data=[go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Price')])
        fig.update_layout(template="plotly_dark", xaxis_title="التاريخ", yaxis_title="السعر")
        st.plotly_chart(fig, use_container_width=True)

        # عرض البيانات التاريخية (Data Analyst Task)
        st.subheader("جدول البيانات التاريخية (آخر 7 أيام)")
        st.write(df.tail(7))

    except Exception as e:
        st.error("خطأ: تأكدي من كتابة رمز السهم بشكل صحيح (مثل AAPL أو MSFT)")
    