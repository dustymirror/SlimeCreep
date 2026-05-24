# SLIME CREEP v1.13

from europi import *
from europi_script import EuroPiScript
from time import ticks_ms, ticks_diff, sleep
import random
import machine

FPS = 12
DISP_MS = int(1000 / FPS)
CHAOS_MS = 8

# 旋钮映射参数：目标范围 speed 0.3 ~ 10.0
SPEED_MIN = 0.3
SPEED_MAX = 10.0
DEPTH_MIN = 0.05
DEPTH_MAX = 2.0

# 增量响应参数
THRESH = 0.008
SPD_SCALE = 25.0    # 增大，让一次转动覆盖更大范围
DEP_SCALE = 4.0     # 增大，让一次转动覆盖更大范围

BUTTON_WINDOW = 250


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def to_cv(v):
    return clamp(v + 5, 0, 10)


class Sloth:
    def __init__(self, base):
        self.base = base
        self.x = random.uniform(-1, 1)
        self.y = random.uniform(-1, 1)
        self.vx = 0
        self.vy = 0
        self.cx = random.uniform(-2, 2)
        self.cy = random.uniform(-2, 2)
        self.cvx = 0
        self.cvy = 0
        self.range = random.uniform(0.5, 1.2)
        self.target = random.uniform(0.4, 1.4)
        self.ax = random.uniform(-1, 1)
        self.ay = random.uniform(-1, 1)
        self.speed = 1.0
        self.depth = 0.6

    def perturb(self, amt):
        self.vx += random.uniform(-amt, amt)
        self.vy += random.uniform(-amt, amt)
        self.cvx += random.uniform(-amt, amt) * 0.2
        self.cvy += random.uniform(-amt, amt) * 0.2

    def update(self, coupling):
        t = self.speed
        b = self.base

        self.cvx += random.uniform(-0.00003, 0.00003) * t
        self.cvy += random.uniform(-0.00003, 0.00003) * t
        self.cvx *= 0.9994
        self.cvy *= 0.9994
        self.cx += self.cvx * t * 14
        self.cy += self.cvy * t * 14
        self.cx = clamp(self.cx, -3.5, 3.5)
        self.cy = clamp(self.cy, -3.5, 3.5)

        if random.randint(0, max(4, int(9000 / t))) == 1:
            self.target = random.uniform(0.25, 1.8)
        self.range += (self.target - self.range) * (0.00005 * t)

        self.ax += random.uniform(-0.0003, 0.0003) * t
        self.ay += random.uniform(-0.0003, 0.0003) * t
        self.ax = clamp(self.ax, -2, 2)
        self.ay = clamp(self.ay, -2, 2)

        dx = self.x - self.cx
        dy = self.y - self.cy
        dist = abs(dx) + abs(dy) + 0.001
        force = 0.001 + self.depth * 0.0018

        self.vx += ( (dy * force) - (dx * abs(dx) * 0.0007) + (self.ax * 0.0003) + random.uniform(-0.0005, 0.0005) ) * b * t
        self.vy += ( (-dx * force) - (dy * abs(dy) * 0.0007) + (self.ay * 0.0003) + random.uniform(-0.0005, 0.0005) ) * b * t

        self.vx += coupling * 0.00005 * t
        self.vy -= coupling * 0.00005 * t

        if dist > self.range:
            escape = (dist - self.range) * 0.0012 * t
            self.vx -= dx * escape
            self.vy -= dy * escape
            self.vx += random.uniform(-0.001, 0.001) * t
            self.vy += random.uniform(-0.001, 0.001) * t

        self.vx *= 0.9985
        self.vy *= 0.9985
        self.x += self.vx
        self.y += self.vy
        self.x = clamp(self.x, -5, 5)
        self.y = clamp(self.y, -5, 5)

        return self.x, self.y


class SlimeCreep(EuroPiScript):

    def __init__(self):
        super().__init__()

        self.names = ["Creep", "Ooze", "Smear"]

        self.creep = Sloth(0.0040)
        self.ooze = Sloth(0.00065)
        self.smear = Sloth(0.000025)
        self.sloths = [self.creep, self.ooze, self.smear]

        self.sel = 0

        self.scope_x = [16] * 128
        self.scope_y = [16] * 128
        self.scope_pos = 0

        self.flash = 0
        self.coupling = 0

        # 记录上一次旋钮位置，用于增量判断
        self.last_k1 = k1.percent()
        self.last_k2 = k2.percent()

        self.b1_time = 0
        self.b2_time = 0
        self.b1_pending = False
        self.b2_pending = False

        # 蜗牛动画变量
        self.snail_frame = 0
        self.snail_y = 20

        @b1.handler_falling
        def _():
            self.b1_time = ticks_ms()
            self.b1_pending = True

        @b2.handler_falling
        def _():
            self.b2_time = ticks_ms()
            self.b2_pending = True

        @din.handler
        def _():
            amt = 0.02 + self.sloths[self.sel].depth * 0.03
            for s in self.sloths:
                s.perturb(amt)
            self.flash = 5

    def animate_snail(self, duration_ms=5000):
        start_time = ticks_ms()
        last_frame = start_time
        active_sel = self.sel
        frame_interval = 400

        while ticks_diff(ticks_ms(), start_time) < duration_ms:
            now = ticks_ms()
            if ticks_diff(now, last_frame) >= frame_interval:
                self.snail_frame = (self.snail_frame + 1) % 2
                last_frame = now

            s = self.sloths[active_sel]
            norm_x = (s.x + 5) / 10.0
            snail_x = int(norm_x * 100) - 12
            snail_x = min(snail_x, 110)

            self.snail_y += random.randint(-2, 2)
            self.snail_y = clamp(self.snail_y, 8, 30)

            oled.fill(0)
            oled.text("Slime Creep", 0, 0)
            oled.text("v1.13", 100, 24)
            snail_char = [" ;@- ", " ;@ ~ "][self.snail_frame]
            oled.text(snail_char, snail_x, self.snail_y)
            oled.show()
            sleep(0.02)

        oled.fill(0)
        oled.show()

    def handle_buttons(self):
        now = ticks_ms()
        if self.b1_pending and self.b2_pending and abs(ticks_diff(self.b1_time, self.b2_time)) < BUTTON_WINDOW:
            self.b1_pending = False
            self.b2_pending = False
            machine.soft_reset()
            return
        if self.b1_pending and ticks_diff(now, self.b1_time) > BUTTON_WINDOW:
            self.sel = (self.sel - 1) % 3
            self.b1_pending = False
        if self.b2_pending and ticks_diff(now, self.b2_time) > BUTTON_WINDOW:
            self.sel = (self.sel + 1) % 3
            self.b2_pending = False

    def controls(self):
        s = self.sloths[self.sel]

        k1v = k1.percent()
        k2v = k2.percent()

        # 计算旋钮变化量
        d1 = k1v - self.last_k1
        d2 = k2v - self.last_k2

        # 更新记录值
        self.last_k1 = k1v
        self.last_k2 = k2v

        # 增量响应（仅当转动超过阈值时）
        if abs(d1) > THRESH:
            # 直接线性映射，手感直接
            delta = d1 * SPD_SCALE
            s.speed = clamp(s.speed + delta, SPEED_MIN, SPEED_MAX)

        if abs(d2) > THRESH:
            delta = d2 * DEP_SCALE
            s.depth = clamp(s.depth + delta, DEPTH_MIN, DEPTH_MAX)

        self.coupling = ain.percent() * 2

    def chaos(self):
        vals = []
        for s in self.sloths:
            vals.append(s.update(self.coupling))
        cv1.voltage(to_cv(vals[0][0]))
        cv4.voltage(to_cv(vals[0][1]))
        cv2.voltage(to_cv(vals[1][0]))
        cv5.voltage(to_cv(vals[1][1]))
        cv3.voltage(to_cv(vals[2][0]))
        cv6.voltage(to_cv(vals[2][1]))

        x = clamp(int(16 + vals[self.sel][0] * 1.3), 8, 22)
        y = clamp(int(16 + vals[self.sel][1] * 1.3), 8, 22)
        self.scope_x[self.scope_pos] = x
        self.scope_y[self.scope_pos] = y
        self.scope_pos = (self.scope_pos + 1) % 128

    def display(self):
        oled.fill(0)
        s = self.sloths[self.sel]
        oled.text(self.names[self.sel], 0, 0)

        for i in range(127):
            p1 = (self.scope_pos + i) % 128
            p2 = (self.scope_pos + i + 1) % 128
            oled.line(i, self.scope_x[p1], i+1, self.scope_x[p2], 1)
        for i in range(128):
            p = (self.scope_pos + i) % 128
            oled.pixel(i, self.scope_y[p], 1)

        oled.text(f"X{s.speed:.1f}", 0, 24)
        oled.text(f"D{s.depth:.2f}", 50, 24)
        oled.text("D*" if self.flash else "D.", 98, 24)
        if self.flash:
            self.flash -= 1

        bars = ["_", "-", "=", "#", "@"]
        lvl = int(clamp(self.coupling * 2, 0, 4))
        oled.text("A" + bars[lvl], 112, 24)
        oled.show()

    def main(self):
        self.animate_snail(5000)
        lc = ticks_ms()
        ld = ticks_ms()
        while True:
            self.handle_buttons()
            self.controls()
            now = ticks_ms()
            if ticks_diff(now, lc) >= CHAOS_MS:
                self.chaos()
                lc = now
            if ticks_diff(now, ld) >= DISP_MS:
                self.display()
                ld = now


if __name__ == "__main__":
    SlimeCreep().main()