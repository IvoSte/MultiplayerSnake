from time import sleep
import pygame


def main():
    pygame.init()
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    #sleep(1)
    #print(joysticks[n_j].rumble(100, 1000000, 0))
    # #joysticks[n_j].stop_rumble()
    while True:
        pygame.event.get()
        for n_j, _ in enumerate(joysticks):
            print(  f"{n_j} = " + \
                    f"{joysticks[n_j].get_axis(0)} " + \
                    f"{joysticks[n_j].get_axis(1)}" + \
                    f"{joysticks[n_j].get_button(1)} " + \
                    f"{joysticks[n_j].get_axis(1)} " \
                    )
            sleep(1)
        #     if event.type == pygame.JOYAXISMOTION:
        #         print("JOYAXISMOTION")
        #     if event.type == pygame.JOYBALLMOTION:
        #         print("JOYBALLMOTION")
        #     if event.type == pygame.JOYBUTTONDOWN:
        #         print("JOYBUTTONDOWN")
        #     if event.type == pygame.JOYBUTTONUP:
        #         print("JOYBUTTONUP")
        #     if event.type == pygame.JOYHATMOTION:
        #         print("JOYHATMOTION")

           # print(f"{event.type = } {event = }")
#        sleep(1)

if __name__ == "__main__":
    main()