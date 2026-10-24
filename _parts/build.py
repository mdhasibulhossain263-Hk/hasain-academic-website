#!/usr/bin/env python3
"""
Build script for mdhasibulhossain263-hk.github.io/hasain-academic-website

This assembles the .html pages from the shared shell in _parts/ and exports
standalone copies of the figures to assets/figures/.

YOU DO NOT NEED TO RUN THIS. The .html files are already built and can be
edited directly. This script exists only so the shared header/footer can be
changed in one place if you ever want to. If you do edit the .html files by
hand and then run this script, your hand edits will be overwritten.

Run with:   python3 _parts/build.py
"""

import io
import os
import re
import html.entities

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARTS = os.path.join(ROOT, '_parts')


def read(name):
    with io.open(os.path.join(PARTS, name), encoding='utf-8') as fh:
        return fh.read()


# ---------------------------------------------------------------- pages ----

NAV_KEYS = ['HOME', 'RESEARCH', 'EXPERIENCE', 'PORTFOLIO', 'TEACHING', 'CV',
            'CONTACT']
CURRENT = ' aria-current="page"'

PAGES = [
    dict(file='index.html', body='body-index.html', nav='HOME', page='',
         title='Md Hasibul Hossain — Civil &amp; Environmental Engineering Researcher',
         desc='Civil Engineering graduate with four years of laboratory research across '
              'structural, geotechnical and environmental engineering, and five years of '
              'professional practice in sustainability assessment. Seeking M.Sc. admission '
              'in Environmental Science.',
         jsonld=True),
    dict(file='research.html', body='body-research.html', nav='RESEARCH',
         page='research.html',
         title='Research — Md Hasibul Hossain',
         desc='Four undergraduate research projects: rice husk ash as a partial cement '
              'replacement, granular pile ground improvement modelled in PLAXIS 3D, '
              'reclaimed asphalt pavement reuse, and neural network forecasting of urban '
              'river water quality.',
         jsonld=False),
    dict(file='experience.html', body='body-experience.html', nav='EXPERIENCE',
         page='experience.html',
         title='Professional Experience — Md Hasibul Hossain',
         desc='Five years of professional practice: ISO 9001, 14001 and 45001 auditing, '
              'energy and ETP assessment, GRI-standard sustainability reporting for GIZ, '
              'BGMEA and national industrial groups, and civil infrastructure supervision.',
         jsonld=False),
    dict(file='portfolio.html', body='body-portfolio.html', nav='PORTFOLIO',
         page='portfolio.html',
         title='Portfolio — Md Hasibul Hossain',
         desc='Architectural design and visualisation in AutoCAD and SketchUp, '
              'infrastructure and campus master planning, AutoCAD working drawings, '
              'and cadastral land mapping and GIS digitisation in ArcGIS for '
              'national land-zoning work in Bangladesh.',
         jsonld=False),
    dict(file='teaching.html', body='body-teaching.html', nav='TEACHING',
         page='teaching.html',
         title='Teaching &amp; Service — Md Hasibul Hossain',
         desc='Seven years teaching physics, chemistry and biology at secondary and '
              'higher-secondary level, research mentoring in the geotechnical laboratory, '
              'and volunteering with United Nations Volunteers and Bidyanondo Foundation.',
         jsonld=False),
    dict(file='cv.html', body='body-cv.html', nav='CV', page='cv.html',
         title='Curriculum Vitae — Md Hasibul Hossain',
         desc='Full academic and professional curriculum vitae of Md Hasibul Hossain: '
              'education, research experience, work experience, laboratory expertise, '
              'digital skills, languages and references. PDF download available.',
         jsonld=False),
    dict(file='contact.html', body='body-contact.html', nav='CONTACT',
         page='contact.html',
         title='Contact — Md Hasibul Hossain',
         desc='Contact details and academic referees for Md Hasibul Hossain. Enquiries '
              'from prospective M.Sc. supervisors and research collaborators are welcome.',
         jsonld=False),
    dict(file='404.html', body='body-404.html', nav=None, page='404.html',
         title='Page not found — Md Hasibul Hossain',
         desc='The requested page could not be found. Links to the main sections '
              'of the academic website of Md Hasibul Hossain: about, research, '
              'experience, teaching and curriculum vitae.',
         jsonld=False),
]


def build_pages():
    head = read('head.html')
    footer = read('footer.html')
    jsonld = read('jsonld-index.html')

    for p in PAGES:
        out = head
        out = out.replace('{{TITLE}}', p['title'])
        out = out.replace('{{DESC}}', p['desc'])
        out = out.replace('{{PAGE}}', p['page'])
        out = out.replace('{{JSONLD}}', jsonld if p['jsonld'] else '')
        for key in NAV_KEYS:
            out = out.replace('{{NAV_%s}}' % key,
                              CURRENT if key == p['nav'] else '')
        out += read(p['body']) + footer
        assert '{{' not in out, 'unreplaced placeholder in ' + p['file']
        with io.open(os.path.join(ROOT, p['file']), 'w', encoding='utf-8') as fh:
            fh.write(out)
        print('  %-16s %7d bytes' % (p['file'], len(out.encode('utf-8'))))


# -------------------------------------------------------------- figures ----

FIG_TOKENS = '''  <style>
    /*  Standalone copy of a figure from mdhasibulhossain263-hk.github.io/hasain-academic-website
        Colours are defined here so the file works on its own in any
        viewer, and in Word, PowerPoint, Illustrator or Inkscape.       */
    :root {
      --font-display: Georgia, "Times New Roman", serif;
      --font-body: "Helvetica Neue", Helvetica, Arial, sans-serif;
      --font-mono: Menlo, Consolas, monospace;
      --fig-bg: #ffffff;
      --fig-panel: #f5f3ef;
      --fig-stroke: #b9b2a6;
      --fig-ink: #1b2a3a;
      --fig-ink-soft: #5c6b7a;
      --fig-1: #16365c;
      --fig-2: #1f7a6a;
      --fig-3: #b4802a;
      --fig-4: #9b4a2f;
      --fig-5: #5a6b86;
      --fig-grid: #e6e2da;
    }
    @media (prefers-color-scheme: dark) {
      :root {
        --fig-bg: #131f2b; --fig-panel: #192835; --fig-stroke: #46596b;
        --fig-ink: #dde6ee; --fig-ink-soft: #9aaab8;
        --fig-1: #7fb0e8; --fig-2: #4fc0aa; --fig-3: #e0a94f;
        --fig-4: #e08a6a; --fig-5: #93a6bd; --fig-grid: #24333f;
      }
    }
    svg { background: var(--fig-bg); }
  </style>
'''

FIGURES = {
    'index.html': [('fig-framework-title', 'figure-1-research-framework.svg')],
    'research.html': [
        ('fig2-title', 'figure-2-rha-production-and-programme.svg'),
        ('fig3-title', 'figure-3-oxide-composition-opc-vs-rha.svg'),
        ('fig4-title', 'figure-4-compressive-strength-results.svg'),
        ('fig5-title', 'figure-5-cost-and-water-absorption.svg'),
        ('fig6-title', 'figure-6-granular-pile-failure-mechanisms.svg'),
        ('fig7-title', 'figure-7-granular-pile-and-fe-model.svg'),
        ('fig8-title', 'figure-8-ann-pipeline-and-architecture.svg'),
        ('fig9-title', 'figure-9-astm-laboratory-programme.svg'),
    ],
}

# XML predefines only these five; every other HTML named entity must be
# converted to a literal character or the standalone SVG will not parse.
XML_SAFE = {'amp', 'lt', 'gt', 'quot', 'apos'}
_ENTITY_RE = re.compile(r'&([A-Za-z][A-Za-z0-9]*);')


def xmlify_entities(text):
    def sub(match):
        name = match.group(1)
        if name in XML_SAFE:
            return match.group(0)
        codepoint = html.entities.name2codepoint.get(name)
        if codepoint is None:
            raise ValueError('unknown entity &%s;' % name)
        return chr(codepoint)
    return _ENTITY_RE.sub(sub, text)


def split_svgs(markup):
    blocks, i = [], 0
    while True:
        start = markup.find('<svg ', i)
        if start == -1:
            return blocks
        end = markup.find('</svg>', start)
        blocks.append(markup[start:end + 6])
        i = end + 6


def build_figures():
    outdir = os.path.join(ROOT, 'assets', 'figures')
    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    for src, figs in FIGURES.items():
        with io.open(os.path.join(ROOT, src), encoding='utf-8') as fh:
            blocks = split_svgs(fh.read())
        for title_id, outname in figs:
            match = [b for b in blocks if 'id="%s"' % title_id in b]
            if not match:
                print('  !! figure not found:', title_id)
                continue
            svg = xmlify_entities(match[0])
            cut = svg.find('>')
            open_tag, rest = svg[:cut + 1], svg[cut + 1:]
            if 'xmlns=' not in open_tag:
                open_tag = open_tag[:-1] + ' xmlns="http://www.w3.org/2000/svg">'
            doc = ('<?xml version="1.0" encoding="UTF-8"?>\n'
                   + open_tag + '\n' + FIG_TOKENS + rest)
            with io.open(os.path.join(outdir, outname), 'w', encoding='utf-8') as fh:
                fh.write(doc)
            print('  %-48s %6d bytes' % (outname, len(doc.encode('utf-8'))))


if __name__ == '__main__':
    print('Building pages...')
    build_pages()
    print('\nExporting standalone figures...')
    build_figures()
    print('\nDone.')
