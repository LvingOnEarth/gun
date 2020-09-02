from random import randrange as rnd, choice
import tkinter as tk
import math
import time

WIDTH = 800
HEIGHT = 500

class Game:
    pass

def main():
    global root, canvas, target, screen, gun, bullet, balls, targets
    root = tk.Tk()
    # fr = tk.Frame(root)
    root.geometry(str(WIDTH) + 'x' + str(HEIGHT + 100))
    canvas = tk.Canvas(root, bg='white')
    canvas.pack(fill=tk.BOTH, expand=1)
    canvas.create_line(0, HEIGHT, WIDTH, HEIGHT, fill='red')

    numb_of_targets = 3
    targets = [Target() for i in range(numb_of_targets)]
    screen = canvas.create_text(400, 300, text='', font='28')
    gun = Gun()
    bullet = 0
    balls = []


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
        self.state = True
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canvas.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color
        )

    def set_coords(self):
        canvas.coords(
                self.id,
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r
        )

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        print(self.vy, self.gravitation)

        # algorithm of ball's gravitation (axis y)
        if ((self.y + self.r) + math.fabs(self.vy) > HEIGHT) and ((self.y + self.r) != HEIGHT):
            self.vy_start /= 2
            self.vy = self.vy_start
            self.y += (HEIGHT - (self.y + self.r))
        if ((self.y + self.r) == HEIGHT) and (self.vy < .5):
            self.vy = 0
            self.gravitation = 0
        else:
            self.vy -= self.gravitation
            self.y -= self.vy

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

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        hypo = ((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2) ** .5
        if hypo <= (self.r + obj.r):
            return True
        else:
            return False


class Gun:
    def __init__(self):
        x_1 = self.x_1 = 20
        y_1 = self.y_1 = 450
        self.x_2 = 0
        self.y_2 = 0
        self.power = 10
        self.fire_on = 0
        self.angle = 1
        self.id = canvas.create_line(x_1, y_1, 50, 420, width=7)

    def fire_start(self, event):
        self.fire_on = 1

    def fire_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        self.angle = math.atan((event.y - self.y_1) / (event.x - self.x_1))
        self.x_2 = self.x_1 + max(self.power, self.x_1) * math.cos(self.angle)
        self.y_2 = self.y_1 + max(self.power, self.x_1) * math.sin(self.angle)
        new_ball_vx = self.power * math.cos(self.angle)
        new_ball_vy = - self.power * math.sin(self.angle)
        new_ball = Ball(self.x_2, self.y_2, new_ball_vx, new_ball_vy)
        new_ball.r += 5
        balls += [new_ball]
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
        r = self.r = rnd(2, 50)
        self.color = 'red'
        self.points = 0 # move to Class Game
        self.live = 1
        self.id = canvas.create_oval(x - r, y - r, x + r, y + r, fill=self.color)
        self.id_points = canvas.create_text(30, 30, text = self.points, font = '28') # move to Class Game
        # canvas.coords(self.id, x - r, y - r, x + r, y + r)
        # canvas.itemconfig(self.id, fill=color)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        canvas.coords(self.id, -10, -10, -10, -10) # remove self.id ???
        self.points += points # move to Class Game
        canvas.itemconfig(self.id_points, text=self.points) # move to Class Game


def cycle():
    for ball in balls:
        if not ball.state:
            balls.remove(ball)
            continue
        if (ball.gravitation != 0) or (ball.x_resistance != 0):
            ball.move()
        for target in targets:
            if ball.hittest(target) and target.live:
                target.live = 0
                target.hit()
                # canvas.bind('<Button-1>', '')
                # canvas.bind('<ButtonRelease-1>', '')
                canvas.itemconfig(screen, text='Вы уничтожили цель за ' + str(bullet) + ' выстрелов')
    # canvas.update()
    gun.targetting()
    # time.sleep(0.03)
    gun.power_up()
    canvas.itemconfig(screen, text='')
    # canvas.delete(gun)
    root.after(30, cycle)

def new_game(event=''):
    canvas.bind('<Button-1>', gun.fire_start)
    canvas.bind('<ButtonRelease-1>', gun.fire_end)
    canvas.bind('<Motion>', gun.targetting)


main()
new_game()
cycle()
tk.mainloop()
