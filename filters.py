
dirs = ['v0_0', 'v0_1', 'v0_2', 'v1_0', 'v1_1', 'v2_0', 'v2_1', 'v2_2', 'v2_3', 'v3_0']
major = 1
result = []
filters = []

for m in range(major+1):
    result += list(filter(lambda x: x.startswith(f'v{m}_'), dirs))

print(result)

if __name__ == '__main__':
    print('Done.')
