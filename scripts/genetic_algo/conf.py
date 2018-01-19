import random
import numpy as np


selectors = {
    'BTC-CUR': ['gdax.BTC-USD', 'gdax.BTC-EUR', 'gdax.BTC-GBP'],
    'ETH-BTC': ['gdax.ETH-BTC'],
    'ETH-EUR': ['gdax.ETH-EUR'],
    'ETH-USD': ['gdax.ETH-USD'],
    'ETH-CUR': ['gdax.ETH-USD', 'gdax.ETH-EUR'],
}
partitions = 2
selectivity = 0.3

runid = random.randint(1000, 9999)
sigma = 20
indpb = 0.3
mutpb = 0.3
cxpb = 0.3

# strategies = ['crossover_vwap', 'trend_ema', 'cci_srsi', 'macd']
strategies = ['trend_ema']
# need to debug:
# crossover_vwap, cci_srsi, macd

# parameters for strategies
params_default = {}
params_default['crossover_vwap'] = {
    # common
    'period': {'min': 1, 'max': 400, 'default': 120,
               'std': 2, 'dtype': np.int32, 'unit': 'm'},  # RangePeriod(1, 400, 'm'),
    # 'min_periods': {'min': 1, 'max': 200, 'default': 200,
    #                 'dtype': np.int32},  # Range(1, 200),
    # 'markdown_buy_pct': {'min': -1, 'max': 5, 'default': 200,
    #                      'dtype': np.float64},  # RangeFloat(-1, 5),
    # 'markup_sell_pct': {'min': -1, 'max': 5, 'default': 200,
    #                     'dtype': np.float64},  # RangeFloat(-1, 5),
    # -- strategy
    'emalen1': {'min': 1, 'max': 300, 'default': 30,
                'std': 2, 'dtype': np.int32, 'unit': ''},  # Range(1, 300),
    'smalen1': {'min': 1, 'max': 300, 'default': 108,
                'std': 2, 'dtype': np.int32, 'unit': ''},  # Range(1, 300),
    'smalen2': {'min': 1, 'max': 300, 'default': 60,
                'std': 2, 'dtype': np.int32, 'unit': ''},  # Range(1, 300),
    'vwap_length': {'min': 1, 'max': 300, 'default': 10,
                    'std': 2, 'dtype': np.int32, 'unit': ''},  # Range(1, 300),
    'vwap_max': {'min': 0, 'max': 10000, 'default': 8000,
                 'std': 2, 'dtype': np.int32, 'unit': ''},  # RangeFactor(0, 10000, 10)  # 0 disables this max cap. Test in increments of 10
    }
# trend_ema (default)
#   description:
#     Buy when (EMA - last(EMA) > 0) and sell when (EMA - last(EMA) < 0). Optional buy on low RSI.
params_default['trend_ema'] = {
    # common
    # --periodLength=<value>  period length, same as --period (default: 2m)
    'period': {'min': 1, 'max': 120, 'default': 2, 'std': 2,
               'dtype': np.int32, 'unit': 'm'},  # RangePeriod(1, 400, 'm'),
    # --min_periods=<value>  min. number of history periods (default: 52)
    'min_periods': {'min': 1, 'max': 100, 'default': 52, 'std': 2,
                    'dtype': np.int32, 'unit': ''},  # Range(1, 100),
    # --trend_ema=<value>  number of periods for trend EMA (default: 26)
    'trend_ema': {'min': 1, 'max': 50, 'default': 26, 'std': 2,
                  'dtype': np.int32, 'unit': ''},  # Range(TREND_EMA_MIN, TREND_EMA_MAX),
    # --neutral_rate=<value>  avoid trades if abs(trend_ema) under this float (0 to disable, "auto" for a variable filter) (default: auto)
    # leave at 'auto' -> no mention
    # --oversold_rsi_periods=<value>  number of periods for oversold RSI (default: 14)
    'oversold_rsi_periods': {'min': 1, 'max': 50, 'default': 14, 'std': 2,
                             'dtype': np.int32, 'unit': ''},  #
    # --oversold_rsi=<value>  buy when RSI reaches this value (default: 10)
    'oversold_rsi_periods': {'min': 1, 'max': 20, 'default': 10, 'std': 2,
                             'dtype': np.int32, 'unit': ''},  #
    }
# cci_srsi,
#   description:
#     Stochastic CCI Strategy
params_default['cci_srsi'] = {
    # --period=<value>  period length, same as --periodLength (default: 20m)
    'period': {'min': 1, 'max': 120, 'default': 20, 'std': 2,
               'dtype': np.int32, 'unit': 'm'},
    # --min_periods=<value>  min. number of history periods (default: 30)
    'min_periods': {'min': 1, 'max': 200, 'default': 30, 'std': 2,
                    'dtype': np.int32, 'unit': ''},
    # --ema_acc=<value>  sideways threshold (0.2-0.4) (default: 0.03)
    'ema_acc': {'min': 0, 'max': 1, 'default': 0.03, 'std': .1,
                'dtype': np.float64, 'unit': ''},
    # --cci_periods=<value>  number of RSI periods (default: 14)
    'cci_periods': {'min': 1, 'max': 200, 'default': 14, 'std': 2,
                    'dtype': np.int32, 'unit': ''},
    # --rsi_periods=<value>  number of RSI periods (default: 14)
    'rsi_periods': {'min': 1, 'max': 200, 'default': 14, 'std': 2,
                    'dtype': np.int32, 'unit': ''},
    # --srsi_periods=<value>  number of RSI periods (default: 9)
    'srsi_periods': {'min': 1, 'max': 200, 'default': 9, 'std': 2,
                     'dtype': np.int32, 'unit': ''},
    # --srsi_k=<value>  %K line (default: 5)
    'srsi_k': {'min': 1, 'max': 50, 'default': 5, 'std': 2,
               'dtype': np.int32, 'unit': ''},
    # --srsi_d=<value>  %D line (default: 3)
    'srsi_d': {'min': 1, 'max': 50, 'default': 3, 'std': 2,
               'dtype': np.int32, 'unit': ''},
    # --oversold_rsi=<value>  buy when RSI reaches or drops below this value (default: 18)
    'oversold_rsi': {'min': 1, 'max': 100, 'default': 18, 'std': 2,
                     'dtype': np.int32, 'unit': ''},
    # --overbought_rsi=<value>  sell when RSI reaches or goes above this value (default: 85)
    'overbought_rsi': {'min': 1, 'max': 100, 'default': 85, 'std': 2,
                       'dtype': np.int32, 'unit': ''},
    # --oversold_cci=<value>  buy when CCI reaches or drops below this value (default: -90)
    'oversold_cci': {'min': -100, 'max': 100, 'default': -90, 'std': 2,
                     'dtype': np.int32, 'unit': ''},
    # --overbought_cci=<value>  sell when CCI reaches or goes above this value (default: 140)
    'oversold_cci': {'min': -100, 'max': 300, 'default': 140, 'std': 2,
                     'dtype': np.int32, 'unit': ''},
    # --constant=<value>  constant (default: 0.015)
    'oversold_cci': {'min': 0.001, 'max': 0.05, 'default': 0.015,
                     'std': 0.02, 'dtype': np.float64, 'unit': ''},
    }
# macd
#   description:
#     Buy when (MACD - Signal > 0) and sell when (MACD - Signal < 0).
params_default['macd'] = {
    # --period=<value>  period length, same as --periodLength (default: 1h)
    'period': {'min': 1, 'max': 240, 'default': 60, 'std': 5,
               'dtype': np.int32, 'unit': 'm'},
    # --min_periods=<value>  min. number of history periods (default: 52)
    'min_periods': {'min': 1, 'max': 200, 'default': 52, 'std': 2,
                    'dtype': np.int32, 'unit': ''},
    # --ema_short_period=<value>  number of periods for the shorter EMA (default: 12)
    'ema_short_period': {'min': 1, 'max': 20, 'default': 12, 'std': 1,
                         'dtype': np.int32, 'unit': ''},
    # --ema_long_period=<value>  number of periods for the longer EMA (default: 26)
    'ema_long_period': {'min': 20, 'max': 100, 'default': 26, 'std': 2,
                        'dtype': np.int32, 'unit': ''},
    # --signal_period=<value>  number of periods for the signal EMA (default: 9)
    'signal_period': {'min': 1, 'max': 20, 'default': 9, 'std': 1,
                      'dtype': np.int32, 'unit': ''},
    # --up_trend_threshold=<value>  threshold to trigger a buy signal (default: 0)
    'up_trend_threshold': {'min': 0, 'max': 50, 'default': 0, 'std': 1,
                           'dtype': np.int32, 'unit': ''},
    # --down_trend_threshold=<value>  threshold to trigger a sold signal (default: 0)
    'down_trend_threshold': {'min': 0, 'max': 50, 'default': 0, 'std': 1,
                             'dtype': np.int32, 'unit': ''},
    # --overbought_rsi_periods=<value>  number of periods for overbought RSI (default: 25)
    'overbought_rsi_periods': {'min': 1, 'max': 50, 'default': 25,
                               'std': 1, 'dtype': np.int32, 'unit': ''},
    # --overbought_rsi=<value>  sold when RSI exceeds this value (default: 70)
    'overbought_rsi': {'min': 20, 'max': 100, 'default': 70,
                       'std': 1, 'dtype': np.int32, 'unit': ''},
    }




#
# forex_analytics
#   description:
#     Apply the trained forex analytics model.
#   options:
#     --modelfile=<value>  modelfile (generated by running `train`), should be in models/ (default: none)
#     --period=<value>  period length of a candlestick (default: 30m), same as --periodLength (default: 30m)
#     --periodLength=<value>  period length of a candlestick (default: 30m), same as --period (default: 30m)
#     --min_periods=<value>  min. number of history periods (default: 100)
#
#
# neural
#   description:
#     Use neural learning to predict future price. Buy = mean(last 3 real prices) < mean(current & last prediction)
#   options:
#     --period=<value>  period length - make sure to lower your poll trades time to lower than this value. Same as --periodLength (default: 1m)
#     --periodLength=<value>  period length - make sure to lower your poll trades time to lower than this value. Same as --period (default: 1m)
#     --activation_1_type=<value>  Neuron Activation Type: sigmoid, tanh, relu (default: sigmoid)
#     --neurons_1=<value>  Neurons in layer 1 Shoot for atleast 100 (default: 1)
#     --depth=<value>  Rows of data to predict ahead for matches/learning (default: 1)
#     --selector=<value>  Selector (default: Gdax.BTC-USD)
#     --min_periods=<value>  Periods to calculate learn from (default: 1000)
#     --min_predict=<value>  Periods to predict next number from (default: 1)
#     --momentum=<value>  momentum of prediction (default: 0.9)
#     --decay=<value>  decay of prediction, use teeny tiny increments (default: 0.1)
#     --threads=<value>  Number of processing threads you'd like to run (best for sim) (default: 1)
#     --learns=<value>  Number of times to 'learn' the neural network with past data (default: 2)
#
# rsi
#   description:
#     Attempts to buy low and sell high by tracking RSI high-water readings.
#   options:
#     --period=<value>  period length, same as --periodLength (default: 2m)
#     --periodLength=<value>  period length, same as --period (default: 2m)
#     --min_periods=<value>  min. number of history periods (default: 52)
#     --rsi_periods=<value>  number of RSI periods
#     --oversold_rsi=<value>  buy when RSI reaches or drops below this value (default: 30)
#     --overbought_rsi=<value>  sell when RSI reaches or goes above this value (default: 82)
#     --rsi_recover=<value>  allow RSI to recover this many points before buying (default: 3)
#     --rsi_drop=<value>  allow RSI to fall this many points before selling (default: 0)
#     --rsi_divisor=<value>  sell when RSI reaches high-water reading divided by this value (default: 2)
#
# sar
#   description:
#     Parabolic SAR
#   options:
#     --period=<value>  period length, same as --periodLength (default: 2m)
#     --periodLength=<value>  period length, same as --period (default: 2m)
#     --min_periods=<value>  min. number of history periods (default: 52)
#     --sar_af=<value>  acceleration factor for parabolic SAR (default: 0.015)
#     --sar_max_af=<value>  max acceleration factor for parabolic SAR (default: 0.3)
#
# speed
#   description:
#     Trade when % change from last two 1m periods is higher than average.
#   options:
#     --period=<value>  period length, same as --periodLength (default: 1m)
#     --periodLength=<value>  period length, same as --period (default: 1m)
#     --min_periods=<value>  min. number of history periods (default: 3000)
#     --baseline_periods=<value>  lookback periods for volatility baseline (default: 3000)
#     --trigger_factor=<value>  multiply with volatility baseline EMA to get trigger value (default: 1.6)
#
# srsi_macd
#   description:
#     Stochastic MACD Strategy
#   options:
#     --period=<value>  period length, same as --periodLength (default: 30m)
#     --periodLength=<value>  period length, same as --period (default: 30m)
#     --min_periods=<value>  min. number of history periods (default: 200)
#     --rsi_periods=<value>  number of RSI periods
#     --srsi_periods=<value>  number of RSI periods (default: 9)
#     --srsi_k=<value>  %D line (default: 5)
#     --srsi_d=<value>  %D line (default: 3)
#     --oversold_rsi=<value>  buy when RSI reaches or drops below this value (default: 20)
#     --overbought_rsi=<value>  sell when RSI reaches or goes above this value (default: 80)
#     --ema_short_period=<value>  number of periods for the shorter EMA (default: 24)
#     --ema_long_period=<value>  number of periods for the longer EMA (default: 200)
#     --signal_period=<value>  number of periods for the signal EMA (default: 9)
#     --up_trend_threshold=<value>  threshold to trigger a buy signal (default: 0)
#     --down_trend_threshold=<value>  threshold to trigger a sold signal (default: 0)
#
# stddev
#   description:
#     Buy when standard deviation and mean increase, sell on mean decrease.
#   options:
#     --period=<value>  period length, set poll trades to 100ms, poll order 1000ms. Same as --periodLength (default: 100ms)
#     --periodLength=<value>  period length, set poll trades to 100ms, poll order 1000ms. Same as --period (default: 100ms)
#     --trendtrades_1=<value>  Trades for array 1 to be subtracted stddev and mean from (default: 5)
#     --trendtrades_2=<value>  Trades for array 2 to be calculated stddev and mean from (default: 53)
#     --min_periods=<value>  min_periods (default: 1250)
#
# ta_ema
#   description:
#     Buy when (EMA - last(EMA) > 0) and sell when (EMA - last(EMA) < 0). Optional buy on low RSI.
#   options:
#     --period=<value>  period length, same as --periodLength (default: 10m)
#     --periodLength=<value>  period length, same as --period (default: 10m)
#     --min_periods=<value>  min. number of history periods (default: 52)
#     --trend_ema=<value>  number of periods for trend EMA (default: 20)
#     --neutral_rate=<value>  avoid trades if abs(trend_ema) under this float (0 to disable, "auto" for a variable filter) (default: 0.06)
#     --oversold_rsi_periods=<value>  number of periods for oversold RSI (default: 20)
#     --oversold_rsi=<value>  buy when RSI reaches this value (default: 30)
#
# ta_macd
#   description:
#     Buy when (MACD - Signal > 0) and sell when (MACD - Signal < 0).
#   options:
#     --period=<value>  period length, same as --periodLength (default: 1h)
#     --periodLength=<value>  period length, same as --period (default: 1h)
#     --min_periods=<value>  min. number of history periods (default: 52)
#     --ema_short_period=<value>  number of periods for the shorter EMA (default: 12)
#     --ema_long_period=<value>  number of periods for the longer EMA (default: 26)
#     --signal_period=<value>  number of periods for the signal EMA (default: 9)
#     --up_trend_threshold=<value>  threshold to trigger a buy signal (default: 0)
#     --down_trend_threshold=<value>  threshold to trigger a sold signal (default: 0)
#     --overbought_rsi_periods=<value>  number of periods for overbought RSI (default: 25)
#     --overbought_rsi=<value>  sold when RSI exceeds this value (default: 70)
#
# trendline
#   description:
#     Calculate a trendline and trade when trend is positive vs negative.
#   options:
#     --period=<value>  period length (default: 30s)
#     --periodLength=<value>  period length (default: 30s)
#     --lastpoints=<value>  Number of trades for short trend average (default: 100)
#     --avgpoints=<value>  Number of trades for long trend average (default: 1000)
#     --lastpoints2=<value>  Number of trades for short trend average (default: 10)
#     --avgpoints2=<value>  Number of trades for long trend average (default: 100)
#     --min_periods=<value>  Basically avgpoints + a BUNCH of more preroll periods for anything less than 5s period (default: 15000)
#     --markup_sell_pct=<value>  test (default: 0)
#     --markdown_buy_pct=<value>  test (default: 0)
#
# trust_distrust
#   description:
#     Sell when price higher than $sell_min% and highest point - $sell_threshold% is reached. Buy when lowest price point + $buy_threshold% reached.
#   options:
#     --period=<value>  period length, same as --periodLength (default: 30m)
#     --periodLength=<value>  period length, same as --period (default: 30m)
#     --min_periods=<value>  min. number of history periods (default: 52)
#     --sell_threshold=<value>  sell when the top drops at least below this percentage (default: 2)
#     --sell_threshold_max=<value>  sell when the top drops lower than this max, regardless of sell_min (panic sell, 0 to disable) (default: 0)
#     --sell_min=<value>  do not act on anything unless the price is this percentage above the original price (default: 1)
#     --buy_threshold=<value>  buy when the bottom increased at least above this percentage (default: 2)
#     --buy_threshold_max=<value>  wait for multiple buy signals before buying (kill whipsaw, 0 to disable) (default: 0)
#     --greed=<value>  sell if we reach this much profit (0 to be greedy and either win or lose) (default: 0)
#
#
#   srsi_macd: {
#     // -- common
#     periodLength: RangePeriod(1, 120, 'm'),
#     min_periods: Range(1, 200),
#     markup_pct: RangeFloat(0, 5),
#     order_type: RangeMakerTaker(),
#     sell_stop_pct: Range0(1, 50),
#     buy_stop_pct: Range0(1, 50),
#     profit_stop_enable_pct: Range0(1, 20),
#     profit_stop_pct: Range(1,20),
#
#     // -- strategy
#     rsi_periods: Range(1, 200),
#     srsi_periods: Range(1, 200),
#     srsi_k: Range(1, 50),
#     srsi_d: Range(1, 50),
#     oversold_rsi: Range(1, 100),
#     overbought_rsi: Range(1, 100),
#     ema_short_period: Range(1, 20),
#     ema_long_period: Range(20, 100),
#     signal_period: Range(1, 20),
#     up_trend_threshold: Range(0, 20),
#     down_trend_threshold: Range(0, 20)
#   },
#   neural: {
#     // -- common
#     periodLength: RangePeriod(1, 120, 'm'),
#     min_periods: Range(1, 200),
#     markup_pct: RangeFloat(0, 5),
#     order_type: RangeMakerTaker(),
#     sell_stop_pct: Range0(1, 50),
#     buy_stop_pct: Range0(1, 50),
#     profit_stop_enable_pct: Range0(1, 20),
#     profit_stop_pct: Range(1,20),
#     // -- strategy
#     neurons_1: Range(1, 200),
#     activation_1_type: RangeNeuralActivation(),
#     depth: Range(1, 100),
#     min_predict: Range(1, 100),
#     momentum: Range(0, 100),
#     decay: Range(1, 10),
#     learns: Range(1, 200)
#   },
#   rsi: {
#     // -- common
#     periodLength: RangePeriod(1, 120, 'm'),
#     min_periods: Range(1, 200),
#     markup_pct: RangeFloat(0, 5),
#     order_type: RangeMakerTaker(),
#     sell_stop_pct: Range0(1, 50),
#     buy_stop_pct: Range0(1, 50),
#     profit_stop_enable_pct: Range0(1, 20),
#     profit_stop_pct: Range(1,20),
#
#     // -- strategy
#     rsi_periods: Range(1, 200),
#     oversold_rsi: Range(1, 100),
#     overbought_rsi: Range(1, 100),
#     rsi_recover: Range(1, 100),
#     rsi_drop: Range(0, 100),
#     rsi_divisor: Range(1, 10)
#   },
#   sar: {
#     // -- common
#     periodLength: RangePeriod(1, 120, 'm'),
#     min_periods: Range(2, 100),
#     markup_pct: RangeFloat(0, 5),
#     order_type: RangeMakerTaker(),
#     sell_stop_pct: Range0(1, 50),
#     buy_stop_pct: Range0(1, 50),
#     profit_stop_enable_pct: Range0(1, 20),
#     profit_stop_pct: Range(1,20),
#
#     // -- strategy
#     sar_af: RangeFloat(0.01, 1.0),
#     sar_max_af: RangeFloat(0.01, 1.0)
#   },
#   speed: {
#     // -- common
#     periodLength: RangePeriod(1, 120, 'm'),
#     min_periods: Range(1, 100),
#     markup_pct: RangeFloat(0, 5),
#     order_type: RangeMakerTaker(),
#     sell_stop_pct: Range0(1, 50),
#     buy_stop_pct: Range0(1, 50),
#     profit_stop_enable_pct: Range0(1, 20),
#     profit_stop_pct: Range(1,20),
#
#     // -- strategy
#     baseline_periods: Range(1, 5000),
#     trigger_factor: RangeFloat(0.1, 10)
#   },
#   trust_distrust: {
#     // -- common
#     periodLength: RangePeriod(1, 120, 'm'),
#     min_periods: Range(1, 100),
#     markup_pct: RangeFloat(0, 5),
#     order_type: RangeMakerTaker(),
#     sell_stop_pct: Range0(1, 50),
#     buy_stop_pct: Range0(1, 50),
#     profit_stop_enable_pct: Range0(1, 20),
#     profit_stop_pct: Range(1,20),
#
#     // -- strategy
#     sell_threshold: Range(1, 100),
#     sell_threshold_max: Range0(1, 100),
#     sell_min: Range(1, 100),
#     buy_threshold: Range(1, 100),
#     buy_threshold_max: Range0(1, 100),
#     greed: Range(1, 100)
#   },
#   ta_macd: {
#     // -- common
#     periodLength: RangePeriod(1, 120, 'm'),
#     min_periods: Range(1, 200),
#     markup_pct: RangeFloat(0, 5),
#     order_type: RangeMakerTaker(),
#     sell_stop_pct: Range0(1, 50),
#     buy_stop_pct: Range0(1, 50),
#     profit_stop_enable_pct: Range0(1, 20),
#     profit_stop_pct: Range(1,20),
#
#     // -- strategy
#     // have to be minimum 2 because talib will throw an "TA_BAD_PARAM" error
#     ema_short_period: Range(2, 20),
#     ema_long_period: Range(20, 100),
#     signal_period: Range(1, 20),
#     up_trend_threshold: Range(0, 50),
#     down_trend_threshold: Range(0, 50),
#     overbought_rsi_periods: Range(1, 50),
#     overbought_rsi: Range(20, 100)
#   },
#   trendline: {
#     // -- common
#     periodLength: RangePeriod(1, 400, 'm'),
#     min_periods: Range(1, 200),
#     markdown_buy_pct: RangeFloat(-1, 5),
#     markup_sell_pct: RangeFloat(-1, 5),
#     order_type: RangeMakerTaker(),
#     sell_stop_pct: Range0(1, 50),
#     buy_stop_pct: Range0(1, 50),
#     profit_stop_enable_pct: Range0(1, 20),
#     profit_stop_pct: Range(1,20),
#
#     // -- strategy
#     lastpoints: Range(20, 500),
#     avgpoints: Range(300, 3000),
#     lastpoints2: Range(5, 300),
#     avgpoints2: Range(50, 1000),
#   },
#   ta_ema: {
#     // -- common
#     periodLength: RangePeriod(1, 120, 'm'),
#     min_periods: Range(1, 100),
#     markup_pct: RangeFloat(0, 5),
#     order_type: RangeMakerTaker(),
#     sell_stop_pct: Range0(1, 50),
#     buy_stop_pct: Range0(1, 50),
#     profit_stop_enable_pct: Range0(1, 20),
#     profit_stop_pct: Range(1,20),
#
#     // -- strategy
#     trend_ema: Range(TREND_EMA_MIN, TREND_EMA_MAX),
#     oversold_rsi_periods: Range(OVERSOLD_RSI_PERIODS_MIN, OVERSOLD_RSI_PERIODS_MAX),
#     oversold_rsi: Range(OVERSOLD_RSI_MIN, OVERSOLD_RSI_MAX)
#   }
