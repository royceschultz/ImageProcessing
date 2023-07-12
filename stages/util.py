def Cache():
    def stage(prev_stage):
        cache = None

        def cache_stage():
            nonlocal cache
            if cache is None:
                cache = prev_stage()
            return cache
        return cache_stage
    return stage


def Then(*stages):
    def stage(prev_stage):
        p = prev_stage
        for s in stages:
            p = s(p)
        return p
    return stage
