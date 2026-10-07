import json, base64, os
info = {v: json.load(open(f'info_{v}.json')) for v in 'LU'}
body = open('body.html').read().replace('/*INFO*/null', json.dumps(info))
# GitHub Pages version: full document, loads the .glb files next to it
head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<style>*{box-sizing:border-box}body{margin:0}[hidden]{display:none!important}</style>\n')
i = body.index('<div class="app">')
gh = head + body[:i] + '</head>\n<body>\n' + body[i:] + '\n</body>\n</html>\n'
os.makedirs('github/daata-hamlet-3d', exist_ok=True)
open('github/daata-hamlet-3d/index.html', 'w').write(gh)
# Claude artifact version: models embedded (artifacts cannot serve .glb)
a = """  loader.load(`DH-GF-${v}.glb`, g => { cache[v] = g; done(g); }, undefined,
    () => { st.textContent = 'The 3D model could not load. Check that DH-GF-' + v + '.glb sits next to this page.'; });"""
assert a in body
b = """  const bin = Uint8Array.from(atob(GLB[v]), c => c.charCodeAt(0)).buffer;
  loader.parse(bin, '', g => { cache[v] = g; done(g); }, () => { st.textContent = 'The 3D model could not load.'; });"""
g = {v: base64.b64encode(open(f'DH-GF-{v}.glb', 'rb').read()).decode() for v in 'LU'}
art = body.replace(a, b).replace('const INFO =', "const GLB = {L: '%s', U: '%s'};\nconst INFO =" % (g['L'], g['U']), 1)
open('daata_hamlet_3d.html', 'w').write(art)
# local test copies (three from node_modules)
os.makedirs('test', exist_ok=True)
open('test/index.html', 'w').write(gh.replace('https://cdn.jsdelivr.net/npm/three@0.147.0/', '/three/'))
open('test/artifact.html', 'w').write(head + art.replace('https://cdn.jsdelivr.net/npm/three@0.147.0/', '/three/') )
print('ok', len(art) / 1e6)
