import re

lines = sc.textFile("frwiki_w_lines.corpus")

def remove_null(line):
    split = line.split(" ", 1)
    if len(split) > 1:
        return split[1]
    return ""

lines = lines.map(lambda line: line.split(" ", 1))
lines = lines.map(lambda (n, line): (n, remove_null(line)))
lines = lines.map(lambda (n, line): (n, re.sub("DBPEDIA_ID\/[^ ]* ", '', line)))
lines = lines.map(lambda (n, line): n + " " + line)

res = lines.coalesce(1, False).saveAsTextFile('frwiki_w_lines_wo_dbpedia2.txt')