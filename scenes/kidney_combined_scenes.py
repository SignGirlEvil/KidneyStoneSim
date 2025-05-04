import math
import pygame as py 
import sys
import cv2


def play_animation():
    py.init()

    # define colors & font
    white = (255, 255, 255)
    green = (0, 255, 0)
    black = (0, 0, 0)
    blue = (47, 141, 255)
    # font = py.font.SysFont('arial', 25)
    font = py.font.Font('resources/ARIAL.TTF', 20)

    # define clock
    clock = py.time.Clock()
    start_time = py.time.get_ticks()


    # define screen and images
    FrameHeight = 600
    FrameWidth = 800
    screen = py.display.set_mode((FrameWidth, FrameHeight))
    supersaturated = py.image.load("resources/supersaturated_1.jpeg").convert()
    kidney_with_callout = py.image.load("resources/kidney_w_callout_1.jpg").convert()
    flow = py.image.load("resources/supersaturated_mini_2.jpeg").convert()
    crystal = py.image.load("resources/crystal_2.jpg").convert()
    stone = py.image.load("resources/stone_1.png").convert_alpha()
    kidney = py.image.load("resources/kidney_2.jpeg").convert()
    moving_stone = py.image.load("resources/stone_1.png")

    # scene 1 description w/ white backgrounds
    s1_description_l1 = font.render('As flow continues through the nephrons in the kidneys for filtration,', True, black, white)
    s1_description_l2 = font.render('a supersaturation of water to CaOx molecules will lead to nucleation.', True, black, white)
    s1_description_length = 800
    s1_description_width = 1000
    s1_description_rect_l1 = s1_description_l1.get_rect()
    s1_description_rect_l1.center = (s1_description_length // 2, s1_description_width // 2)
    s1_description_rect_l2 = s1_description_l2.get_rect()
    s1_description_rect_l2.center = (s1_description_length // 2, (s1_description_width // 2 + 28))

    # scene 1 legend
    s1_legend_width = 50
    s1_legend_length = 1200
    s1_legend_water = font.render('Water Molecule', True, black)
    s1_legend_caox = font.render('CaOx Molecule', True, black)
    s1_legend_rect_water = s1_legend_water.get_rect()
    s1_legend_rect_water.topleft = (s1_legend_length // 2, s1_legend_width // 2)
    s1_legend_rect_caox= s1_legend_caox.get_rect()
    s1_legend_rect_caox.topleft = (s1_legend_length // 2, (s1_legend_width // 2 + 30))
    s1_legend_bg = py.Rect(595, 25, 187, 60)

    # scrolling the background
    s1_scroll = 0
    s1_tiles = math.ceil(FrameWidth / supersaturated.get_width()) + 1

    # scene 2 scrolling window
    s2_window = py.Rect(50, 150, 100, 100)
    s2_window_frame = py.Rect(48.5, 148.5, 105, 105)
    s2_tiles = math.ceil(FrameWidth / flow.get_width()) + 1
    s2_scroll = 0

    # scene 2 description
    s2_description = font.render('This flow takes place in the nephrons, which flow into the papillae.', True, black, white)
    s2_description_rect = s2_description.get_rect()
    s2_description_length = 800
    s2_description_width = 1000
    s2_description_rect.center = (s2_description_length // 2, s2_description_width // 2)

    # scene 3 window
    s3_window = py.Rect(50, 150, 100, 100)
    s3_window_frame = py.Rect(48.5, 148.5, 105, 105)

    # scene 3 description
    s3_description = font.render('As nucleation takes place, these molecules form crystals which grow on the papillae.', True, black, white)
    s3_description_rect = s2_description.get_rect()
    s3_description_length = 800
    s3_description_width = 1000
    s3_description_rect.center = (s3_description_length // 2 - 75, s3_description_width // 2)

    # scene 4 growth
    s4_stone_start_size = 10
    s4_stone_end_size = 200
    s4_stone_speed = 0.5  # pixels per frame
    s4_stone_current_size = s4_stone_start_size
    s4_stone_locations = [(295, 155), (415, 400), (410, 210), (440, 360)]

    # scene 4 description
    s4_description = font.render('These crystals grow into stones on the papillae over years.', True, black, white)
    s4_description_rect = s4_description.get_rect()
    s4_description_length = 800
    s4_description_width = 1000
    s4_description_rect.center = (s4_description_length // 2, s4_description_width // 2)

    # scene 5 stone scale
    s5_moving_stone = py.transform.scale(moving_stone, (200, 200))
    s5_stone_rect = s5_moving_stone.get_rect()

    # scene 5 extracting path function
    def extract_path(image_path, screen_width, screen_height):
        # Load image and get its dimensions
        s5_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        img_height, img_width = s5_img.shape
        # Threshold the image to get a binary path representation
        _, thresh = cv2.threshold(s5_img, 128, 255, cv2.THRESH_BINARY_INV)
        # Find contours in the thresholded image
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Scale coordinates to fit the screen
        s5_path_points = []
        for contour in contours:
            for point in contour:
                x, y = point[0]
                y -=100
                x -= 132
                s5_path_points.append((x, y))
        #print(s5_path_points)
        s5_path_points = s5_path_points[:(len(s5_path_points)//2)]
        return s5_path_points

    # scene 5 extract path
    s5_path = extract_path("resources/stone_path_2.jpeg", FrameWidth, FrameHeight)
    s5_path_index = 0
    s5_stone_speed = 0.71
    # initial position
    if s5_path:
        s5_stone_rect.x, s5_stone_rect.y = s5_path[0]
    # grab target
    s5_path_target_x, s5_path_target_y = s5_path[s5_path_index] if s5_path else (0, 0)

    # scene 5 description
    s5_description_l1 = font.render('Over time, the flow through the kidney can dislodge a stone,', True, black, white)
    s5_description_l2 = font.render('and cause it to get caught in the renal tube.', True, black, white)
    s5_description_length = 800;
    s5_description_width = 1000;
    s5_description_rect_l1 = s5_description_l1.get_rect()
    s5_description_rect_l1.center = (s5_description_length // 2, s5_description_width // 2)
    s5_description_rect_l2= s5_description_l2.get_rect()
    s5_description_rect_l2.center = (s5_description_length // 2, (s5_description_width // 2 + 28))

    #scene durations
    s1_duration = 6000
    s2_duration = 5000
    s3_duration = 5000
    s4_duration = 5000
    s5_duration = 5000
    # MAIN LOOP
    running = True
    while running:

        # setting up timer
        time = py.time.get_ticks() - start_time

        # general quit statement
        for event in py.event.get():
            if event.type == py.QUIT:
                running = False
        ## SCENE 1
        if time <= s1_duration:
            # Scrolling background
            for i in range(s1_tiles):
                screen.blit(supersaturated, (supersaturated.get_width() * i + s1_scroll, 0))
            s1_scroll -= 0.1
            if abs(s1_scroll) > supersaturated.get_width():
                s1_scroll = 0

            py.draw.rect(screen, white, s1_legend_bg)
            py.draw.circle(screen, blue, (760, 40), 10)
            py.draw.circle(screen, green, (760, 70), 10)
            screen.blit(s1_description_l1, s1_description_rect_l1)
            screen.blit(s1_description_l2, s1_description_rect_l2)
            screen.blit(s1_legend_water, s1_legend_rect_water)
            screen.blit(s1_legend_caox, s1_legend_rect_caox)
        ## SCENE 2
        elif time > s1_duration and time <= (s1_duration + s2_duration):
            # background kidney
            screen.blit(kidney_with_callout, (0, 0))
            # creating temporary window frame
            s2_temp_frame = py.Surface((s2_window_frame.width, s2_window_frame.height))
            screen.blit(s2_temp_frame, (s2_window_frame.x, s2_window_frame.y))
            s2_temp_surface = py.Surface((s2_window.width, s2_window.height))
            for i in range(s2_tiles):
                s2_temp_surface.blit(flow, (flow.get_width()*i + s2_scroll, 0))
                s2_scroll -=0.01
            if abs(s2_scroll) > flow.get_width():
                s2_scroll = 0;
            screen.blit(s2_temp_surface, (s2_window.x, s2_window.y))
            screen.blit(s2_description, s2_description_rect)
        ## SCENE 3
        elif time > (s1_duration + s2_duration) and time <= (s1_duration + s2_duration + s3_duration):
            # background kidney
            screen.blit(kidney_with_callout, (0, 0))
            # creating temporary window frame
            s3_temp_frame = py.Surface((s3_window_frame.width, s3_window_frame.height))
            s3_temp_surface = py.Surface((s3_window.width, s3_window.height))
            s3_temp_surface.blit(crystal, (0, 25))
            screen.blit(s3_temp_surface, (s3_window.width, s3_window.height))
            screen.blit(s3_description, s3_description_rect)
        ## SCENE 4
        elif time > (s1_duration + s2_duration + s3_duration) and time <= (s1_duration + s2_duration + s3_duration + s4_duration):
            # growth
            if s4_stone_current_size < s4_stone_end_size:
                s4_stone_current_size += s4_stone_speed
            if s4_stone_current_size > s4_stone_end_size:
                s4_stone_current_size = s4_stone_end_size
             # draw
            screen.blit(kidney, (0, 0))
            s4_scaled_img = [0]*len(s4_stone_locations)
            s4_img_rect = [0]*len(s4_stone_locations)
            for i in range(len(s4_stone_locations)):
                s4_scaled_img[i] = py.transform.smoothscale(stone, (s4_stone_current_size, s4_stone_current_size))
                s4_img_rect[i] = s4_scaled_img[i].get_rect(center=s4_stone_locations[i])
                screen.blit(s4_scaled_img[i], s4_img_rect[i].topleft)
            screen.blit(s4_description, s4_description_rect)
        ## SCENE 5
        elif time > (s1_duration + s2_duration + s3_duration + s4_duration) and time <= (s1_duration + s2_duration + s3_duration + s4_duration + s5_duration):
            screen.blit(kidney, (0, 0))
            if s5_path_index < len(s5_path):
                # Move sprite towards target
                s5_dx, s5_dy = s5_path_target_x - s5_stone_rect.x, s5_path_target_y - s5_stone_rect.y
                s5_distance = (s5_dx**2 + s5_dy**2) ** 0.5

                if s5_distance > s5_stone_speed or s5_distance > 1:
                    # s5_stone_rect.x += s5_stone_speed * s5_dx / s5_distance
                    # s5_stone_rect.y += s5_stone_speed * s5_dy / s5_distance
                    s5_stone_move_x = s5_stone_speed * s5_dx / s5_distance
                    s5_stone_move_y = s5_stone_speed * s5_dy / s5_distance

                    s5_stone_rect.x += s5_stone_move_x
                    s5_stone_rect.y += s5_stone_move_y
                else:
                    s5_stone_rect.x, s5_stone_rect.y = s5_path_target_x, s5_path_target_y
                    s5_path_index += 1
                    if s5_path_index < len(s5_path):
                        s5_path_target_x, s5_path_target_y = s5_path[s5_path_index]
            screen.blit(s5_moving_stone, s5_stone_rect)
            screen.blit(s5_moving_stone, (315, 300))
            screen.blit(s5_moving_stone, (310, 110))
            screen.blit(s5_moving_stone, (340, 260))
            screen.blit(s5_description_l1, s5_description_rect_l1)
            screen.blit(s5_description_l2, s5_description_rect_l2)
        else:
            print('Animation done!')
            return

        py.display.update()

    py.quit()

