
qa_lists = ['QA_list_updated.csv']
out_file = 'reg_failed_list.csv'


with open(out_file, 'w') as out:
    for list in qa_lists:
        with open(list, 'r') as f:
            for i, line in enumerate(f.readlines()):
                parts = line.strip().split(',')
                if len(parts[5]) != 0:
                    out.write(line)


