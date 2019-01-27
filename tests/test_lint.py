from pylint import lint

def test_Lint():
    pylint_opts = [
        'rbcore',
        'tests',
        'setup.py',
    ]
    lint.Run(pylint_opts)
