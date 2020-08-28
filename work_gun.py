from random import randrange as rnd, choice
import tkinter as tk
import math
import time

WIDTH = 800
HEIGHT = 500

def main():
    global root, canvas, target, screen1, gun, bullet, balls
    root = tk.Tk()
    # fr = tk.Frame(root)
    root.geometry(str(WIDTH) + 'x' + str(HEIGHT + 100))
    canvas = tk.Canvas(root, bg='white')
    canvas.pack(fill=tk.BOTH, expand=1)

    target = Target()
    screen1 = canvas.create_text(400, 300, text='', font='28')
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
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canvas.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color
        )
        self.live = 30

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
        # FIXME
        self.x += self.vx
        self.y -= self.vy
        self.set_coords()

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        # FIXME
        return False


class Gun:
    def __init__(self):
        x_1 = self.x_1 = 20
        y_1 = self.y_1 = 450
        self.f2_power = 10
        self.f2_on = 0
        self.angle = 1
        self.id = canvas.create_line(x_1, y_1, 50, 420, width=7)

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        self.angle = math.atan((event.y - self.y_1) / (event.x - self.x_1))
        self.x_2 = self.x_1 + max(self.f2_power, self.x_1) * math.cos(self.angle)
        self.y_2 = self.y_1 + max(self.f2_power, self.x_1) * math.sin(self.angle)
        new_ball_vx = self.f2_power * math.cos(self.angle)
        new_ball_vy = - self.f2_power * math.sin(self.angle)
        new_ball = Ball(self.x_2, self.y_2, new_ball_vx, new_ball_vy)
        new_ball.r += 5
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.angle = math.atan((event.y - self.y_1) / (event.x - self.x_1))
        if self.f2_on:
            canvas.itemconfig(self.id, fill='orange')
        else:
            canvas.itemconfig(self.id, fill='black')
        canvas.coords(self.id, self.x_1, self.y_1,
                      self.x_1 + max(self.f2_power, self.x_1) * math.cos(self.angle),
                      self.y_1 + max(self.f2_power, self.x_1) * math.sin(self.angle))

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canvas.itemconfig(self.id, fill='orange')
        else:
            canvas.itemconfig(self.id, fill='black')


class Target:
    def __init__(self):
        x = self.x = rnd(600, 780)
        y = self.y = rnd(300, 550)
        r = self.r = rnd(2, 50)
        self.color = 'red'
        self.points = 0
        self.live = 1
        self.id = canvas.create_oval(x - r, y - r, x + r, y + r, fill=self.color)
        self.id_points = canvas.create_text(30, 30, text = self.points, font = '28')
        # canvas.coords(self.id, x - r, y - r, x + r, y + r)
        # canvas.itemconfig(self.id, fill=color)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        canvas.coords(self.id, -10, -10, -10, -10)
        self.points += points
        canvas.itemconfig(self.id_points, text=self.points)




def cycle():
    target.live = 1
    while target.live or balls:
        for ball in balls:
            ball.move()
            if ball.hittest(target) and target.live:
                target.live = 0
                target.hit()
                canvas.bind('<Button-1>', '')
                canvas.bind('<ButtonRelease-1>', '')
                canvas.itemconfig(screen1, text='Вы уничтожили цель за ' + str(bullet) + ' выстрелов')
        canvas.update()
        gun.targetting()
        time.sleep(0.03)
        gun.power_up()
    canvas.itemconfig(screen1, text='')
    canvas.delete(gun)
    root.after(50, cycle)


def new_game(event=''):
    canvas.bind('<Button-1>', gun.fire2_start)
    canvas.bind('<ButtonRelease-1>', gun.fire2_end)
    canvas.bind('<Motion>', gun.targetting)


main()
new_game()
cycle()
tk.mainloop()
