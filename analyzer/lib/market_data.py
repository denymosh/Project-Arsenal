"""
研报分析系统 - 市场数据拉取模块

使用yfinance获取股票实时/历史数据，用于验证研报预测。
"""

from typing import Optional
from datetime import datetime, timedelta

try:
    import yfinance as yf
except ImportError:
    yf = None
    print("⚠️ yfinance未安装，市场数据功能不可用。请运行: uv add yfinance")


def get_current_price(ticker: str) -> Optional[float]:
    """获取标的当前价格"""
    if yf is None:
        return None
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return info.get("currentPrice") or info.get("regularMarketPrice")
    except Exception as e:
        print(f"  ⚠️ 获取{ticker}价格失败: {e}")
        return None


def get_price_on_date(ticker: str, target_date: str) -> Optional[float]:
    """获取标的在指定日期的收盘价"""
    if yf is None:
        return None
    try:
        stock = yf.Ticker(ticker)
        dt = datetime.strptime(target_date, "%Y-%m-%d")
        start = dt - timedelta(days=5)  # 往前多取几天防止节假日
        end = dt + timedelta(days=1)
        hist = stock.history(start=start.strftime("%Y-%m-%d"), end=end.strftime("%Y-%m-%d"))
        if not hist.empty:
            return float(hist["Close"].iloc[-1])
        return None
    except Exception as e:
        print(f"  ⚠️ 获取{ticker}在{target_date}的价格失败: {e}")
        return None


def get_market_summary(ticker: str) -> dict:
    """
    获取标的的市场数据摘要

    返回:
        包含当前价格、市值、PE等信息的字典
    """
    if yf is None:
        return {"error": "yfinance未安装"}
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            "current_price": info.get("currentPrice") or info.get("regularMarketPrice"),
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE"),
            "forward_pe": info.get("forwardPE"),
            "52w_high": info.get("fiftyTwoWeekHigh"),
            "52w_low": info.get("fiftyTwoWeekLow"),
            "avg_volume": info.get("averageVolume"),
            "beta": info.get("beta"),
        }
    except Exception as e:
        print(f"  ⚠️ 获取{ticker}市场摘要失败: {e}")
        return {"error": str(e)}


def get_price_change(ticker: str, days: int = 30) -> Optional[dict]:
    """
    获取标的在指定天数内的价格变化

    返回:
        包含起始价、当前价、涨跌幅的字典
    """
    if yf is None:
        return None
    try:
        stock = yf.Ticker(ticker)
        end = datetime.now()
        start = end - timedelta(days=days)
        hist = stock.history(start=start.strftime("%Y-%m-%d"), end=end.strftime("%Y-%m-%d"))
        if len(hist) >= 2:
            start_price = float(hist["Close"].iloc[0])
            end_price = float(hist["Close"].iloc[-1])
            change_pct = (end_price - start_price) / start_price * 100
            return {
                "start_price": round(start_price, 2),
                "end_price": round(end_price, 2),
                "change_pct": round(change_pct, 2),
                "period_days": days
            }
        return None
    except Exception as e:
        print(f"  ⚠️ 获取{ticker}价格变化失败: {e}")
        return None
