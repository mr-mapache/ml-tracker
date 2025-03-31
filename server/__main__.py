import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

if __name__ == '__main__':
    from uvicorn import run
    run('entrypoint:api', host='0.0.0.0', port=8000, log_level='info')