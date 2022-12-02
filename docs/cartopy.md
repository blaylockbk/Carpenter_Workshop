# Cartopy


## `adjustable` axes, 'box' or 'datalim'

```python
fig, axes = plt.subplots(1, 2, subplot_kw=dict(projection=pc, adjustable='datalim'))
for ax in axes:
    ax.coastlines()
```

![image](https://user-images.githubusercontent.com/6249613/135505469-eb6953c2-3e32-478f-962c-af9841d7e252.png)

```python
# Default behavior is "box"
fig, axes = plt.subplots(1, 2, subplot_kw=dict(projection=pc, adjustable='box'))
for ax in axes:
    ax.coastlines()
```

![image](https://user-images.githubusercontent.com/6249613/135505540-68df0136-06ac-432d-82a0-be17e96b0fb9.png)
