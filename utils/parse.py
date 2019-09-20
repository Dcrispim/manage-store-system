import json



def strToArrayObj(stringObj,tryOnlyResponse=False):
    errors = []
    out_list = []
    if stringObj[0] == '[' or stringObj[-1] == ']':
        arrayObj = stringObj[1:-1].split('},')
    else:
        arrayObj = stringObj.split('},')
    try:
        for item in arrayObj[:-1]:
            try:
                if len(item)>1:
                    out_list.append(json.loads(item+'}'))
            except Exception as err:
                errors.append(err)
        try:        
            if len(arrayObj[-1])>1:
                out_list.append(json.loads(arrayObj[-1]))
        except Exception as err:
            errors.append(err)
    except Exception as erro:
        errors.append(erro)

    if tryOnlyResponse and len(errors)==0:
        return out_list

    return (out_list, errors)


    