
from pkg_resources import iter_entry_points

groups = ['ginga.rv.plugins']
for group in groups:
    for entry_point in iter_entry_points(group=group, name=None):
        print(entry_point)
