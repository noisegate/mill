import gcoder

gcodes = [i.strip() for i in open('./circle.ngc')]
gcodes = gcoder.LightGCode(gcodes)

print gcodes
