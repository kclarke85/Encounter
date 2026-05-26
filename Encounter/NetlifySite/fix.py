with open('../../../../Downloads/sentinel-portal-v2.html', 'r', encoding='utf-8-sig') as f:
    c = f.read()

pairs = [
    ('signup-firstname', 'signup-firstname'),
    ('signup-lastname', 'signup-lastname'),
    ('signup-org', 'signup-org'),
    ('signup-email', 'signup-email'),
    ('signup-password', 'signup-password'),
    ('signup-confirm', 'signup-confirm'),
]

for id_name, _ in pairs:
    bad = 'id="{}" id="{}"'.format(id_name, id_name)
    good = 'id="{}"'.format(id_name)
    c = c.replace(bad, good)

with open('../../../../Downloads/sentinel-portal-v2.html', 'w', encoding='utf-8') as f:
    f.write(c)

print('done')
