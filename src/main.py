
from subprocess import PIPE, run

class CommandLine():
    @staticmethod
    def execute(command):
        result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
        print(result)
        return result.stdout

def init_app(debug=True, port=8000, host='0.0.0.0'):
    try:
        from app import app, socketio
        socketio.run(app, debug=debug, port=port, host=host)
    except ModuleNotFoundError as e:
        module = [str(w).replace("'","") for w in str(e).split()][-1]
        if module != 'loopgpt':
            print(f'Module not found: \'{module}\'. Installing now.')
            CommandLine.execute(f'sudo pip3 install -U {module.title()}')
            init_app()
        else:
            print(str(e))

if __name__ == '__main__':
    init_app(debug=True, port=8000, host='0.0.0.0')