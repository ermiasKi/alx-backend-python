def lazy_paginate(page_size):
    data = paginate_users(page_size,0)

    for d in data:
        yield d
