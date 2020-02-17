

class TuplesGenerator:

    @staticmethod
    def generate_tuples(items):
        """
        [1, 2, 3, 4] -> [(1, 2), (3, 4)]

        :param items: list of any type
        :return:
        """
        assert len(items) > 1
        return [(items[i], items[i+1]) for i in range(0, len(items), 2)]

    @staticmethod
    def generate_tuples_lr_shuffle(items):
        left = items[0:int(len(items) / 2)]
        right = items[int(len(items) / 2):]
        return [(item_left, item_right) for item_left, item_right in zip(left, right)]

    @staticmethod
    def generate_wheels(items, gap=1):
        """
        [1, 2, 3, 4] -> [(4, 1), (1, 2), (2, 3), (3, 4)]

        :param items: list of any type
        :param gap: int
        :return:
        """
        assert len(items) > 1
        return [(items[i], items[i - gap]) for i in range(len(items))]
