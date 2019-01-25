from view.app import App
import sys

if len(sys.argv) == 2:
    app = App(int(sys.argv[1]), int(sys.argv[1]))
    app.on_init()
    app.run_game()
else:
    print('Invalid Arguments, you should specify N = Maze size in the arguments')
