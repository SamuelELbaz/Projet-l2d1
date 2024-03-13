import pygame
import os

PATH = os.path.abspath(__file__)
PATH = os.path.dirname(PATH)
PATH = os.path.dirname(PATH)


class ScreenRenderer:

    @staticmethod
    def update_screen_resolution(self):
        pygame.display.set_mode(self.resolution)
        self.options_screen()
    
    @staticmethod
    def update_margins(self):
        self.margin_x = int(self.resolution[0] * self.margin_x_ratio)
        self.margin_y = int(self.resolution[1] * self.margin_y_ratio)

    @staticmethod
    def update_font_size(self):
        self.font_size = int(self.base_font_size * min(self.resolution[0] / self.base_resolution[0],
                                                       self.resolution[1] / self.base_resolution[1]))
        self.font = pygame.font.Font(self.font_name, self.font_size)

    @staticmethod
    def draw_text(screen, text, color, font, x, y):
        rendered_text = font.render(text, True, color)
        text_rect = rendered_text.get_rect(topleft=(x, y))
        screen.screen.blit(rendered_text, text_rect)

    def draw_options_text(self, screen, options_data):
        for i, option_data in enumerate(options_data):
            self.draw_text(screen, option_data["desc text"], "#d7fcd4", screen.font, screen.margin_x,
                           screen.margin_y + i * screen.font.size(option_data["desc text"])[1])

    @staticmethod
    def render_background(screen, background: str) -> None:
        image = pygame.image.load(background)
        image = pygame.transform.scale(image, screen.resolution)
        screen.screen.blit(image, (0, 0))

    def render_option_background(self, screen) -> None:
        self.render_background(screen, "./assets/background-options.bmp")
        overlay = pygame.Surface(screen.resolution, pygame.SRCALPHA)
        pygame.draw.rect(overlay, (0, 0, 0, 200), (0, 0, screen.resolution[0], screen.resolution[1]))
        screen.screen.blit(overlay, (0, 0))