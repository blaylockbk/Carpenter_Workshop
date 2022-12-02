# Pandas

## DateOffset Strings

Several functions accept a DateOffset frequency string, https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects

```python
df.resample('5T').mean()
pd.date_range('2015-01-01', '2015-02-01', freq='5D')
```

| String | Meaning         | Example                                  |
| ------ | --------------- | ---------------------------------------- |
| 'M'    | Month end       | '3M' - every three months                |
| 'SM'   | Semi month end  | 'SM' - every 15th and last day of month. |
| 'A'    | Year end        | '3A' - every 3 years                     |
| 'D'    | Day             | '2D' -every 2 days                       |
| 'H'    | Hour            | '6H' -every 6 hours                      |
| 'T'    | or 'min' Minute | '5T' - every five minutes                |
| 'S'    | Second          | '30S' - every 30 seconds                 |
