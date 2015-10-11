#ings = set(open("ingredients_sorted_by_count").read().split("\n")[:20])
ings = set(open("handpicked").read().split("\n")[:20])
print len(ings)
with open("export.dm") as f:
    with open("plotting.csv","w") as fw:
        for line in f:
            if line.split("\t")[0] in ings:
                fw.write(line)
