import time

import concurrent.futures

from tqdm import tqdm


def f(x):
    time.sleep(0.001)  # to visualize the progress
    return x ** 2


def run(f, my_iter):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(tqdm(executor.map(f, my_iter), total=len(my_iter)))

    return results


def __init__(self, hibiscus):
    self.hibiscus = hibiscus
    self.responses = defaultdict(list)


def append_success(self, time_cost):
    self.responses[SUCCESS_STATUS].append(time_cost)


def append_failed(self, time_cost):
    self.responses[FAILED_STATUS].append(time_cost)


def completed(self):
    count = 0
    for key, values in self.responses.items():
        count += len(values)

    return count


def out_put(self):
    self._out_hibiscus_info()
    self._out_time_cost()
    self._out_distribution()


def _out_hibiscus_info(self):
    """
    输出性能测试基本信息
    :return:
    """
    info = {
        'concurrency': str(self.hibiscus.concurrency),
        'count': str(self.hibiscus.count),
        'success': str(len(self.responses[SUCCESS_STATUS])),
        'fail': str(len(self.responses[FAILED_STATUS]))
    }
    line = "并发度:{concurrency:12} 请求总数:{count:10} 成功数量:{success:10} 失败数量:{fail}"
    line = line.format(**info)
    print(line)


def _out_time_cost(self):
    """
    输出平均耗时，最大耗时，最小耗时
    :return:
    """
    success_lst = self.responses[SUCCESS_STATUS]
    min_cost = str(round(min(success_lst), 4))
    max_cost = str(round(max(success_lst), 4))
    avg_cost = str(round(float(sum(success_lst)) / len(success_lst), 4))

    line = "平均耗时:{avg_cost:10} 最大耗时:{max_cost:10} 最小耗时{min_cost}"
    print(line.format(min_cost=min_cost, max_cost=max_cost, avg_cost=avg_cost))


def _out_distribution(self):
    elapsed_sorted = sorted(self.responses[SUCCESS_STATUS])
    print("响应时间分布情况:\n")
    for p in [50, 60, 70, 80, 90, 95, 98, 99, 100, ]:
        c = (len(elapsed_sorted) * p / 100) - 1
        print("{:>12}%{:>10.2f}ms".format(p, elapsed_sorted[int(c)] * 1000))
