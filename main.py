from scenes.kidney_combined_scenes import play_animation
from crystals.simulation import run_simulation
import threading
from crystals.equil2 import equil2
from scenes.kidneyinputupdated import *


def main():
    calcium_level, oxalate_level = make_gui()
    calcium_level = float(calcium_level)
    oxalate_level = float(oxalate_level)
    print(calcium_level, oxalate_level)
    info_dict = equil2(5, 5, calcium_level, 5, 5, 5, 5, 5, oxalate_level, 5, 5, 5)
    supersaturation = info_dict[0]['Calcium Oxalate']
    print(supersaturation)

    animation_thread = threading.Thread(target=play_animation)
    simulation_thread = threading.Thread(target=run_simulation, args=(supersaturation,))

    animation_thread.start()
    simulation_thread.start()

    animation_thread.join()
    simulation_thread.join()
    print('All done!')


if __name__ == '__main__':
    main()
