import glob
import YamlStudies as ys
import yaml

CORDEX_DOMAIN = 'EUR'

alldata = []
for fname in glob.glob('CMIP6_studies/*.yaml'):
  with open(fname) as fp:
    entrylist = yaml.load(fp, Loader=yaml.FullLoader)
    for x in entrylist:
      x['file'] = fname
    alldata.extend(entrylist)

def is_incomplete(dic):
  try:
    return(dic['disabled']['cause'] == 'incomplete')
  except:
    return(False)

print(f'## Incomplete entries\n')
for x in alldata:
  if is_incomplete(x):
    print(f' * [{x["key"]}]({x["file"]})')

print(f'## Disabled entries\n')
for x in alldata:
  if 'disabled' in x:
    print(f' · [{x["key"]}]({x["file"]})')

with open('CMIP6_studies_config.yaml') as fp:
  config = yaml.load(fp, Loader=yaml.FullLoader)

alldata = ys.load_from_files('CMIP6_studies/*.yaml', resolve_doi = True, skip_disabled = True)
# filter and sort
alldata = [x for x in alldata if x.spatial_scope in config['spatial_scope_filter'][CORDEX_DOMAIN]]
alldata.sort(key=lambda x: config['spatial_scope_filter'][CORDEX_DOMAIN].index(x.spatial_scope))

typenames = dict(
  performance = 'Performance',
  future_spread = 'Spread of future outcomes',
  independence = 'Independence'
)
print(f'## Available entries ({CORDEX_DOMAIN} scope)')
for t in typenames:
  print(f'### {typenames[t]}')
  for x in alldata:
    if x.type == t:
      print(f'#### {x.key}\n')
      print(f'Located in [{x.file}]({x.file})\n')
      print(f'{x.reference}\n')
      print(f'```\n{x.__str__()}\n```\n')
