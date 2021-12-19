import time
from collections import defaultdict

import click
import requests
import utility
import threading
import concurrent.futures
from tqdm import tqdm

FLAG_SUCCESS = 1
FLAG_Fail = 0


class TestResult:
    def __init__(self, funcTest):
        self.funcTest = funcTest
        self.response = defaultdict(list)

    def appendSuccess(self, duration):
        self.response[FLAG_SUCCESS].append(duration)

    def appendFailed(self, duration):
        self.response[FLAG_Fail].append(duration)

    def getRequestCount(self):
        count = 0
        for key, value in self.response.items():
            count += len(value)
        return count

    def outPut(self):
        self._outFuncInfo()
        self._outTimeCost()
        self._outDistribution()

    def _outFuncInfo(self):
        info = {
            'concurrency': str(self.funcTest.concurrency),
            'success': str(len(self.response[FLAG_SUCCESS])),
            'fail': str(len(self.response[FLAG_Fail]))
        }
        line = "Concurrency:{concurrency:10} Success:{success:10} Fail:{fail:10}"
        line = line.format(**info)
        print(line)

    def _outTimeCost(self):
        success_lst = self.response[FLAG_SUCCESS]
        min_cost = str(round(min(success_lst), 4))
        max_cost = str(round(max(success_lst), 4))
        avg_cost = str(round(float(sum(success_lst)) / len(success_lst), 4))

        line = "AVG:{avg_cost} MAX:{max_cost} MIN:{min_cost}"
        print(line.format(min_cost=min_cost, max_cost=max_cost, avg_cost=avg_cost))

    def _outDistribution(self):
        elapsed_sorted = sorted(self.response[FLAG_SUCCESS])
        print("Response status summary:")
        for p in [50, 90, 95, 99, 100]:
            c = (len(elapsed_sorted) * p / 100) - 1
            print("{:>8}%{:>10.2f}ms".format(p, elapsed_sorted[int(c)] * 1000))


class FuncTest:
    def __init__(self, *args, **kwargs):
        self.method = kwargs['method']
        self.timeout = kwargs['timeout']
        self.concurrency = kwargs['concurrency']
        self.headers = utility.get_header()
        self.params = []
        self.test_result = TestResult(self)

    def _request(self, params):
        time_span = 0
        session = requests.session()
        status = FLAG_Fail
        try:
            if self.method == 'GET':
                res = session.get(url=utility.BASE_URL, params=params, headers=self.headers, timeout=self.timeout)
            else:
                res = session.post(url=utility.BASE_URL, json=params, headers=self.headers, timeout=self.timeout)
            time_span = res.elapsed.total_seconds()
            if 200 <= res.status_code:
                status = FLAG_SUCCESS
        except ValueError:
            pass
        if status == FLAG_SUCCESS:
            self.test_result.appendSuccess(time_span)
        else:
            self.test_result.appendFailed(time_span)

    def init_params(self):
        for _ in range(self.concurrency):
            self.params.append(utility.get_query())

    def run(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(tqdm(executor.map(self._request, self.params), total=len(self.params)))
        return results

        # with tqdm(total=10, desc='Process...', leave=True, ncols=100, unit='B', unit_scale=True):
        #     process_bar = tqdm(self.threads)
        #     for t in self.threads:
        #         process_bar.update(1)
        #         t.setDaemon(True)
        #         t.start()
        #         print('%s Execute time: %s' % (t, get_time_ms()))
        #         t.join()
        #  print("Done")
        #   exit()


def get_time_ms():
    ct = time.time()  # 时间戳
    local_time = time.localtime(ct)  # 本地化时间
    cart_time_strftime = time.strftime("%Y-%m-%d %H:%M:%S", local_time)  # 格式化时间
    cart_time_strftime_ms = (ct - int(ct)) * 1000
    ms = "%s.%03d" % (cart_time_strftime, cart_time_strftime_ms)  # 拼接，获取毫秒级时间
    return ms


@click.command()
@click.option('-m', '--method', type=click.Choice(['GET', 'POST']), default='GET', help='GET or POST')
@click.option('-t', '--timeout', type=int, default=3, help='The max latency time')
@click.option('-c', '--concurrency', type=int, default=10, help='Num of thread')
def main(method, timeout, concurrency):
    print(method, timeout, concurrency)
    f = FuncTest(**locals())
    f.init_params()
    f.run()
    f.test_result.outPut()


if __name__ == '__main__':
    main()
