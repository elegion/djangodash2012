compose = lambda f, g: lambda *a, **k: f(g(*a, **k))
