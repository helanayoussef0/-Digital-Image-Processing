from flake8.main.application import Application
import pytest

if __name__ == "__main__":
    # Lint code
    flake8 = Application()
    flake8.run([
        'assignment',
        '--max-line-length', '100',
    ])

    if flake8.result_count > 0:
        print('-- flake8 found code style issues --')
        flake8.exit()

    # Run tests
    pytest.main(['-v', '--basetemp', 'processing_results', '-W', 'ignore::DeprecationWarning'])
