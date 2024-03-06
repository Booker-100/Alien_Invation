import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """ 管理游戏资源和行为的类"""

    def __init__(self):
        
        pygame.init()

        # 读取设置
        self.settings = Settings()

        # 创建屏幕
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width,self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion")
        
        # 创建一艘飞船
        self.ship = Ship(self)

        # 创建子弹编组
        self.bullets = pygame.sprite.Group()

        # 创建外星人编组
        self.aliens = pygame.sprite.Group()
        self._create_fleet()


    def run_game(self):
        """游戏主循环"""
        while True:
            self._check_events()
            self.ship.update()
            self.bullets.update()
            self._update_bullet()
            self._update_screen()

    def _check_events(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """响应按键按下"""
        # 飞船移动
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
            

    def _check_keyup_events(self, event):
        """相应按键松开"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets中"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullet(self):
        """删除飞出屏幕的子弹"""
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _create_fleet(self):
        """创建外星人舰队"""
        alien = Alien(self)
        
        # 计算一行可容纳多少敌人
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # 计算屏幕可容纳多少行敌人
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # 创建敌人舰队
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._creat_alien(alien_number, row_number)


    def _creat_alien(self, alien_number, row_number):
        """创建一个敌人并放在当前行"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_screen(self):
        """更新屏幕上的图像"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        pygame.display.flip()
    
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()