# Roshan Gann SSL Indicator - TradingView Pine Script

## Overview

This is a complete **Pine Script conversion** of the popular **Roshan Gann SSL** indicator from MetaTrader 4 to TradingView. It combines the power of SSL Channel with Gann Hi-Lo Activator methodology for trend detection and trading signals.

## Features

- ✅ **SSL Channel + Gann Hi-Lo Activator** - Powerful trend-following system
- ✅ **Multi-Timeframe Analysis** - Analyze higher timeframes without switching charts
- ✅ **Customizable Parameters** - Period, MA type, colors, and visual settings
- ✅ **Entry Signals** - Clear buy/sell arrows and labels
- ✅ **Alert System** - Get notified on trend changes and signals
- ✅ **No Repaint** - Reliable signals that don't change after candle close
- ✅ **Info Table** - Display current settings and trend on chart

## Quick Start

### Installation

1. Copy the code from `Roshan_Gann_SSL_TF.pine`
2. Open TradingView Pine Editor
3. Paste the code
4. Click "Add to Chart"

### Basic Settings

| Parameter | Default | Description |
|-----------|---------|-------------|
| SSL Period | 10 | Period for moving average calculation |
| Timeframe Shift | 0 | Higher timeframe analysis (0=current, 1=next TF, etc.) |
| MA Type | SMA | Type of moving average (SMA/EMA/WMA/HMA) |

## How It Works

### SSL Channel Logic

The indicator calculates two moving averages:
- One on **High** prices
- One on **Low** prices

### Trend Detection (Gann Hi-Lo Activator)

- **Bullish Trend**: When price closes above the high MA
- **Bearish Trend**: When price closes below the low MA

The lines "flip" based on price position, creating a channel that follows the trend.

## Timeframe System

The **Timeframe Shift** parameter allows you to analyze higher timeframes:

```
Shift 0: Current timeframe
Shift 1: One step up (1m → 5m, 5m → 15m, etc.)
Shift 2: Two steps up (1m → 15m, 5m → 30m, etc.)
Shift 3: Three steps up (1m → 30m, 5m → 1h, etc.)
```

**Timeframe Ladder:**
```
1min → 5min → 15min → 30min → 1hour → 4hours → 1day → 1week → 1month
```

## Trading Signals

### 🟢 Buy Signal
- Price crosses above the upper SSL line
- Lines turn green
- Green arrow appears below candle
- "BUY" label displayed

### 🔴 Sell Signal
- Price crosses below the lower SSL line
- Lines turn red
- Red arrow appears above candle
- "SELL" label displayed

## Trading Strategies

### Strategy 1: Trend Following
1. Wait for a clear trend (green or red)
2. Enter on pullbacks to the SSL lines
3. Exit when trend changes (opposite color signal)

### Strategy 2: Multi-Timeframe Confirmation
1. Add two instances of the indicator:
   - Instance 1: Timeframe Shift = 0 (entry signals)
   - Instance 2: Timeframe Shift = 2 (trend filter)
2. Only take trades when both agree on direction

### Strategy 3: SSL + RSI
Filter signals with RSI:
- Buy: SSL Buy + RSI < 30 = Strong Buy
- Sell: SSL Sell + RSI > 70 = Strong Sell

## Alert Configuration

The indicator includes three alert types:

1. **Buy Signal** - Triggers on bullish reversal
2. **Sell Signal** - Triggers on bearish reversal
3. **Trend Change** - Triggers on any trend change

### Setting Up Alerts:
1. Right-click on the indicator
2. Select "Add Alert"
3. Choose your preferred alert condition
4. Configure notification settings
5. Click "Create"

## Parameters Guide

### Core Settings

**SSL Period**
- Lower values (5-8): More signals, faster response, more noise
- Medium values (10-14): Balanced approach
- Higher values (20-25): Fewer signals, smoother trend

**MA Type Selection**
- **SMA**: Simple, good for beginners
- **EMA**: Faster response, better for volatile markets
- **WMA**: Weighted average
- **HMA**: Least lag, most responsive

### Visual Settings

- **Show Entry Signals**: Display arrows on chart
- **Show Trend Labels**: Display BUY/SELL text labels
- **Line Width**: Thickness of SSL lines (1-5)
- **Show Background Color**: Color the chart background based on trend
- **Show Info Table**: Display settings and current trend

### Color Settings

Customize colors for:
- Bull trend lines
- Bear trend lines
- Channel fill (bull)
- Channel fill (bear)

## Risk Management

### Stop Loss Placement
- **Long positions**: Below the lower SSL line
- **Short positions**: Above the upper SSL line

### Position Sizing
- Use 1-2% risk per trade
- Calculate position size based on stop loss distance

### Take Profit
- Use minimum 1:2 risk-to-reward ratio
- Consider trailing stop along SSL lines

## Performance Optimization

### For Different Markets

**Forex:**
- SSL Period: 10-14
- MA Type: EMA
- Timeframe Shift: 1-2

**Crypto:**
- SSL Period: 14-20
- MA Type: EMA or HMA
- Timeframe Shift: 1-2

**Stocks:**
- SSL Period: 10-15
- MA Type: SMA
- Timeframe Shift: 2-3

### For Different Trading Styles

**Scalping (1-5 min)**
- SSL Period: 5-8
- Timeframe Shift: 0-1

**Day Trading (15min-1h)**
- SSL Period: 10-14
- Timeframe Shift: 1-2

**Swing Trading (4h-1D)**
- SSL Period: 14-20
- Timeframe Shift: 2-3

## Common Issues & Solutions

### Issue: Too many signals
**Solution:** Increase SSL Period or use higher timeframe shift

### Issue: Signals are too late
**Solution:** Decrease SSL Period or switch to EMA/HMA

### Issue: Many false signals
**Solution:**
- Use higher timeframe for trend filter
- Combine with other indicators (RSI, MACD)
- Trade only in strong trending markets

## Differences from MT4 Version

This Pine Script version includes improvements:

1. ✅ Better interface and parameter organization
2. ✅ More customization options
3. ✅ Info table showing current settings
4. ✅ Advanced alert system
5. ✅ Background coloring option
6. ✅ Fill between lines for better visualization

## Technical Details

### Algorithm
1. Calculate MA of High and Low prices
2. Apply Gann Hi-Lo logic for trend detection
3. Flip lines based on price position relative to MAs
4. Generate signals on trend changes

### Pine Script Version
- Version 5 (latest)
- Compatible with all TradingView plans
- No external dependencies

## Files Included

- `Roshan_Gann_SSL_TF.pine` - Main indicator code
- `Roshan_Gann_SSL_TradingView_Guide.md` - Detailed guide in Persian
- `Roshan_Gann_SSL_README.md` - This file

## Credits

This indicator is based on the **Roshan Gann SSL** indicator for MetaTrader 4.

Original creator's Telegram: https://t.me/forexsystems

## License

Free for personal and educational use. For commercial use, please credit the original creator.

## Disclaimer

⚠️ **Risk Warning**: Trading in forex, cryptocurrencies, and other leveraged markets involves substantial risk and may not be suitable for all investors. Past performance is not indicative of future results. Always use proper risk management and never trade with money you cannot afford to lose.

## Version History

### v1.0.0 (2025-01-06)
- Initial release
- Full SSL Channel + Gann implementation
- Multi-timeframe capability
- Buy/Sell signals
- Alert system
- Info table

## Support

For questions and support:
- TradingView community forums
- Pine Script documentation: https://www.tradingview.com/pine-script-docs/

---

**Happy Trading!** 📈
