from Log import Log


class DataAggregate(object):
    def __init__(self):
        self.__tmp_date = set()
        self.__operate_list_dict = list()
        self.__result = list()
        self.__key = ""
        # 按传入当参数类型进行聚合,入参形式[{},{},{}]
        # 只找第一个匹配当数据，之后数据丢弃处理
        # 返回数据格式是[{},{},{}]
        self.L = Log("DataAggregate")

    def __key_suit(self):
        for i in self.__operate_list_dict:
            for j in i:
                self.__tmp_date.add(j.get(self.__key))
        try:
            self.__tmp_date.remove(None)
        except KeyError:
            pass
        finally:
            if len(self.__tmp_date) == 0:
                self.L.logger.warning("分类参数不在数据中")

    def __do_aggregate(self) -> None:
        self.__result = list()
        self.__key_suit()
        self.__tmp_date = list(self.__tmp_date)
        self.__tmp_date.sort()

        for i in range(len(self.__tmp_date)):
            self.__result.append({self.__key: self.__tmp_date[i]})

            for j in self.__operate_list_dict:

                for k in j:
                    if self.__tmp_date[i] == k.get(self.__key):
                        self.__result[i].update(k)
                        del self.__operate_list_dict[self.__operate_list_dict.index(j)][j.index(k)]
                        break

    def get_aggregate_result(self, *operate_list_dict: list, key: str) -> list:
        if len(operate_list_dict) > 1:
            self.__operate_list_dict = operate_list_dict
            self.__key = key
            self.__do_aggregate()
        else:
            try:
                self.__result = operate_list_dict[0]
            except IndexError:
                pass
            finally:
                self.__result = []

        self.__tmp_date = set()
        self.__operate_list_dict = list()
        self.__key = ""
        return self.__result

    def get_aggregate_result_copy(self, operate_list_dict: list, key: str) -> list:
        if len(operate_list_dict) > 1:
            self.__operate_list_dict = operate_list_dict
            self.__key = key
            self.__do_aggregate()
        else:
            try:
                self.__result = operate_list_dict[0]
            except IndexError:
                pass
            finally:
                self.__result = []

        self.__tmp_date = set()
        self.__operate_list_dict = list()
        self.__key = ""
        return self.__result
