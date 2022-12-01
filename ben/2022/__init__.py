from pathlib import Path
py_files = list(Path(__file__).parent.glob('**/*.py'))
py_files = [x.relative_to(Path.cwd()).as_posix().replace('/', '.').replace('.py', '') 
            for x in py_files if not x.stem.startswith('_')]
[__import__(x) for x in py_files]
