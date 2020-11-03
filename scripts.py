from subprocess import call


def start():
    print('INFO:     Starting Server...')
    try:
        call([
            'uvicorn',
            'server.main:app',
            '--host', '192.168.2.2',
            '--port', '8000',
            '--no-use-colors'
        ])
    except KeyboardInterrupt:
        print('INFO:     Keyboard Interrupt.')


def dev():
    print('INFO:     Starting Server... [Debug Mode]')
    try:
        call([
            'uvicorn',
            'server.main:app',
            '--host', '192.168.2.2',
            '--port', '8000',
            '--reload',
            '--no-use-colors'
        ])
    except KeyboardInterrupt:
        print('INFO:     Keyboard Interrupt.')


def test():
    call(['pytest', '.\\tests'])
