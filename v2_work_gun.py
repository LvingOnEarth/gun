from random import randrange as rnd, choice
import tkinter as tk
import math
import time

WIDTH = 800
HEIGHT = 600
root = tk.Tk()
canvas = tk.Canvas(root, bg='white')
root.geometry('800x600')
canvas.pack(fill=tk.BOTH, expand=1)

class Game:
    def __init__(self):
        self.points = 0
        self.id_points_text = canvas.create_text(30, 30, text = self.points, font = '28')
        self.finished_text = canvas.create_text(400, 300, text='', font='28')
        self.numb_targets = self.get_numb_of_targets()
        self.arr_targets = [Target() for i in range(self.numb_targets)]
        self.gun = Gun()
        self.horizon = canvas.create_line(0, HEIGHT - 100,
                                          WIDTH, HEIGHT - 100, fill='brown')

    def main(self):
        self.handlers()
        self.run()

    def get_numb_of_targets(self):
        return rnd(1, 4)

    def handlers(self):
        canvas.bind('<Button-1>', self.gun.fire_start)
        canvas.bind('<ButtonRelease-1>', self.gun.fire_end)
        canvas.bind('<Motion>', self.gun.targetting)

    def hit(self):
        self.points += 1
        canvas.itemconfig(self.id_points_text, text=self.points)

    def run(self):
        for target in self.arr_targets:
            target.move()
            for ball in self.gun.arr_balls:
                ball.move()
                if ball.hittest(target) and target.live:
                    target.live -= 1
                    self.hit()
                    self.numb_targets -= 1
                    canvas.delete(target.id)

        if self.numb_targets == 0:
            canvas.itemconfig(self.finished_text, text='Вы уничтожили цель за ' + str(self.gun.shots) + ' выстрелов')

        self.gun.power_up()
        self.gun.targetting()

        root.after(30, self.run)


class Ball:
    def __init__(self, x, y, vx, vy):
        """ Конструктор класса ball
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = 10
        self.vx = vx
        self.vy = vy
        self.vy_start = vy
        self.gravitation = .5
        self.x_resistance = .1
        self.future = 3
        self.state = True # after end of ball's life, it can't hit targets
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canvas.create_oval(self.x - self.r, self.y - self.r,
                                     self.x + self.r, self.y + self.r,
                                     fill=self.color)

    def set_coords(self):
        canvas.coords(self.id,
                      self.x - self.r, self.y - self.r,
                      self.x + self.r, self.y + self.r)

    def move(self):
        """Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        if self.gravitation != 0:
            # algorithm of ball's gravitation (axis y)
            if ((self.y + self.r) + math.fabs(self.vy) > (HEIGHT - 100)) and ((self.y + self.r) != (HEIGHT - 100)):
                self.vy_start /= 2
                self.vy = self.vy_start
                self.y += ((HEIGHT - 100) - (self.y + self.r))
            if ((self.y + self.r) == (HEIGHT - 100)) and (self.vy < .5):
                self.vy = 0
                self.gravitation = 0
            else:
                self.vy -= self.gravitation
                self.y -= self.vy

            self.set_coords()

        if self.x_resistance != 0:
            self.x += self.vx
            # algorithm of ball's resistance by wind (axis x)
            if self.vx > 0:
                self.vx -= self.x_resistance
            elif self.vx < 0:
                self.vx += self.x_resistance
            if math.fabs(self.vx) <= .2:
                self.vx = 0
                self.x_resistance = 0
            if ((self.x + self.r) >= WIDTH) or ((self.x - self.r) <= 0):
                self.vx *= (-1)

            self.set_coords()

        if (self.gravitation == 0) and (self.x_resistance == 0):
            self.end()

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if self.state:
            hypo = ((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2) ** .5
            if hypo <= (self.r + obj.r):
                return True
            else:
                return False

    def end(self):
        now = time.time()
        if self.future == 3:
            self.future += now
        if now >= self.future:
            self.state = False
            canvas.delete(self.id)


class Gun:
    def __init__(self):
        x_1 = self.x_1 = 20
        y_1 = self.y_1 = 450
        self.x_2 = 0
        self.y_2 = 0
        self.shots = 0
        self.arr_balls = []
        self.power = 10
        self.fire_on = False
        self.angle = 1
        self.id = canvas.create_line(x_1, y_1, 50, 420, width=7)

    def fire_start(self, event):
        self.fire_on = True

    def fire_end(self, event):
        """Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        self.shots += 1
        self.angle = math.atan((event.y - self.y_1) / (event.x - self.x_1))
        self.x_2 = self.x_1 + max(self.power, self.x_1) * math.cos(self.angle)
        self.y_2 = self.y_1 + max(self.power, self.x_1) * math.sin(self.angle)
        new_ball_vx = self.power * math.cos(self.angle)
        new_ball_vy = - self.power * math.sin(self.angle)
        new_ball = Ball(self.x_2, self.y_2, new_ball_vx, new_ball_vy)
        new_ball.r += 5
        self.arr_balls += [new_ball]
        self.fire_on = 0
        self.power = 10

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.angle = math.atan((event.y - self.y_1) / (event.x - self.x_1))
        if self.fire_on:
            canvas.itemconfig(self.id, fill='orange')
        else:
            canvas.itemconfig(self.id, fill='black')
        canvas.coords(self.id, self.x_1, self.y_1,
                      self.x_1 + max(self.power, self.x_1) * math.cos(self.angle),
                      self.y_1 + max(self.power, self.x_1) * math.sin(self.angle))

    def power_up(self):
        if self.fire_on:
            if self.power < 100:
                self.power += 1
            canvas.itemconfig(self.id, fill='orange')
        else:
            canvas.itemconfig(self.id, fill='black')


class Target:
    def __init__(self):
        x = self.x = rnd(600, 780)
        y = self.y = rnd(200, 450)
        self.vy = rnd(1, 5)
        r = self.r = rnd(2, 50)
        self.color = 'red'
        self.live = 1
        self.id = canvas.create_oval(x - r, y - r, x + r, y + r, fill=self.color)

    def set_coords(self):
        canvas.coords(self.id,
                      self.x - self.r, self.y - self.r,
                      self.x + self.r, self.y + self.r)

    def move(self):
        self.y += self.vy
        if ((self.y - self.r) <= 0) or (self.y + self.r) >= (HEIGHT - 100):
            self.vy *= (-1)

        self.set_coords()




game = Game()
game.main()
tk.mainloop()
