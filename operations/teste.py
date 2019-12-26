import math
import requests
import json
def makeBootstrapCssFile(maxw):
    for i in range(12):
        css = []
        css.append('.col-md-'+str(i+1)+'{')
        css.append(f"   max-width: {math.ceil((i+1)*(100/12))}%;")
        css.append('}')
        print('\n'.join(css))

makeBootstrapCssFile(576)
