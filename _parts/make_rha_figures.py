#!/usr/bin/env python3
"""
Generates the SVG geometry for the rice husk ash figures (3, 4 and 5) from the
measured values in the thesis, so no coordinate is typed by hand.

Source of every number below:
  Md Hasibul Hossain et al. (2022) "Utilization of Rice Husk Ash (RHA) as
  Partial Replacement of Cement for Sustainable Concrete", B.Sc. thesis,
  Department of Civil Engineering, Presidency University, Bangladesh.
  Supervisor: Susmita Majumder.
"""

# ---------------------------------------------------------------- data ----

LEVELS = [0, 5, 10, 15, 20, 25]          # % cement replaced by RHA

STRENGTH = {                              # average compressive strength, psi
    7:  [1840.381, 1125.804, 1293.794, 1002.923,  522.202, 545.069],
    14: [1672.381, 1937.928, 1743.144,  872.203,  883.167, 508.746],
    28: [2723.974, 3316.907, 2584.458, 1535.064,  950.403, 868.011],
}

COST = [21.853, 21.578, 21.303, 21.027, 20.752, 20.477]   # tk per cylinder
ABSORPTION = [2.630, 2.374, 3.013, 3.448, 4.000, 4.320]   # water absorption, %

OXIDES = ['SiO2', 'CaO', 'Al2O3', 'Fe2O3', 'MgO', 'SO3']
OXIDE_LABEL = ['SiO&#8322;', 'CaO', 'Al&#8322;O&#8323;',
               'Fe&#8322;O&#8323;', 'MgO', 'SO&#8323;']
OPC = [20.49, 63.85, 4.98, 3.11, 2.57, 2.69]              # % by mass
RHA = [62.30, 12.56, 10.11, 6.48, 3.50, 0.61]             # % by mass


def esc(v, n=0):
    return ('%.' + str(n) + 'f') % v


# ------------------------------------------- FIGURE 3 : oxide composition ----

def figure3():
    X0, X1 = 170, 862          # plot area
    TOP = 56
    PITCH = 52
    BAR_H = 15
    SCALE = (X1 - X0) / 70.0   # 0 - 70 % by mass

    out = []
    # grid + axis ticks every 10 %
    grid, ticks = [], []
    for v in range(0, 71, 10):
        x = X0 + v * SCALE
        grid.append('M%.1f %d V%d' % (x, TOP - 10, TOP + PITCH * 6 - 14))
        ticks.append('<text x="%.1f" y="%d" text-anchor="middle" '
                     'font-family="var(--font-body)" font-size="9.5" '
                     'fill="var(--fig-ink-soft)">%d</text>'
                     % (x, TOP + PITCH * 6 + 2, v))
    out.append('            <g stroke="var(--fig-grid)" stroke-width="1">')
    out.append('              <path d="%s"/>' % ' '.join(grid))
    out.append('            </g>')

    for i, name in enumerate(OXIDE_LABEL):
        top = TOP + PITCH * i
        out.append('            <text x="%d" y="%d" text-anchor="end" '
                   'font-family="var(--font-body)" font-size="11.5" '
                   'font-weight="600" fill="var(--fig-ink)">%s</text>'
                   % (X0 - 14, top + 22, name))
        # OPC bar
        w = OPC[i] * SCALE
        out.append('            <rect x="%d" y="%d" width="%.1f" height="%d" rx="2" '
                   'fill="var(--fig-5)"/>' % (X0, top, w, BAR_H))
        out.append('            <text x="%.1f" y="%d" font-family="var(--font-body)" '
                   'font-size="10" fill="var(--fig-ink-soft)">%s %%</text>'
                   % (X0 + w + 7, top + 12, esc(OPC[i], 2)))
        # RHA bar
        w2 = RHA[i] * SCALE
        out.append('            <rect x="%d" y="%d" width="%.1f" height="%d" rx="2" '
                   'fill="var(--fig-2)"/>' % (X0, top + BAR_H + 4, w2, BAR_H))
        out.append('            <text x="%.1f" y="%d" font-family="var(--font-body)" '
                   'font-size="10" font-weight="600" fill="var(--fig-2)">%s %%</text>'
                   % (X0 + w2 + 7, top + BAR_H + 16, esc(RHA[i], 2)))

    out.append('            <g>')
    out.extend('  ' + t for t in ticks)
    out.append('            </g>')
    out.append('            <path d="M%d %d V%d" stroke="var(--fig-stroke)" '
               'stroke-width="1.3" fill="none"/>'
               % (X0, TOP - 10, TOP + PITCH * 6 - 14))
    return '\n'.join(out)


# ------------------------------------ FIGURE 4 : compressive strength -------

def figure4():
    X0, X1 = 86, 884
    Y0, Y1 = 306, 62           # Y0 = zero line, Y1 = top of scale
    YMAX = 3500.0
    scale = (Y0 - Y1) / YMAX
    group_w = (X1 - X0) / 6.0
    bar_w, gap = 33, 5
    ages = [7, 14, 28]
    colours = ['var(--fig-5)', 'var(--fig-1)', 'var(--fig-2)']

    out = []
    # gridlines
    grid, ylab = [], []
    v = 0
    while v <= 3500:
        y = Y0 - v * scale
        grid.append('M%d %.1f H%d' % (X0, y, X1))
        ylab.append('<text x="%d" y="%.1f" text-anchor="end" '
                    'font-family="var(--font-body)" font-size="9.5" '
                    'fill="var(--fig-ink-soft)">%d</text>' % (X0 - 10, y + 3.5, v))
        v += 500
    out.append('            <g stroke="var(--fig-grid)" stroke-width="1">')
    out.append('              <path d="%s"/>' % ' '.join(grid))
    out.append('            </g>')
    out.append('            <g>')
    out.extend('  ' + t for t in ylab)
    out.append('            </g>')

    # highlight the optimum band (5 % replacement group)
    c_opt = X0 + group_w * 1.5
    out.append('            <rect x="%.1f" y="%d" width="%.1f" height="%.1f" rx="4" '
               'fill="var(--fig-2)" opacity="0.07"/>'
               % (X0 + group_w, Y1 - 24, group_w, Y0 - Y1 + 24))

    total = 3 * bar_w + 2 * gap
    for i, lvl in enumerate(LEVELS):
        c = X0 + group_w * (i + 0.5)
        left = c - total / 2.0
        for j, age in enumerate(ages):
            val = STRENGTH[age][i]
            h = val * scale
            x = left + j * (bar_w + gap)
            out.append('            <rect x="%.1f" y="%.1f" width="%d" height="%.1f" '
                       'rx="2" fill="%s"/>' % (x, Y0 - h, bar_w, h, colours[j]))
            if age == 28:
                out.append('            <text x="%.1f" y="%.1f" text-anchor="middle" '
                           'font-family="var(--font-body)" font-size="9.5" '
                           'font-weight="650" fill="var(--fig-2)">%d</text>'
                           % (x + bar_w / 2.0, Y0 - h - 6, round(val)))
        # category label
        out.append('            <text x="%.1f" y="%d" text-anchor="middle" '
                   'font-family="var(--font-body)" font-size="11" '
                   'font-weight="%s" fill="%s">%d %%</text>'
                   % (c, Y0 + 20, '700' if lvl == 5 else '500',
                      'var(--fig-2)' if lvl == 5 else 'var(--fig-ink-soft)', lvl))
        # 28-day value as a percentage of the control
        pct = STRENGTH[28][i] / STRENGTH[28][0] * 100.0
        out.append('            <text x="%.1f" y="%d" text-anchor="middle" '
                   'font-family="var(--font-body)" font-size="9.5" fill="%s">%s %%</text>'
                   % (c, Y0 + 35,
                      'var(--fig-2)' if pct >= 100 else 'var(--fig-4)', esc(pct, 1)))

    # axes
    out.append('            <path d="M%d %d V%d H%d" fill="none" '
               'stroke="var(--fig-stroke)" stroke-width="1.4"/>'
               % (X0, Y1 - 24, Y0, X1))
    return '\n'.join(out)


# --------------------------------- FIGURE 5 : cost and durability -----------

def panel(x0, x1, y0, y1, values, ymin, ymax, colour, fmt, unit):
    scale = (y0 - y1) / float(ymax - ymin)
    gw = (x1 - x0) / 6.0
    bw = 26
    out = []
    grid = []
    steps = 4
    for k in range(steps + 1):
        v = ymin + (ymax - ymin) * k / float(steps)
        y = y0 - (v - ymin) * scale
        grid.append('M%d %.1f H%d' % (x0, y, x1))
        out.append('            <text x="%d" y="%.1f" text-anchor="end" '
                   'font-family="var(--font-body)" font-size="9" '
                   'fill="var(--fig-ink-soft)">%s</text>'
                   % (x0 - 8, y + 3.5, fmt % v))
    out.insert(0, '            <g stroke="var(--fig-grid)" stroke-width="1">'
                  '<path d="%s"/></g>' % ' '.join(grid))

    pts = []
    for i, val in enumerate(values):
        c = x0 + gw * (i + 0.5)
        h = (val - ymin) * scale
        out.append('            <rect x="%.1f" y="%.1f" width="%d" height="%.1f" '
                   'rx="2" fill="%s" opacity="0.85"/>'
                   % (c - bw / 2.0, y0 - h, bw, h, colour))
        pts.append('%.1f,%.1f' % (c, y0 - h))
        out.append('            <text x="%.1f" y="%d" text-anchor="middle" '
                   'font-family="var(--font-body)" font-size="9" '
                   'fill="var(--fig-ink-soft)">%d</text>' % (c, y0 + 16, LEVELS[i]))
    out.append('            <polyline points="%s" fill="none" stroke="%s" '
               'stroke-width="1.6" stroke-linejoin="round"/>' % (' '.join(pts), colour))
    for p in pts:
        cx, cy = p.split(',')
        out.append('            <circle cx="%s" cy="%s" r="3" fill="var(--fig-bg)" '
                   'stroke="%s" stroke-width="1.6"/>' % (cx, cy, colour))
    out.append('            <path d="M%d %d V%d H%d" fill="none" '
               'stroke="var(--fig-stroke)" stroke-width="1.3"/>' % (x0, y1, y0, x1))
    out.append('            <text x="%.1f" y="%d" text-anchor="middle" '
               'font-family="var(--font-body)" font-size="9.5" '
               'fill="var(--fig-ink-soft)">RHA replacement (%%)</text>'
               % ((x0 + x1) / 2.0, y0 + 34))
    return '\n'.join(out)


def figure5():
    a = panel(90, 430, 250, 70, COST, 20.0, 22.0,
              'var(--fig-3)', '%.1f', 'tk')
    b = panel(560, 890, 250, 70, ABSORPTION, 2.0, 4.5,
              'var(--fig-4)', '%.1f', '%')
    return a, b


if __name__ == '__main__':
    import io, os, sys
    here = os.path.dirname(os.path.abspath(__file__))
    f5a, f5b = figure5()
    blocks = {
        '{{FIG3_BODY}}': figure3(),
        '{{FIG4_BODY}}': figure4(),
        '{{FIG5_A}}': f5a,
        '{{FIG5_B}}': f5b,
    }
    target = os.path.join(here, 'body-research.html')
    s = io.open(target, encoding='utf-8').read()
    for k, v in blocks.items():
        if k not in s:
            sys.stderr.write('placeholder missing: %s\n' % k)
            sys.exit(1)
        s = s.replace(k, v)
    io.open(target, 'w', encoding='utf-8').write(s)
    print('RHA figure geometry injected')
