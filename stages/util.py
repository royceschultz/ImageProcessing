def Cache():
    cache = None
    def stage(prev_stage):
        def cache_stage():
            nonlocal cache
            if cache is None:
                cache = prev_stage()
            return cache
        return cache_stage
    def clear(*args, **kwargs):
        nonlocal cache
        cache = None
    return stage, clear


def Then(*stages):
    def stage(prev_stage):
        p = prev_stage
        for s in stages:
            p = s(p)
        return p
    return stage


def PostEffect(effect):
    def stage(prev_stage):
        def post_effect():
            image = prev_stage()
            effect(image)
            return image
        return post_effect
    return stage
