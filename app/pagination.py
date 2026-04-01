class Pagination:
    def __init__(self, page: int, limit: int, total: int):
        self.page = page
        self.limit = limit
        self.total = total

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page * self.limit < self.total

    @property
    def prev_num(self):
        return self.page - 1

    @property
    def next_num(self):
        return self.page + 1

    def iter_pages(self):
        total_pages = (self.total // self.limit) + 1
        return range(1, total_pages + 1)