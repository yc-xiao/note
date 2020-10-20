# doc -> https://matplotlib.org/api/_as_gen/matplotlib.pyplot.html
# 中文乱码 -> https://blog.csdn.net/dgatiger/article/details/50414549

import matplotlib.pyplot as plt
import matplotlib


def generate_line_char(xvalues, yvalues, title='line char', show_value=True):
    """
        title, 标题
        xvalue = [x1,x2,x3] x轴数值
        yvalue = [
            'tags': '标签名', # 不同标签的线
            'values': ['y1', 'y2', 'y3'] # 与x轴对应
        ]
        is show value 是否显示数值
    """
    try:
        matplotlib.rcParams['font.sans-serif'] = ['SimHei']
        matplotlib.rcParams['font.family'] = 'sans-serif'
        matplotlib.rcParams['axes.unicode_minus'] = False
        plt.figure(figsize=(16, 8), dpi=120)  # 图表大小
        # plt.title('样本')
        plt.xticks([i for i in range(len(xvalues))], xvalues, rotation=30)  # 设置x轴

        for y in yvalues:
            values = [int(v.split('%')[0]) for v in y['values']]
            plt.plot(xvalues, values, label=y['tags'], linewidth=1)
            if not show_value:
                continue
            for x, y in zip(xvalues, values):
                plt.annotate(f'{y}%', (x, y+1))

        path = f'/tmp/{title}.png'
        plt.grid(linestyle='--')  # 网格
        plt.legend(loc=(1.01, 0.82))
        plt.savefig(path)
        plt.show()
    except Exception as e:  
        print(e)
        return None
    return path

if __name__ == '__main__':
    x = ['2020-01', '2020-02', '2020-03']
    y = [
        {'tags': 'a', 'values':['1%', '11%', '21%']},
        {'tags': 'b', 'values':['7%', '32%', '6%']},
        {'tags': 'c', 'values':['2%', '15%', '9%']},
    ]
    generate_line_char(x, y)
